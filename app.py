import streamlit as st
import pandas as pd
import urllib.parse
from supabase import create_client

st.set_page_config(page_title="B2B Vehicles", layout="wide", page_icon="🚘")

hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

# ==========================================
# 🌐 SPROG OG OVERSÆTTELSER
# ==========================================
translations = {
    "en": {
        "title": "🚘 Dealer Portal (B2B Vehicles)",
        "subtitle": "Welcome to our B2B portal. Here you will find our current vehicles ready for export or trade.",
        "search": "🔍 Search make/model",
        "vat": "🏷️ VAT", "tax": "⚖️ Tax", "sort": "🔽 Sort by", "all": "All",
        "buy": "🛒 Buy", "bid": "⚖️ Bid", "print": "🖨️ Print / PDF",
        "view": "📸 View details & photos", "no_cars": "There are currently no active vehicles for sale.",
        "tech_data": "⚙️ Technical Data", "mail_sub": "Purchase of",
        "mail_koeb_body": "Hi Mathias and Brian,\n\nI would like to purchase the vehicle at the advertised price.\n\nVIN: ",
        "mail_byd_body":  "Hi Mathias and Brian,\n\nI would like to make an offer on the vehicle.\n\nMy offer is: [Enter your bid here] EUR\n\nVIN: ",
        "pkg_title": "📦 Your Package",
        "pkg_info": "Click '➕ Add to package' under the cars to bundle them and make a combined offer.",
        "pkg_your_bids": "**Your bids per car:**", "pkg_list_price": "List price",
        "pkg_total_list": "**Total list price:**", "pkg_total_bid": "**Your total bid:**",
        "pkg_send_mail": "✉️ Send combined bid (Mail)", "pkg_send_wa": "💬 Send combined bid (WA)",
        "pkg_clear": "🗑️ Clear package", "pkg_add": "➕ Add to package", "pkg_rm": "➖ Remove",
        "pkg_mail_body": "Hi Mathias and Brian,\n\nI would like to make the following combined offer for {count} cars:\n\n{cars}\n\nTotal combined bid: € {total}\n\nBest regards,",
        "sort_default": "Newest added (Default)", "sort_price_asc": "Price: Low to High",
        "sort_price_desc": "Price: High to Low", "sort_year_desc": "Year: Newest first",
        "sort_km_asc": "Mileage: Lowest first",
        "year": "Year", "odometer": "Odometer", "price": "Price", "gearbox": "Gearbox",
        "fuel": "Fuel type", "paint_areas": "Paint areas", "location": "Location",
        "reg_nr": "Reg. nr.", "vin": "VIN", "co2": "CO2-emission", "equip": "Equipment & Remarks",
        "Inkl. Moms": "Incl. VAT", "Ekskl. Moms": "Excl. VAT", "Momsfri": "VAT Free", "Papegøje": "Parrot plates (DK)",
        "Uden Afgift": "Excl. Tax", "Med Afgift": "Incl. Tax", "Forholdsmæssig": "Proportional Tax",
        "inkl. moms": "Incl. VAT", "ekskl. moms": "Excl. VAT", "uden afgift": "Excl. Tax", "med afgift": "Incl. Tax",
        "Manuel": "Manual", "Automatgear": "Automatic", "Automatisk": "Automatic",
        "Benzin": "Petrol", "Diesel": "Diesel", "Hybrid": "Hybrid", "El": "Electric",
        "Elektrisk": "Electric", "Plugin hybrid": "Plugin Hybrid",
    },
    "de": {
        "title": "🚘 Händler-Portal (B2B Fahrzeuge)",
        "subtitle": "Willkommen in unserem B2B-Portal. Hier finden Sie unsere aktuellen Fahrzeuge für den Export oder Handel.",
        "search": "🔍 Marke/Modell suchen", "vat": "🏷️ MwSt", "tax": "⚖️ Steuer",
        "sort": "🔽 Sortieren nach", "all": "Alle", "buy": "🛒 Kaufen", "bid": "⚖️ Bieten",
        "print": "🖨️ Drucken / PDF", "view": "📸 Details & Fotos",
        "no_cars": "Derzeit stehen keine aktiven Fahrzeuge zum Verkauf.",
        "tech_data": "⚙️ Technische Daten", "mail_sub": "Kauf von",
        "mail_koeb_body": "Hallo Mathias und Brian,\n\nich möchte das Fahrzeug zum angegebenen Preis kaufen.\n\nFIN: ",
        "mail_byd_body":  "Hallo Mathias und Brian,\n\nich möchte ein Angebot abgeben.\n\nMein Angebot: [Bitte eingeben] EUR\n\nFIN: ",
        "pkg_title": "📦 Ihr Paket", "pkg_info": "Klicken Sie auf '➕ Zum Paket' um ein Gesamtangebot abzugeben.",
        "pkg_your_bids": "**Ihre Gebote pro Auto:**", "pkg_list_price": "Listenpreis",
        "pkg_total_list": "**Gesamtlistenpreis:**", "pkg_total_bid": "**Ihr Gesamtgebot:**",
        "pkg_send_mail": "✉️ Gesamtangebot senden (Mail)", "pkg_send_wa": "💬 Gesamtangebot senden (WA)",
        "pkg_clear": "🗑️ Paket leeren", "pkg_add": "➕ Zum Paket", "pkg_rm": "➖ Entfernen",
        "pkg_mail_body": "Hallo Mathias und Brian,\n\nGesamtangebot für {count} Fahrzeuge:\n\n{cars}\n\nGesamtgebot: € {total}\n\nMit freundlichen Grüßen,",
        "sort_default": "Zuletzt hinzugefügt", "sort_price_asc": "Preis: Aufsteigend",
        "sort_price_desc": "Preis: Absteigend", "sort_year_desc": "Jahr: Neueste zuerst",
        "sort_km_asc": "Kilometer: Niedrigste zuerst",
        "year": "Jahr", "odometer": "Kilometerstand", "price": "Preis", "gearbox": "Getriebe",
        "fuel": "Kraftstoff", "paint_areas": "Lackierfelder", "location": "Standort",
        "reg_nr": "Kennzeichen", "vin": "FIN", "co2": "CO2-Ausstoß", "equip": "Ausstattung & Bemerkungen",
        "Inkl. Moms": "Inkl. MwSt", "Ekskl. Moms": "Exkl. MwSt", "Momsfri": "MwSt-Frei", "Papegøje": "Papageienschilder (DK)",
        "Uden Afgift": "Exkl. Steuer", "Med Afgift": "Inkl. Steuer", "Forholdsmæssig": "Verhältnismäßige Steuer",
        "inkl. moms": "Inkl. MwSt", "ekskl. moms": "Exkl. MwSt", "uden afgift": "Exkl. Steuer", "med afgift": "Inkl. Steuer",
        "Manuel": "Schaltgetriebe", "Automatgear": "Automatik", "Automatisk": "Automatik",
        "Benzin": "Benzin", "Diesel": "Diesel", "Hybrid": "Hybrid", "El": "Elektro",
        "Elektrisk": "Elektro", "Plugin hybrid": "Plugin Hybrid",
    },
    "nl": {
        "title": "🚘 Dealerportaal (B2B Voertuigen)",
        "subtitle": "Welkom op ons B2B portaal. Hier vindt u onze actuele voertuigen klaar voor export of handel.",
        "search": "🔍 Zoek merk/model", "vat": "🏷️ BTW", "tax": "⚖️ Belasting",
        "sort": "🔽 Sorteer op", "all": "Alle", "buy": "🛒 Kopen", "bid": "⚖️ Bieden",
        "print": "🖨️ Print / PDF", "view": "📸 Bekijk details & foto's",
        "no_cars": "Er staan momenteel geen actieve voertuigen te koop.",
        "tech_data": "⚙️ Technische Gegevens", "mail_sub": "Aankoop van",
        "mail_koeb_body": "Hallo Mathias en Brian,\n\nIk wil graag het voertuig kopen.\n\nChassisnummer: ",
        "mail_byd_body":  "Hallo Mathias en Brian,\n\nIk wil graag bieden.\n\nMijn bod: [Vul in] EUR\n\nChassisnummer: ",
        "pkg_title": "📦 Uw Pakket", "pkg_info": "Klik op '➕ Aan pakket' om voertuigen te bundelen.",
        "pkg_your_bids": "**Uw biedingen per auto:**", "pkg_list_price": "Lijstprijs",
        "pkg_total_list": "**Totale lijstprijs:**", "pkg_total_bid": "**Uw totaalbod:**",
        "pkg_send_mail": "✉️ Stuur totaalbod (Mail)", "pkg_send_wa": "💬 Stuur totaalbod (WA)",
        "pkg_clear": "🗑️ Pakket wissen", "pkg_add": "➕ Aan pakket", "pkg_rm": "➖ Verwijderen",
        "pkg_mail_body": "Hallo Mathias en Brian,\n\nTotaalbod voor {count} voertuigen:\n\n{cars}\n\nTotaalbod: € {total}\n\nMet vriendelijke groet,",
        "sort_default": "Nieuwste eerst", "sort_price_asc": "Prijs: Laag naar Hoog",
        "sort_price_desc": "Prijs: Hoog naar Laag", "sort_year_desc": "Jaar: Nieuwste eerst",
        "sort_km_asc": "Kilometerstand: Laagste eerst",
        "year": "Jaar", "odometer": "Kilometerstand", "price": "Prijs", "gearbox": "Versnellingsbak",
        "fuel": "Brandstof", "paint_areas": "Spuitdelen", "location": "Locatie",
        "reg_nr": "Kenteken", "vin": "Chassisnummer", "co2": "CO2-uitstoot", "equip": "Uitrusting & Opmerkingen",
        "Inkl. Moms": "Incl. BTW", "Ekskl. Moms": "Excl. BTW", "Momsfri": "BTW Vrij", "Papegøje": "Papegaaienplaten (DK)",
        "Uden Afgift": "Excl. Belasting", "Med Afgift": "Incl. Belasting", "Forholdsmæssig": "Proportionele Belasting",
        "inkl. moms": "Incl. BTW", "ekskl. moms": "Excl. BTW", "uden afgift": "Excl. Belasting", "med afgift": "Incl. Belasting",
        "Manuel": "Handgeschakeld", "Automatgear": "Automaat", "Automatisk": "Automaat",
        "Benzin": "Benzine", "Diesel": "Diesel", "Hybrid": "Hybride", "El": "Elektrisch",
        "Elektrisk": "Elektrisch", "Plugin hybrid": "Plugin Hybride",
    }
}

