import streamlit as st
import pandas as pd

st.set_page_config(page_title="B2B Vehicles", layout="wide", page_icon="🚘")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

translations = {
    "en": {
        "title": "🚘 Dealer Portal (B2B Vehicles)",
        "subtitle": "Welcome to our B2B portal. Here you will find our current vehicles ready for export or trade.",
        "search": "🔍 Search make/model",
        "vat": "🏷️ VAT",
        "tax": "⚖️ Tax",
        "all": "All",
        "buy": "🛒 Buy now",
        "view": "📸 View details",
        "no_cars": "There are currently no active vehicles for sale.",
        "tech_data": "⚙️ Technical Data",
        "mail_sub": "Purchase of",
        "mail_body": "Hi Mathias and Brian,%0D%0A%0D%0AI would like to purchase the vehicle with VIN:"
    },
    "de": {
        "title": "🚘 Händler-Portal (B2B Fahrzeuge)",
        "subtitle": "Willkommen in unserem B2B-Portal. Hier finden Sie unsere aktuellen Fahrzeuge für den Export oder Handel.",
        "search": "🔍 Marke/Modell suchen",
        "vat": "🏷️ MwSt",
        "tax": "⚖️ Steuer",
        "all": "Alle",
        "buy": "🛒 Jetzt kaufen",
        "view": "📸 Details ansehen",
        "no_cars": "Derzeit stehen keine aktiven Fahrzeuge zum Verkauf.",
        "tech_data": "⚙️ Technische Daten",
        "mail_sub": "Kauf von",
        "mail_body": "Hallo Mathias und Brian,%0D%0A%0D%0Aich möchte das Fahrzeug kaufen mit der FIN:"
    },
    "nl": {
        "title": "🚘 Dealerportaal (B2B Voertuigen)",
        "subtitle": "Welkom op ons B2B portaal. Hier vindt u onze actuele voertuigen klaar voor export of handel.",
        "search": "🔍 Zoek merk/model",
        "vat": "🏷️ BTW",
        "tax": "⚖️ Belasting",
        "all": "Alle",
        "buy": "🛒 Nu kopen",
        "view": "📸 Bekijk details",
        "no_cars": "Er staan momenteel geen actieve voertuigen te koop.",
        "tech_data": "⚙️ Technische Gegevens",
        "mail_sub": "Aankoop van",
        "mail_body": "Hallo Mathias en Brian,%0D%0A%0D%0AIk wil graag het voertuig kopen met chassisnummer:"
    }
}

col_lang, _ = st.columns([1, 5])
lang = col_lang.selectbox("🌐 Language", ["English", "Deutsch", "Nederlands"])
if lang == "English": l = "en"
elif lang == "Deutsch": l = "de"
else: l = "nl"
t = translations[l]

st.title(t["title"])
st.write(t["subtitle"])

@st.cache_data(ttl=60)
def load_b2b_data():
    sheet_id = "1Tx8pe8tgo0qpoiTcrTo6kbVZwkx5_uMYaoeYf3mJP6M" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try: return pd.read_csv(url)
    except: return None

