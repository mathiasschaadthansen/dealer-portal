import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="B2B Vehicles", layout="wide", page_icon="🚘")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# --- SPROG OG OVERSÆTTELSER ---
translations = {
    "en": {
        "title": "🚘 Dealer Portal (B2B Vehicles)",
        "subtitle": "Welcome to our B2B portal. Here you will find our current vehicles ready for export or trade.",
        "search": "🔍 Search make/model",
        "vat": "🏷️ VAT",
        "tax": "⚖️ Tax",
        "sort": "🔽 Sort by",
        "all": "All",
        "buy": "🛒 Buy",
        "bid": "⚖️ Bid",
        "print": "🖨️ Print / PDF",
        "view": "📸 View details & photos",
        "no_cars": "There are currently no active vehicles for sale.",
        "tech_data": "⚙️ Technical Data",
        "mail_sub": "Purchase of",
        "mail_koeb_body": "Hi Mathias and Brian,\n\nI would like to purchase the vehicle at the advertised price.\n\nVIN: ",
        "mail_byd_body": "Hi Mathias and Brian,\n\nI would like to make an offer on the vehicle.\n\nMy offer is: [Enter your bid here] EUR\n\nVIN: ",
        # Pakke funktion
        "pkg_title": "📦 Your Package",
        "pkg_info": "Click '➕ Add to package' under the cars to bundle them and make a combined offer.",
        "pkg_your_bids": "**Your bids per car:**",
        "pkg_list_price": "List price",
        "pkg_total_list": "**Total list price:**",
        "pkg_total_bid": "**Your total bid:**",
        "pkg_send_mail": "✉️ Send combined bid (Mail)",
        "pkg_send_wa": "💬 Send combined bid (WA)",
        "pkg_clear": "🗑️ Clear package",
        "pkg_add": "➕ Add to package",
        "pkg_rm": "➖ Remove",
        "pkg_mail_body": "Hi Mathias and Brian,\n\nI would like to make the following combined offer for {count} cars:\n\n{cars}\n\nTotal combined bid: € {total}\n\nBest regards,",
        # Sortering
        "sort_default": "Newest added (Default)",
        "sort_price_asc": "Price: Low to High",
        "sort_price_desc": "Price: High to Low",
        "sort_year_desc": "Year: Newest first",
        "sort_km_asc": "Mileage: Lowest first",
        # Tekniske felter
        "year": "Year",
        "odometer": "Odometer",
        "price": "Price",
        "gearbox": "Gearbox",
        "fuel": "Fuel type",
        "paint_areas": "Paint areas",
        "location": "Location",
        "reg_nr": "Reg. nr.",
        "vin": "VIN",
        "co2": "CO2-emission",
        "equip": "Equipment & Remarks",
        # Status oversættelser
        "Inkl. Moms": "Incl. VAT", "Ekskl. Moms": "Excl. VAT", "Momsfri": "VAT Free", "Papegøje": "Parrot plates (DK)",
        "Uden Afgift": "Excl. Tax", "Med Afgift": "Incl. Tax", "Forholdsmæssig": "Proportional Tax",
        "inkl. moms": "Incl. VAT", "ekskl. moms": "Excl. VAT", "uden afgift": "Excl. Tax", "med afgift": "Incl. Tax",
        # Gearkasse & Drivmiddel
        "Manuel": "Manual", "Automatgear": "Automatic", "Automatisk": "Automatic",
        "Benzin": "Petrol", "Diesel": "Diesel", "Hybrid": "Hybrid", "El": "Electric", "Plugin hybrid": "Plugin Hybrid"
    },
    "de": {
        "title": "🚘 Händler-Portal (B2B Fahrzeuge)",
        "subtitle": "Willkommen in unserem B2B-Portal. Hier finden Sie unsere aktuellen Fahrzeuge für den Export oder Handel.",
        "search": "🔍 Marke/Modell suchen", "vat": "🏷️ MwSt", "tax": "⚖️ Steuer", "sort": "🔽 Sortieren nach",
        "all": "Alle", "buy": "🛒 Kaufen", "bid": "⚖️ Bieten", "print": "🖨️ Drucken / PDF",
        "view": "📸 Details & Fotos", "no_cars": "Derzeit stehen keine aktiven Fahrzeuge zum Verkauf.",
        "tech_data": "⚙️ Technische Daten", "mail_sub": "Kauf von", 
        "mail_koeb_body": "Hallo Mathias und Brian,\n\nich möchte das Fahrzeug zum angegebenen Preis kaufen.\n\nFIN: ",
        "mail_byd_body": "Hallo Mathias und Brian,\n\nich möchte ein Angebot für das Fahrzeug abgeben.\n\nMein Angebot lautet: [Bitte Angebot eingeben] EUR\n\nFIN: ",
        "pkg_title": "📦 Ihr Paket", "pkg_info": "Klicken Sie auf '➕ Zum Paket hinzufügen', um ein Gesamtangebot abzugeben.",
        "pkg_your_bids": "**Ihre Gebote pro Auto:**", "pkg_list_price": "Listenpreis", "pkg_total_list": "**Gesamtlistenpreis:**",
        "pkg_total_bid": "**Ihr Gesamtgebot:**", "pkg_send_mail": "✉️ Gesamtangebot senden (Mail)", "pkg_send_wa": "💬 Gesamtangebot senden (WA)",
        "pkg_clear": "🗑️ Paket leeren", "pkg_add": "➕ Zum Paket", "pkg_rm": "➖ Entfernen",
        "pkg_mail_body": "Hallo Mathias und Brian,\n\nich möchte folgendes Gesamtangebot für {count} Fahrzeuge abgeben:\n\n{cars}\n\nMein Gesamtgebot: € {total}\n\nMit freundlichen Grüßen,",
        "sort_default": "Zuletzt hinzugefügt", "sort_price_asc": "Preis: Aufsteigend", "sort_price_desc": "Preis: Absteigend",
        "sort_year_desc": "Jahr: Neueste zuerst", "sort_km_asc": "Kilometer: Niedrigste zuerst",
        "year": "Jahr", "odometer": "Kilometerstand", "price": "Preis", "gearbox": "Getriebe", "fuel": "Kraftstoff",
        "paint_areas": "Lackierfelder", "location": "Standort", "reg_nr": "Kennzeichen", "vin": "FIN",
        "co2": "CO2-Ausstoß", "equip": "Ausstattung & Bemerkungen",
        "Inkl. Moms": "Inkl. MwSt", "Ekskl. Moms": "Exkl. MwSt", "Momsfri": "MwSt-Frei", "Papegøje": "Papageienschilder (DK)",
        "Uden Afgift": "Exkl. Steuer", "Med Afgift": "Inkl. Steuer", "Forholdsmæssig": "Verhältnismäßige Steuer",
        "inkl. moms": "Inkl. MwSt", "ekskl. moms": "Exkl. MwSt", "uden afgift": "Exkl. Steuer", "med afgift": "Inkl. Steuer",
        "Manuel": "Schaltgetriebe", "Automatgear": "Automatik", "Automatisk": "Automatik",
        "Benzin": "Benzin", "Diesel": "Diesel", "Hybrid": "Hybrid", "El": "Elektro", "Plugin hybrid": "Plugin Hybrid"
    },
    "nl": {
        "title": "🚘 Dealerportaal (B2B Voertuigen)",
        "subtitle": "Welkom op ons B2B portaal. Hier vindt u onze actuele voertuigen klaar voor export of handel.",
        "search": "🔍 Zoek merk/model", "vat": "🏷️ BTW", "tax": "⚖️ Belasting", "sort": "🔽 Sorteer op",
        "all": "Alle", "buy": "🛒 Kopen", "bid": "⚖️ Bieden", "print": "🖨️ Print / PDF",
        "view": "📸 Bekijk details & foto's", "no_cars": "Er staan momenteel geen actieve voertuigen te koop.",
        "tech_data": "⚙️ Technische Gegevens", "mail_sub": "Aankoop van", 
        "mail_koeb_body": "Hallo Mathias en Brian,\n\nIk wil graag het voertuig voor de geadverteerde prijs kopen.\n\nChassisnummer: ",
        "mail_byd_body": "Hallo Mathias en Brian,\n\nIk wil graag een bod uitbrengen op het voertuig.\n\nMijn bod is: [Vul uw bod in] EUR\n\nChassisnummer: ",
        "pkg_title": "📦 Uw Pakket", "pkg_info": "Klik op '➕ Aan pakket toevoegen' om voertuigen te bundelen voor een totaalbod.",
        "pkg_your_bids": "**Uw biedingen per auto:**", "pkg_list_price": "Lijstprijs", "pkg_total_list": "**Totale lijstprijs:**",
        "pkg_total_bid": "**Uw totaalbod:**", "pkg_send_mail": "✉️ Stuur totaalbod (Mail)", "pkg_send_wa": "💬 Stuur totaalbod (WA)",
        "pkg_clear": "🗑️ Pakket wissen", "pkg_add": "➕ Aan pakket", "pkg_rm": "➖ Verwijderen",
        "pkg_mail_body": "Hallo Mathias en Brian,\n\nIk wil graag het volgende totaalbod doen voor {count} voertuigen:\n\n{cars}\n\nTotaalbod: € {total}\n\nMet vriendelijke groet,",
        "sort_default": "Nieuwste eerst", "sort_price_asc": "Prijs: Laag naar Hoog", "sort_price_desc": "Prijs: Hoog naar Laag",
        "sort_year_desc": "Jaar: Nieuwste eerst", "sort_km_asc": "Kilometerstand: Laagste eerst",
        "year": "Jaar", "odometer": "Kilometerstand", "price": "Prijs", "gearbox": "Versnellingsbak", "fuel": "Brandstof",
        "paint_areas": "Spuitdelen", "location": "Locatie", "reg_nr": "Kenteken", "vin": "Chassisnummer",
        "co2": "CO2-uitstoot", "equip": "Uitrusting & Opmerkingen",
        "Inkl. Moms": "Incl. BTW", "Ekskl. Moms": "Excl. BTW", "Momsfri": "BTW Vrij", "Papegøje": "Papegaaienplaten (DK)",
        "Uden Afgift": "Excl. Belasting", "Med Afgift": "Incl. Belasting", "Forholdsmæssig": "Proportionele Belasting",
        "inkl. moms": "Incl. BTW", "ekskl. moms": "Excl. BTW", "uden afgift": "Excl. Belasting", "med afgift": "Incl. Belasting",
        "Manuel": "Handgeschakeld", "Automatgear": "Automaat", "Automatisk": "Automaat",
        "Benzin": "Benzine", "Diesel": "Diesel", "Hybrid": "Hybride", "El": "Elektrisch", "Plugin hybrid": "Plugin Hybride"
    }
}