WHATSAPP_NUMBER = "4561438202"

# ==========================================
# 🔌 SUPABASE
# ==========================================
@st.cache_resource
def init_connection():
    return create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])

supabase = init_connection()

@st.cache_data(ttl=60)
def load_b2b_data():
    """Henter alle aktive biler — ingen drivmiddel-filter, viser alle typer."""
    try:
        res = supabase.table("b2b_lager") \
            .select("*") \
            .eq("status", "Aktiv") \
            .execute()
        return pd.DataFrame(res.data) if res.data else pd.DataFrame()
    except Exception as e:
        st.error(f"Kunne ikke hente data: {e}")
        return pd.DataFrame()

def safe(val):
    if val is None or (isinstance(val, float) and pd.isna(val)):
        return ""
    return str(val).strip()

def translate_term(term_str, lang_dict):
    term_clean = safe(term_str)
    return lang_dict.get(term_clean) or lang_dict.get(term_clean.lower()) or term_clean

# ==========================================
# 🌐 SPROG VÆLGER
# ==========================================
col_lang, _ = st.columns([1, 5])
lang = col_lang.selectbox("🌐 Language", ["English", "Deutsch", "Nederlands"])
l = {"English": "en", "Deutsch": "de", "Nederlands": "nl"}[lang]
t = translations[l]