# --- BILLEDE & DATA FREMVISER (POP-UP) ---
@st.dialog(t["view"], width="large")
def show_car_details(row, lang_dict):
    st.markdown(f"## {row.get('Mærke', '')} {row.get('Model', '')} {row.get('Variant', '')}")
    
    try: pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
    except: pris_int = 0
    if pris_int > 0: st.markdown(f"### € {pris_int:,}".replace(',', '.'))
    
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
        c1.write(f"**1st reg. date:** {row.get('Årgang', '-')}")
        c1.write(f"**Gearbox:** {row.get('Gearkasse', '-')}")
        c1.write(f"**Odometer:** {row.get('Odometer', '-')}")
        c1.write(f"**Paint areas (Lakfelter):** {row.get('Antal lakfelter', '-')}")
        
        c2.write(f"**EURO norm:** {row.get('EURO norm', '-')}")
        c2.write(f"**CO2:** {row.get('CO2-udslip', '-')}")
        c2.write(f"**Reg. nr.:** {row.get('Reg. nr.', '-')}")
        c2.write(f"**VIN:** {row.get('Stelnummer', '-')}")
        c2.write(f"**Location:** {row.get('Lokation', '-')}")
        c2.write(f"**VAT:** {row.get('Moms status', '-')}")
        c2.write(f"**Tax:** {row.get('Afgift status', '-')}")
        
        st.write("---")
        st.write("**Equipment & Remarks:**")
        st.info(row.get('Udstyr/Bemærkninger', 'No remarks.'))
        
    st.write("---")
    vin = str(row.get('Stelnummer', 'Ukendt'))
    mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
    modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
    mail_link = f"mailto:{modtagere}?subject={lang_dict['mail_sub']} {mærke_model} (VIN: {vin})&body={lang_dict['mail_body']} {vin}"
    
    st.markdown(f"<a href='{mail_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 12px; cursor: pointer; font-size: 16px; font-weight: bold;'>{lang_dict['buy']}</button></a>", unsafe_allow_html=True)

# --- HOVEDPROGRAM ---
df_b2b = load_b2b_data()

if df_b2b is not None and not df_b2b.empty:
    if 'Status' in df_b2b.columns:
        df_b2b = df_b2b[df_b2b['Status'].astype(str).str.strip().str.lower() == 'aktiv']
    
    if df_b2b.empty:
        st.info(t["no_cars"])
    else:
        c_search, c_moms, c_afgift = st.columns(3)
        search_q = c_search.text_input(t["search"])
        
        moms_opts = [t["all"]] + list(df_b2b['Moms status'].dropna().unique()) if 'Moms status' in df_b2b.columns else [t["all"]]
        moms_q = c_moms.selectbox(t["vat"], moms_opts)
        
        afgift_opts = [t["all"]] + list(df_b2b['Afgift status'].dropna().unique()) if 'Afgift status' in df_b2b.columns else [t["all"]]
        afgift_q = c_afgift.selectbox(t["tax"], afgift_opts)

        if search_q: df_b2b = df_b2b[df_b2b.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
        if moms_q != t["all"]: df_b2b = df_b2b[df_b2b['Moms status'] == moms_q]
        if afgift_q != t["all"]: df_b2b = df_b2b[df_b2b['Afgift status'] == afgift_q]

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
                        if pd.notna(first_img) and first_img.startswith('http'): st.image(first_img, use_container_width=True)
                        else: st.image("https://via.placeholder.com/400x250?text=No+image", use_container_width=True)
                        
                        st.markdown(f"#### {row.get('Mærke', '')} {row.get('Model', '')}")
                        st.markdown(f"*{row.get('Variant', '')}*")
                        
                        aarstal = str(row.get('Årgang', '-'))[:4]
                        km_str = str(row.get('Odometer', '-'))
                        
                        st.markdown(f"📅 **{aarstal}** &nbsp;|&nbsp; 🛣️ **{km_str}**")
                        st.markdown(f"🏷️ {row.get('Moms status', '-')} &nbsp;|&nbsp; ⚖️ {row.get('Afgift status', '-')}")
                        
                        try: pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
                        except: pris_int = 0
                        
                        if pris_int > 0: st.markdown(f"### € {pris_int:,}".replace(',', '.'))
                        else: st.markdown(f"### {row.get('Pris', 'Make offer')}")
                        
                        btn_c1, btn_c2 = st.columns(2)
                        if btn_c1.button(t["view"], key=f"view_{row.name}"): show_car_details(row, t)
                        
                        vin = str(row.get('Stelnummer', 'Ukendt'))
                        mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
                        modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
                        mail_link = f"mailto:{modtagere}?subject={t['mail_sub']} {mærke_model} (VIN: {vin})&body={t['mail_body']} {vin}"
                        btn_c2.markdown(f"<a href='{mail_link}' target='_blank'><button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 6px; cursor: pointer; font-size: 14px; font-weight: bold;'>{t['buy']}</button></a>", unsafe_allow_html=True)
else:
    st.info(t["no_cars"])