# ==========================================
# ⚙️ INDSTILLINGER (WHATSAPP NUMMER)
# ==========================================
WHATSAPP_NUMBER = "4561438202" 

col_lang, _ = st.columns([1, 5])
lang = col_lang.selectbox("🌐 Language", ["English", "Deutsch", "Nederlands"])
if lang == "English": l = "en"
elif lang == "Deutsch": l = "de"
else: l = "nl"
t = translations[l]

# ==========================================
# 🛒 SESSION STATE (PAKKEKØB / KURV)
# ==========================================
if 'cart_exp' not in st.session_state:
    st.session_state['cart_exp'] = {}

# ==========================================
# 📦 SIDEMENU (DIN PAKKE)
# ==========================================
with st.sidebar:
    st.header(t["pkg_title"])
    if not st.session_state['cart_exp']:
        st.info(t["pkg_info"])
    else:
        total_list_price = 0
        total_bid_price = 0
        cart_text_lines = []
        
        st.write(t["pkg_your_bids"])
        for key, car in st.session_state['cart_exp'].items():
            total_list_price += car['price_int']
            current_bid = car.get('bid_price', car['price_int'])
            
            listepris_str = f"€ {car['price_int']:,}".replace(',', '.')
            new_bid = st.number_input(
                f"{car['title']} ({t['pkg_list_price']}: {listepris_str})",
                min_value=0,
                value=int(current_bid),
                step=100,
                key=f"bid_{key}"
            )
            
            st.session_state['cart_exp'][key]['bid_price'] = new_bid
            total_bid_price += new_bid
            
            bid_str = f"€ {new_bid:,}".replace(',', '.')
            cart_text_lines.append(f"- {car['title']} (VIN: {car['vin']}) -> Bid: {bid_str}")
            
        st.write("---")
        st.write(f"{t['pkg_total_list']} € {total_list_price:,}".replace(',', '.'))
        st.write(t["pkg_total_bid"])
        st.markdown(f"<h3 style='color: #2e7b32; margin-top:-10px;'>€ {total_bid_price:,}</h3>".replace(',', '.'), unsafe_allow_html=True)
        
        st.write("---")
        cars_str = "\n".join(cart_text_lines)
        total_bid_str = f"{total_bid_price:,}".replace(',', '.')
        
        mail_body = t["pkg_mail_body"].format(count=len(st.session_state['cart_exp']), cars=cars_str, total=total_bid_str)
        
        mail_link = f"mailto:matsc@maulbiler.dk,brmau@maulbiler.dk?subject=Offer on {len(st.session_state['cart_exp'])} cars&body={urllib.parse.quote(mail_body)}"
        wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(mail_body)}"
        
        st.markdown(f"<a href='{mail_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 10px; cursor: pointer; font-size: 14px; font-weight: bold; margin-bottom: 8px;'>{t['pkg_send_mail']}</button></a>", unsafe_allow_html=True)
        st.markdown(f"<a href='{wa_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #25D366; color: white; border: none; padding: 10px; cursor: pointer; font-size: 14px; font-weight: bold; color: white; margin-bottom: 20px;'>{t['pkg_send_wa']}</button></a>", unsafe_allow_html=True)
        
        if st.button(t["pkg_clear"], use_container_width=True):
            st.session_state['cart_exp'] = {}
            st.rerun()

