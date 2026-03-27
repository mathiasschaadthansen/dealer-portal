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
        "buy": "✉️ Email Us",
        "wa_buy": "💬 WhatsApp Us",
        "print": "🖨️ Print / PDF",
        "view": "📸 View details & photos",
        "no_cars": "There are currently no active vehicles for sale.",
        "tech_data": "⚙️ Technical Data",
        "mail_sub": "Purchase of",
        "mail_body": "Hi Mathias and Brian,\n\nI would like to purchase the vehicle with VIN: ",
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
        "paint_areas": "Paint areas",
        "location": "Location",
        "reg_nr": "Reg. nr.",
        "vin": "VIN",
        "co2": "CO2-emission",
        "equip": "Equipment & Remarks",
        # Status oversættelser
        "Inkl. Moms": "Incl. VAT", "Ekskl. Moms": "Excl. VAT", "Momsfri": "VAT Free", "Papegøje": "Parrot plates (DK)",
        "Uden Afgift": "Excl. Tax", "Med Afgift": "Incl. Tax", "Forholdsmæssig": "Proportional Tax",
        # Gearkasse
        "Manuel": "Manual", "Automatgear": "Automatic", "Automatisk": "Automatic"
    },
    "de": {
        "title": "🚘 Händler-Portal (B2B Fahrzeuge)",
        "subtitle": "Willkommen in unserem B2B-Portal. Hier finden Sie unsere aktuellen Fahrzeuge für den Export oder Handel.",
        "search": "🔍 Marke/Modell suchen", "vat": "🏷️ MwSt", "tax": "⚖️ Steuer", "sort": "🔽 Sortieren nach",
        "all": "Alle", "buy": "✉️ Email senden", "wa_buy": "💬 WhatsApp", "print": "🖨️ Drucken / PDF",
        "view": "📸 Details & Fotos", "no_cars": "Derzeit stehen keine aktiven Fahrzeuge zum Verkauf.",
        "tech_data": "⚙️ Technische Daten", "mail_sub": "Kauf von", "mail_body": "Hallo Mathias und Brian,\n\nich möchte das Fahrzeug kaufen mit der FIN: ",
        "sort_default": "Zuletzt hinzugefügt", "sort_price_asc": "Preis: Aufsteigend", "sort_price_desc": "Preis: Absteigend",
        "sort_year_desc": "Jahr: Neueste zuerst", "sort_km_asc": "Kilometer: Niedrigste zuerst",
        "year": "Jahr", "odometer": "Kilometerstand", "price": "Preis", "gearbox": "Getriebe",
        "paint_areas": "Lackierfelder", "location": "Standort", "reg_nr": "Kennzeichen", "vin": "FIN",
        "co2": "CO2-Ausstoß", "equip": "Ausstattung & Bemerkungen",
        "Inkl. Moms": "Inkl. MwSt", "Ekskl. Moms": "Exkl. MwSt", "Momsfri": "MwSt-Frei", "Papegøje": "Papageienschilder (DK)",
        "Uden Afgift": "Exkl. Steuer", "Med Afgift": "Inkl. Steuer", "Forholdsmæssig": "Verhältnismäßige Steuer",
        "Manuel": "Schaltgetriebe", "Automatgear": "Automatik", "Automatisk": "Automatik"
    },
    "nl": {
        "title": "🚘 Dealerportaal (B2B Voertuigen)",
        "subtitle": "Welkom op ons B2B portaal. Hier vindt u onze actuele voertuigen klaar voor export of handel.",
        "search": "🔍 Zoek merk/model", "vat": "🏷️ BTW", "tax": "⚖️ Belasting", "sort": "🔽 Sorteer op",
        "all": "Alle", "buy": "✉️ Email ons", "wa_buy": "💬 WhatsApp", "print": "🖨️ Print / PDF",
        "view": "📸 Bekijk details & foto's", "no_cars": "Er staan momenteel geen actieve voertuigen te koop.",
        "tech_data": "⚙️ Technische Gegevens", "mail_sub": "Aankoop van", "mail_body": "Hallo Mathias en Brian,\n\nIk wil graag het voertuig kopen met chassisnummer: ",
        "sort_default": "Nieuwste eerst", "sort_price_asc": "Prijs: Laag naar Hoog", "sort_price_desc": "Prijs: Hoog naar Laag",
        "sort_year_desc": "Jaar: Nieuwste eerst", "sort_km_asc": "Kilometerstand: Laagste eerst",
        "year": "Jaar", "odometer": "Kilometerstand", "price": "Prijs", "gearbox": "Versnellingsbak",
        "paint_areas": "Spuitdelen", "location": "Locatie", "reg_nr": "Kenteken", "vin": "Chassisnummer",
        "co2": "CO2-uitstoot", "equip": "Uitrusting & Opmerkingen",
        "Inkl. Moms": "Incl. BTW", "Ekskl. Moms": "Excl. BTW", "Momsfri": "BTW Vrij", "Papegøje": "Papegaaienplaten (DK)",
        "Uden Afgift": "Excl. Belasting", "Med Afgift": "Incl. Belasting", "Forholdsmæssig": "Proportionele Belasting",
        "Manuel": "Handgeschakeld", "Automatgear": "Automaat", "Automatisk": "Automaat"
    }
}