# ==========================================
# 🛒 SESSION STATE
# ==========================================
if 'cart_exp' not in st.session_state:
    st.session_state['cart_exp'] = {}

# ==========================================
# 📦 SIDEMENU
# ==========================================
with st.sidebar:
    st.header(t["pkg_title"])
    if not st.session_state['cart_exp']:
        st.info(t["pkg_info"])
    else:
        total_list_price = 0
        total_bid_price  = 0
        cart_text_lines  = []

        st.write(t["pkg_your_bids"])
        for key, car in st.session_state['cart_exp'].items():
            total_list_price += car['price_int']
            current_bid = car.get('bid_price', car['price_int'])
            listepris_str = f"€ {car['price_int']:,}".replace(',', '.')
            new_bid = st.number_input(
                f"{car['title']} ({t['pkg_list_price']}: {listepris_str})",
                min_value=0, value=int(current_bid), step=100, key=f"bid_{key}"
            )
            st.session_state['cart_exp'][key]['bid_price'] = new_bid
            total_bid_price += new_bid
            bid_str = f"€ {new_bid:,}".replace(',', '.')
            cart_text_lines.append(f"- {car['title']} (VIN: {car['vin']}) -> Bid: {bid_str}")

        st.write("---")
        st.write(f"{t['pkg_total_list']} € {total_list_price:,}".replace(',', '.'))
        st.write(t["pkg_total_bid"])
        st.markdown(f"<h3 style='color:#2e7b32;margin-top:-10px;'>€ {total_bid_price:,}</h3>".replace(',', '.'), unsafe_allow_html=True)
        st.write("---")

        cars_str      = "\n".join(cart_text_lines)
        total_bid_str = f"{total_bid_price:,}".replace(',', '.')
        mail_body = t["pkg_mail_body"].format(
            count=len(st.session_state['cart_exp']),
            cars=cars_str,
            total=total_bid_str
        )
        mail_link = f"mailto:matsc@maulbiler.dk,brmau@maulbiler.dk?subject=Offer on {len(st.session_state['cart_exp'])} cars&body={urllib.parse.quote(mail_body)}"
        wa_link   = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(mail_body)}"

        st.markdown(f"<a href='{mail_link}' target='_blank'><button style='width:100%;border-radius:5px;background:#2e7b32;color:white;border:none;padding:10px;cursor:pointer;font-size:14px;font-weight:bold;margin-bottom:8px;'>{t['pkg_send_mail']}</button></a>", unsafe_allow_html=True)
        st.markdown(f"<a href='{wa_link}'   target='_blank'><button style='width:100%;border-radius:5px;background:#25D366;color:white;border:none;padding:10px;cursor:pointer;font-size:14px;font-weight:bold;margin-bottom:20px;'>{t['pkg_send_wa']}</button></a>", unsafe_allow_html=True)

        if st.button(t["pkg_clear"], use_container_width=True):
            st.session_state['cart_exp'] = {}
            st.rerun()