st.title(t["title"])
st.write(t["subtitle"])

def translate_term(term_str, lang_dict):
    term_clean = str(term_str).strip()
    if term_clean in lang_dict:
        return lang_dict[term_clean]
    elif term_clean.lower() in lang_dict:
        return lang_dict[term_clean.lower()]
    return term_clean

@st.cache_data(ttl=60)
def load_b2b_data():
    sheet_id = "1Tx8pe8tgo0qpoiTcrTo6kbVZwkx5_uMYaoeYf3mJP6M" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try: return pd.read_csv(url)
    except: return None

# --- BILLEDE & DATA FREMVISER (POP-UP) ---
@st.dialog(t["view"], width="large")
def show_car_details(row, lang_dict):
    st.markdown(f"## {row.get('Mærke', '')} {row.get('Model', '')}")
    st.markdown(f"#### {row.get('Variant', '')}")
    st.write("")
    
    aarstal = str(row.get('Årgang', '-'))[:4]
    km_str = str(row.get('Odometer', '-'))
    
    try: 
        p_str = str(row.get('Pris euro', '0')).strip()
        if p_str.endswith('.0'): p_str = p_str[:-2]
        p_clean = "".join(filter(str.isdigit, p_str))
        pris_int = int(p_clean) if p_clean else 0
    except: 
        pris_int = 0
        
    pris_display = f"€ {pris_int:,}".replace(',', '.') if pris_int > 0 else "Make offer"

    m1, m2, m3 = st.columns(3)
    m1.metric(lang_dict["year"], aarstal)
    m2.metric(lang_dict["odometer"], km_str)
    m3.metric(lang_dict["price"], pris_display)
    
    st.write("---")
    
    tab1, tab2 = st.tabs(["📸 Photos", lang_dict['tech_data']])
    
    with tab1:
        img_string = str(row.get('Billede URL', ''))
        images = [url.strip() for url in img_string.split(',')] if img_string and img_string != 'nan' else []
        if images:
            for img in images:
                if img.startswith('http'):
                    st.image(img, use_container_width=True)
                    st.write("---")
        else:
            st.info("No images available.")
            
    with tab2: # TEKNISK DATA
        c1, c2 = st.columns(2)
        c1.write(f"**Make:** {row.get('Mærke', '-')}")
        c1.write(f"**Model:** {row.get('Model', '-')}")
        c1.write(f"**Variant:** {row.get('Variant', '-')}")
        
        disp_gear = translate_term(row.get('Gearkasse', '-'), lang_dict)
        disp_fuel = translate_term(row.get('Drivmiddel', '-'), lang_dict)
        c1.write(f"**{lang_dict['gearbox']}:** {disp_gear}")
        c1.write(f"**{lang_dict['fuel']}:** {disp_fuel}")
        c1.write(f"**{lang_dict['paint_areas']}:** {row.get('Antal lakfelter', '-')}")
        
        c2.write(f"**EURO norm:** {row.get('EURO norm', '-')}")
        c2.write(f"**{lang_dict['co2']}:** {row.get('CO2-udslip', '-')}")
        c2.write(f"**{lang_dict['reg_nr']}:** {row.get('Reg. nr.', '-')}")
        c2.write(f"**{lang_dict['vin']}:** {row.get('Stelnummer', '-')}")
        c2.write(f"**{lang_dict['location']}:** {row.get('Lokation', '-')}")
        
        disp_moms = translate_term(row.get('Moms status', '-'), lang_dict)
        disp_tax = translate_term(row.get('Afgift status', '-'), lang_dict)
        
        c1.write("---")
        c2.write("---")
        c1.write(f"**VAT:** {disp_moms}")
        c2.write(f"**Tax:** {disp_tax}")
        
        st.write("---")
        st.write(f"**{lang_dict['equip']}:**")
        st.info(row.get('Udstyr/Bemærkninger', 'No remarks.'))
        
    st.write("---")
    
    vin = str(row.get('Stelnummer', 'Ukendt'))
    mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
    modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
    
    emne_koeb = urllib.parse.quote(f"{lang_dict['mail_sub']} {mærke_model} (VIN: {vin})")
    tekst_koeb = urllib.parse.quote(f"{lang_dict['mail_koeb_body']}{vin}")
    mail_link_koeb = f"mailto:{modtagere}?subject={emne_koeb}&body={tekst_koeb}"
    
    emne_byd = urllib.parse.quote(f"Offer: {mærke_model} (VIN: {vin})")
    tekst_byd = urllib.parse.quote(f"{lang_dict['mail_byd_body']}{vin}")
    mail_link_byd = f"mailto:{modtagere}?subject={emne_byd}&body={tekst_byd}"
    
    btn_col1, btn_col2 = st.columns(2)
    btn_col1.markdown(f"<a href='{mail_link_koeb}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 12px; cursor: pointer; font-size: 16px; font-weight: bold;'>{lang_dict['buy']}</button></a>", unsafe_allow_html=True)
    btn_col2.markdown(f"<a href='{mail_link_byd}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #555555; color: white; border: none; padding: 12px; cursor: pointer; font-size: 16px; font-weight: bold;'>{lang_dict['bid']}</button></a>", unsafe_allow_html=True)