# ==========================================
# ⚙️ INDSTILLINGER (WHATSAPP NUMMER)
# ==========================================
# Skriv jeres WhatsApp nummer her (Husk landekode, f.eks. 45 for Danmark. Ingen + eller mellemrum)
WHATSAPP_NUMBER = "4561438202" 

col_lang, _ = st.columns([1, 5])
lang = col_lang.selectbox("🌐 Language", ["English", "Deutsch", "Nederlands"])
if lang == "English": l = "en"
elif lang == "Deutsch": l = "de"
else: l = "nl"
t = translations[l]

st.title(t["title"])
st.write(t["subtitle"])

def translate_term(term_str, lang_dict):
    term_clean = str(term_str).strip()
    return lang_dict.get(term_clean, term_clean)

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
    try: pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
    except: pris_int = 0
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
        c1.write(f"**{lang_dict['gearbox']}:** {disp_gear}")
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
    
    # KNAPPER I POP-UP
    vin = str(row.get('Stelnummer', 'Ukendt'))
    mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
    
    # Email Link
    modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
    emne = urllib.parse.quote(f"{lang_dict['mail_sub']} {mærke_model} (VIN: {vin})")
    tekst = urllib.parse.quote(f"{lang_dict['mail_body']}{vin}")
    mail_link = f"mailto:{modtagere}?subject={emne}&body={tekst}"
    
    # WhatsApp Link
    wa_text = urllib.parse.quote(f"{lang_dict['mail_body']}{vin}")
    wa_link = f"https://wa.me/{WHATSAPP_NUMBER}?text={wa_text}"
    
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    
    btn_col1.markdown(f"<a href='{mail_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 10px; cursor: pointer; font-size: 15px; font-weight: bold;'>{lang_dict['buy']}</button></a>", unsafe_allow_html=True)
    btn_col2.markdown(f"<a href='{wa_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #25D366; color: white; border: none; padding: 10px; cursor: pointer; font-size: 15px; font-weight: bold; color: white;'>{lang_dict['wa_buy']}</button></a>", unsafe_allow_html=True)
    
    # Print Knap (Instruktion)
    if btn_col3.button(lang_dict['print'], use_container_width=True):
        st.info("⌨️ Tip: Tryk **CTRL + P** (eller **CMD + P** på Mac) for at gemme som PDF eller printe siden.")

# --- HOVEDPROGRAM ---
df_b2b = load_b2b_data()