# ==========================================
# TITEL
# ==========================================
st.title(t["title"])
st.write(t["subtitle"])

# ==========================================
# 🔍 DETAIL-DIALOG
# ==========================================
@st.dialog(t["view"], width="large")
def show_car_details(row, lang_dict):
    st.markdown(f"## {safe(row.get('maerke'))} {safe(row.get('model'))}")
    st.markdown(f"#### {safe(row.get('variant'))}")
    st.write("")

    pris_int     = int(row.get('pris_euro') or 0)
    pris_display = f"€ {pris_int:,}".replace(',', '.') if pris_int > 0 else "Make offer"

    m1, m2, m3 = st.columns(3)
    m1.metric(lang_dict["year"],     safe(row.get('aargang'))[:4])
    m2.metric(lang_dict["odometer"], safe(row.get('odometer')))
    m3.metric(lang_dict["price"],    pris_display)
    st.write("---")

    pdf_url      = safe(row.get('udstyrsliste_pdf'))
    skade_string = safe(row.get('skadesbilleder_url'))
    has_pdf      = bool(pdf_url)
    has_skader   = bool(skade_string)

    if has_pdf or has_skader:
        tab1, tab2, tab3 = st.tabs(["📸 Photos", lang_dict['tech_data'], "⚠️ Damage & Equipment"])
    else:
        tab1, tab2 = st.tabs(["📸 Photos", lang_dict['tech_data']])

    with tab1:
        img_string = safe(row.get('billede_url'))
        images = [u.strip() for u in img_string.split(',')] if img_string else []
        if images:
            for img in images:
                if img.startswith('http'):
                    st.image(img, use_container_width=True)
                    st.write("---")
        else:
            st.info("No images available.")

    with tab2:
        c1, c2 = st.columns(2)
        c1.write(f"**Make:** {safe(row.get('maerke'))}")
        c1.write(f"**Model:** {safe(row.get('model'))}")
        c1.write(f"**Variant:** {safe(row.get('variant'))}")
        c1.write(f"**{lang_dict['gearbox']}:** {translate_term(row.get('gearkasse'), lang_dict)}")
        c1.write(f"**{lang_dict['fuel']}:** {translate_term(row.get('drivmiddel'), lang_dict)}")
        c1.write(f"**{lang_dict['paint_areas']}:** {safe(row.get('lakfelter'))}")
        c2.write(f"**EURO norm:** {safe(row.get('euro_norm'))}")
        c2.write(f"**{lang_dict['co2']}:** {safe(row.get('co2'))}")
        c2.write(f"**{lang_dict['reg_nr']}:** {safe(row.get('reg_nr'))}")
        c2.write(f"**{lang_dict['vin']}:** {safe(row.get('stelnummer'))}")
        c2.write(f"**{lang_dict['location']}:** {safe(row.get('lokation'))}")
        c1.write("---"); c2.write("---")
        c1.write(f"**VAT:** {translate_term(row.get('moms_status'), lang_dict)}")
        c2.write(f"**Tax:** {translate_term(row.get('afgift_status'), lang_dict)}")
        st.write("---")
        st.write(f"**{lang_dict['equip']}:**")
        udstyr_val = safe(row.get('udstyr'))
        st.info(udstyr_val if udstyr_val else "No remarks.")

    if has_pdf or has_skader:
        with tab3:
            if has_pdf:
                st.subheader("📄 Equipment list")
                st.markdown(f"<a href='{pdf_url}' target='_blank'><button style='width:100%;border-radius:5px;background:#3b82f6;color:white;border:none;padding:10px;cursor:pointer;font-size:15px;font-weight:bold;margin-bottom:20px;'>Open Equipment List (PDF)</button></a>", unsafe_allow_html=True)
            if has_skader:
                st.subheader("⚠️ Noted damages")
                for img in [u.strip() for u in skade_string.split(',')]:
                    if img.startswith('http'):
                        st.image(img, use_container_width=True)
                        st.write("---")

    st.write("---")
    vin          = safe(row.get('stelnummer')) or 'Unknown'
    maerke_model = f"{safe(row.get('maerke'))} {safe(row.get('model'))}"
    modtagere    = "matsc@maulbiler.dk,brmau@maulbiler.dk"

    mail_link_koeb = f"mailto:{modtagere}?subject={urllib.parse.quote(lang_dict['mail_sub'] + ' ' + maerke_model + ' (VIN: ' + vin + ')')}&body={urllib.parse.quote(lang_dict['mail_koeb_body'] + vin)}"
    mail_link_byd  = f"mailto:{modtagere}?subject={urllib.parse.quote('Offer: ' + maerke_model + ' (VIN: ' + vin + ')')}&body={urllib.parse.quote(lang_dict['mail_byd_body'] + vin)}"

    btn1, btn2 = st.columns(2)
    btn1.markdown(f"<a href='{mail_link_koeb}' target='_blank'><button style='width:100%;border-radius:5px;background:#2e7b32;color:white;border:none;padding:12px;cursor:pointer;font-size:16px;font-weight:bold;'>{lang_dict['buy']}</button></a>", unsafe_allow_html=True)
    btn2.markdown(f"<a href='{mail_link_byd}'  target='_blank'><button style='width:100%;border-radius:5px;background:#555555;color:white;border:none;padding:12px;cursor:pointer;font-size:16px;font-weight:bold;'>{lang_dict['bid']}</button></a>", unsafe_allow_html=True)