# --- HOVEDPROGRAM ---
df_b2b = load_b2b_data()

if df_b2b is not None and not df_b2b.empty:
    
    status_cols = [c for c in df_b2b.columns if 'Status' in c and c not in ['Moms status', 'Afgift status', 'Status DK']]
    if status_cols:
        active_col = status_cols[-1]
        df_b2b = df_b2b[df_b2b[active_col].astype(str).str.strip().str.lower() == 'aktiv']
    
    if df_b2b.empty:
        st.info(t["no_cars"])
    else:
        df_b2b['Sort_Price'] = pd.to_numeric(df_b2b['Pris euro'].astype(str).str.replace(r'\.0$', '', regex=True).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        df_b2b['Sort_Year'] = pd.to_numeric(df_b2b['Årgang'].astype(str).str[:4], errors='coerce').fillna(0)
        df_b2b['Sort_Km'] = pd.to_numeric(df_b2b['Odometer'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(9999999)

        c_search, c_moms, c_afgift, c_sort = st.columns(4)
        
        search_q = c_search.text_input(t["search"])
        
        moms_opts = [t["all"]] + list(df_b2b['Moms status'].dropna().unique()) if 'Moms status' in df_b2b.columns else [t["all"]]
        moms_q = c_moms.selectbox(t["vat"], moms_opts)
        
        afgift_opts = [t["all"]] + list(df_b2b['Afgift status'].dropna().unique()) if 'Afgift status' in df_b2b.columns else [t["all"]]
        afgift_q = c_afgift.selectbox(t["tax"], afgift_opts)
        
        sort_opts_map = {
            t["sort_default"]: "default",
            t["sort_price_asc"]: "price_asc",
            t["sort_price_desc"]: "price_desc",
            t["sort_year_desc"]: "year_desc",
            t["sort_km_asc"]: "km_asc"
        }
        sort_q_label = c_sort.selectbox(t["sort"], list(sort_opts_map.keys()))
        sort_q = sort_opts_map[sort_q_label]

        if search_q: df_b2b = df_b2b[df_b2b.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
        if moms_q != t["all"]: df_b2b = df_b2b[df_b2b['Moms status'] == moms_q]
        if afgift_q != t["all"]: df_b2b = df_b2b[df_b2b['Afgift status'] == afgift_q]
        
        if sort_q == "price_asc": df_b2b = df_b2b.sort_values('Sort_Price', ascending=True)
        elif sort_q == "price_desc": df_b2b = df_b2b.sort_values('Sort_Price', ascending=False)
        elif sort_q == "year_desc": df_b2b = df_b2b.sort_values('Sort_Year', ascending=False)
        elif sort_q == "km_asc": df_b2b = df_b2b.sort_values('Sort_Km', ascending=True)

        st.write("---")
        
        cols_per_row = 3
        for i in range(0, len(df_b2b), cols_per_row):
            cols = st.columns(cols_per_row)
            chunk = df_b2b.iloc[i:i+cols_per_row]
            
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    with st.container(border=True):
                        img_string = str(row.get('Billede URL', ''))
                        first_img = img_string.split(',')[0].strip() if img_string and img_string != 'nan' else ''
                        if pd.notna(first_img) and first_img.startswith('http'): 
                            st.image(first_img, use_container_width=True)
                        else: 
                            st.image("https://via.placeholder.com/400x250?text=No+image", use_container_width=True)
                        
                        st.markdown(f"### {row.get('Mærke', '')} {row.get('Model', '')}")
                        st.markdown(f"*{row.get('Variant', '')}*")
                        st.write("")
                        
                        aarstal = str(row.get('Årgang', '-'))[:4]
                        km_str = str(row.get('Odometer', '-'))
                        
                        disp_gear = translate_term(row.get('Gearkasse', '-'), t)
                        disp_fuel = translate_term(row.get('Drivmiddel', '-'), t)
                        
                        st.markdown(f"📅 **{aarstal}** &nbsp; | &nbsp; 🛣️ **{km_str}** <br> 🕹️ **{disp_gear}** &nbsp; | &nbsp; ⛽ **{disp_fuel}**", unsafe_allow_html=True)
                        
                        disp_moms = translate_term(row.get('Moms status', '-'), t)
                        disp_tax = translate_term(row.get('Afgift status', '-'), t)
                        st.markdown(f"🏷️ {disp_moms} &nbsp; | &nbsp; ⚖️ {disp_tax}")
                        
                        pris_int = row.get('Sort_Price', 0)
                        st.write("---")
                        if pris_int > 0: 
                            st.markdown(f"<h2 style='text-align: center; color: #2e7b32; font-weight: bold;'>€ {int(pris_int):,}</h2>".replace(',', '.'), unsafe_allow_html=True)
                        else: 
                            st.markdown(f"<h2 style='text-align: center;'>Make offer</h2>", unsafe_allow_html=True)
                        
                        if st.button(t["view"], key=f"view_{row.name}", use_container_width=True): 
                            show_car_details(row, t)
                        
                        vin = str(row.get('Stelnummer', 'Ukendt'))
                        mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
                        modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
                        
                        emne_koeb = urllib.parse.quote(f"{t['mail_sub']} {mærke_model} (VIN: {vin})")
                        tekst_koeb = urllib.parse.quote(f"{t['mail_koeb_body']}{vin}")
                        mail_link_koeb = f"mailto:{modtagere}?subject={emne_koeb}&body={tekst_koeb}"
                        
                        emne_byd = urllib.parse.quote(f"Offer: {mærke_model} (VIN: {vin})")
                        tekst_byd = urllib.parse.quote(f"{t['mail_byd_body']}{vin}")
                        mail_link_byd = f"mailto:{modtagere}?subject={emne_byd}&body={tekst_byd}"
                        
                        c_btn1, c_btn2 = st.columns(2)
                        c_btn1.markdown(f"<a href='{mail_link_koeb}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 6px; cursor: pointer; font-size: 14px; font-weight: bold;'>{t['buy']}</button></a>", unsafe_allow_html=True)
                        c_btn2.markdown(f"<a href='{mail_link_byd}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #555555; color: white; border: none; padding: 6px; cursor: pointer; font-size: 14px; font-weight: bold;'>{t['bid']}</button></a>", unsafe_allow_html=True)
                        
                        st.write("")
                        vin_key = vin if vin != 'Ukendt' else str(row.name)
                        if vin_key in st.session_state['cart_exp']:
                            if st.button(t["pkg_rm"], key=f"rm_{row.name}", use_container_width=True):
                                del st.session_state['cart_exp'][vin_key]
                                st.rerun()
                        else:
                            if st.button(t["pkg_add"], key=f"add_{row.name}", use_container_width=True):
                                st.session_state['cart_exp'][vin_key] = {
                                    'title': mærke_model,
                                    'price_int': int(pris_int),
                                    'vin': vin,
                                    'bid_price': int(pris_int)
                                }
                                st.rerun()

else:
    st.info(t["no_cars"])