if df_b2b is not None and not df_b2b.empty:
    if 'Status' in df_b2b.columns:
        df_b2b = df_b2b[df_b2b['Status'].astype(str).str.strip().str.lower() == 'aktiv']
    
    if df_b2b.empty:
        st.info(t["no_cars"])
    else:
        # FORBERED DATA TIL SORTERING
        df_b2b['Sort_Price'] = pd.to_numeric(df_b2b['Pris'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(0)
        df_b2b['Sort_Year'] = pd.to_numeric(df_b2b['Årgang'].astype(str).str[:4], errors='coerce').fillna(0)
        df_b2b['Sort_Km'] = pd.to_numeric(df_b2b['Odometer'].astype(str).str.replace(r'[^\d]', '', regex=True), errors='coerce').fillna(9999999)

        # TOP MENU: SØGNING OG FILTRERING
        c_search, c_moms, c_afgift, c_sort = st.columns(4)
        
        search_q = c_search.text_input(t["search"])
        
        moms_opts = [t["all"]] + list(df_b2b['Moms status'].dropna().unique()) if 'Moms status' in df_b2b.columns else [t["all"]]
        moms_q = c_moms.selectbox(t["vat"], moms_opts)
        
        afgift_opts = [t["all"]] + list(df_b2b['Afgift status'].dropna().unique()) if 'Afgift status' in df_b2b.columns else [t["all"]]
        afgift_q = c_afgift.selectbox(t["tax"], afgift_opts)
        
        # SORTERING
        sort_opts = [t["sort_default"], t["sort_price_asc"], t["sort_price_desc"], t["sort_year_desc"], t["sort_km_asc"]]
        sort_q = c_sort.selectbox(t["sort"], sort_opts)

        # Udfør Filtrering
        if search_q: df_b2b = df_b2b[df_b2b.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
        if moms_q != t["all"]: df_b2b = df_b2b[df_b2b['Moms status'] == moms_q]
        if afgift_q != t["all"]: df_b2b = df_b2b[df_b2b['Afgift status'] == afgift_q]
        
        # Udfør Sortering
        if sort_q == t["sort_price_asc"]: df_b2b = df_b2b.sort_values('Sort_Price', ascending=True)
        elif sort_q == t["sort_price_desc"]: df_b2b = df_b2b.sort_values('Sort_Price', ascending=False)
        elif sort_q == t["sort_year_desc"]: df_b2b = df_b2b.sort_values('Sort_Year', ascending=False)
        elif sort_q == t["sort_km_asc"]: df_b2b = df_b2b.sort_values('Sort_Km', ascending=True)

        st.write("---")
        
        # GRID OPSÆTNING
        cols_per_row = 3
        for i in range(0, len(df_b2b), cols_per_row):
            cols = st.columns(cols_per_row)
            chunk = df_b2b.iloc[i:i+cols_per_row]
            
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    with st.container(border=True):
                        # Coverbillede
                        img_string = str(row.get('Billede URL', ''))
                        first_img = img_string.split(',')[0].strip() if img_string and img_string != 'nan' else ''
                        if pd.notna(first_img) and first_img.startswith('http'): 
                            st.image(first_img, use_container_width=True)
                        else: 
                            st.image("https://via.placeholder.com/400x250?text=No+image", use_container_width=True)
                        
                        # Titel og Varianter
                        st.markdown(f"### {row.get('Mærke', '')} {row.get('Model', '')}")
                        st.markdown(f"*{row.get('Variant', '')}*")
                        st.write("")
                        
                        aarstal = str(row.get('Årgang', '-'))[:4]
                        km_str = str(row.get('Odometer', '-'))
                        
                        disp_gear = translate_term(row.get('Gearkasse', '-'), t)
                        
                        st.markdown(f"📅 **{aarstal}** &nbsp; | &nbsp; 🛣️ **{km_str}** &nbsp; | &nbsp; 🕹️ **{disp_gear}**")
                        
                        disp_moms = translate_term(row.get('Moms status', '-'), t)
                        disp_tax = translate_term(row.get('Afgift status', '-'), t)
                        st.markdown(f"🏷️ {disp_moms} &nbsp; | &nbsp; ⚖️ {disp_tax}")
                        
                        pris_int = row.get('Sort_Price', 0)
                        st.write("---")
                        if pris_int > 0: 
                            st.markdown(f"<h2 style='text-align: center; color: #2e7b32;'>€ {int(pris_int):,}</h2>".replace(',', '.'), unsafe_allow_html=True)
                        else: 
                            st.markdown(f"<h2 style='text-align: center;'>Make offer</h2>", unsafe_allow_html=True)
                        
                        # View Knap
                        if st.button(t["view"], key=f"view_{row.name}", use_container_width=True): 
                            show_car_details(row, t)
else:
    st.info(t["no_cars"])