# ==========================================
# HOVEDPROGRAM
# ==========================================
df = load_b2b_data()

if df is not None and not df.empty:

    df['Sort_Price'] = pd.to_numeric(df['pris_euro'], errors='coerce').fillna(0)
    df['Sort_Year']  = pd.to_numeric(df['aargang'].astype(str).str[:4], errors='coerce').fillna(0)
    df['Sort_Km']    = pd.to_numeric(df['odometer'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(9999999)

    # --- FILTRE ---
    c_search, c_moms, c_afgift, c_sort = st.columns(4)
    search_q = c_search.text_input(t["search"])

    moms_opts   = [t["all"]] + sorted(df['moms_status'].dropna().unique().tolist())
    afgift_opts = [t["all"]] + sorted(df['afgift_status'].dropna().unique().tolist())
    moms_q   = c_moms.selectbox(t["vat"],  moms_opts)
    afgift_q = c_afgift.selectbox(t["tax"], afgift_opts)

    sort_opts_map = {
        t["sort_default"]:   "default",
        t["sort_price_asc"]: "price_asc",
        t["sort_price_desc"]:"price_desc",
        t["sort_year_desc"]: "year_desc",
        t["sort_km_asc"]:    "km_asc",
    }
    sort_q = sort_opts_map[c_sort.selectbox(t["sort"], list(sort_opts_map.keys()))]

    if search_q:  df = df[df.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
    if moms_q   != t["all"]: df = df[df['moms_status']   == moms_q]
    if afgift_q != t["all"]: df = df[df['afgift_status'] == afgift_q]

    if sort_q == "price_asc":   df = df.sort_values('Sort_Price', ascending=True)
    elif sort_q == "price_desc": df = df.sort_values('Sort_Price', ascending=False)
    elif sort_q == "year_desc":  df = df.sort_values('Sort_Year',  ascending=False)
    elif sort_q == "km_asc":     df = df.sort_values('Sort_Km',    ascending=True)

    st.write("---")

    # --- KORT VISNING ---
    cols_per_row = 3
    for i in range(0, len(df), cols_per_row):
        cols  = st.columns(cols_per_row)
        chunk = df.iloc[i:i + cols_per_row]

        for col, (_, row) in zip(cols, chunk.iterrows()):
            with col:
                with st.container(border=True):

                    # Cover-billede
                    first_img = safe(row.get('billede_url', '')).split(',')[0].strip()
                    if first_img.startswith('http'):
                        st.image(first_img, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/400x250?text=No+image", use_container_width=True)

                    # Titel
                    st.markdown(f"### {safe(row.get('maerke'))} {safe(row.get('model'))}")
                    st.markdown(f"*{safe(row.get('variant'))}*")

                    # Stelnummer (VIN) på forsiden
                    stel = safe(row.get('stelnummer'))
                    if stel:
                        st.caption(f"🔑 {t['vin']}: {stel}")

                    st.write("")

                    # Specs
                    aarstal    = safe(row.get('aargang'))[:4]
                    km_str     = safe(row.get('odometer'))
                    disp_gear  = translate_term(row.get('gearkasse'), t)
                    disp_fuel  = translate_term(row.get('drivmiddel'), t)
                    disp_moms  = translate_term(row.get('moms_status'), t)
                    disp_tax   = translate_term(row.get('afgift_status'), t)

                    st.markdown(f"📅 **{aarstal}** &nbsp; | &nbsp; 🛣️ **{km_str}** <br> 🕹️ **{disp_gear}** &nbsp; | &nbsp; ⛽ **{disp_fuel}**", unsafe_allow_html=True)
                    st.markdown(f"🏷️ {disp_moms} &nbsp; | &nbsp; ⚖️ {disp_tax}")

                    # Udstyr expander
                    udstyr_val = safe(row.get('udstyr'))
                    if udstyr_val:
                        with st.expander(f"🔧 {t['equip']}"):
                            st.write(udstyr_val)

                    # Pris
                    pris_int = int(row.get('Sort_Price', 0))
                    st.write("---")
                    if pris_int > 0:
                        st.markdown(f"<h2 style='text-align:center;color:#2e7b32;font-weight:bold;'>€ {pris_int:,}</h2>".replace(',', '.'), unsafe_allow_html=True)
                    else:
                        st.markdown("<h2 style='text-align:center;'>Make offer</h2>", unsafe_allow_html=True)

                    # Detalje knap
                    if st.button(t["view"], key=f"view_{row.name}", use_container_width=True):
                        show_car_details(row, t)

                    # Køb / Byd
                    vin          = stel or str(row.name)
                    maerke_model = f"{safe(row.get('maerke'))} {safe(row.get('model'))}"
                    modtagere    = "matsc@maulbiler.dk,brmau@maulbiler.dk"

                    mail_link_koeb = f"mailto:{modtagere}?subject={urllib.parse.quote(t['mail_sub'] + ' ' + maerke_model + ' (VIN: ' + vin + ')')}&body={urllib.parse.quote(t['mail_koeb_body'] + vin)}"
                    mail_link_byd  = f"mailto:{modtagere}?subject={urllib.parse.quote('Offer: ' + maerke_model + ' (VIN: ' + vin + ')')}&body={urllib.parse.quote(t['mail_byd_body'] + vin)}"

                    c_btn1, c_btn2 = st.columns(2)
                    c_btn1.markdown(f"<a href='{mail_link_koeb}' target='_blank'><button style='width:100%;border-radius:5px;background:#2e7b32;color:white;border:none;padding:6px;cursor:pointer;font-size:14px;font-weight:bold;'>{t['buy']}</button></a>", unsafe_allow_html=True)
                    c_btn2.markdown(f"<a href='{mail_link_byd}'  target='_blank'><button style='width:100%;border-radius:5px;background:#555555;color:white;border:none;padding:6px;cursor:pointer;font-size:14px;font-weight:bold;'>{t['bid']}</button></a>", unsafe_allow_html=True)

                    # Pakkekøb
                    st.write("")
                    vin_key = vin
                    if vin_key in st.session_state['cart_exp']:
                        if st.button(t["pkg_rm"], key=f"rm_{row.name}", use_container_width=True):
                            del st.session_state['cart_exp'][vin_key]
                            st.rerun()
                    else:
                        if st.button(t["pkg_add"], key=f"add_{row.name}", use_container_width=True):
                            st.session_state['cart_exp'][vin_key] = {
                                'title':     maerke_model,
                                'price_int': pris_int,
                                'vin':       vin,
                                'bid_price': pris_int,
                            }
                            st.rerun()
else:
    st.info(t["no_cars"])
