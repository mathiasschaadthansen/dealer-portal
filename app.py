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

# --- ORDBOG TIL SPROG ---
translations = {
    "en": {
        "title": "🚘 Dealer Portal (B2B Vehicles)",
        "subtitle": "Welcome to our B2B portal. Here you will find our current vehicles ready for export or trade.",
        "search": "🔍 Search make/model",
        "vat": "🏷️ VAT",
        "tax": "⚖️ Tax",
        "all": "All",
        "buy": "🛒 Buy now",
        "view": "📸 View details & pictures",
        "no_cars": "There are currently no active vehicles for sale.",
        "vin": "VIN",
        "loc": "Location",
        "year": "Year",
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
        "view": "📸 Details & Bilder ansehen",
        "no_cars": "Derzeit stehen keine aktiven Fahrzeuge zum Verkauf.",
        "vin": "FIN",
        "loc": "Standort",
        "year": "Jahr",
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
        "view": "📸 Bekijk details & foto's",
        "no_cars": "Er staan momenteel geen actieve voertuigen te koop.",
        "vin": "Chassisnummer",
        "loc": "Locatie",
        "year": "Jaar",
        "mail_sub": "Aankoop van",
        "mail_body": "Hallo Mathias en Brian,%0D%0A%0D%0AIk wil graag het voertuig kopen met chassisnummer:"
    }
}

# --- SPROGVÆLGER I TOPPEN ---
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
    try:
        return pd.read_csv(url)
    except Exception as e:
        return None

# --- BILLEDE FREMVISER (POP-UP) ---
@st.dialog(t["view"])
def show_car_details(row, lang_dict):
    img_string = str(row.get('Billede URL', ''))
    
    # Splitter billed-linket op, hvis der er flere (adskilt af komma)
    images = [url.strip() for url in img_string.split(',')] if img_string and img_string != 'nan' else []
    
    if images:
        if len(images) > 1:
            st.write(f"📸 Viser {len(images)} billeder:")
            # Viser billederne under hinanden i pop-uppen
            for img in images:
                if img.startswith('http'):
                    st.image(img, use_container_width=True)
                    st.write("---")
        else:
            if images[0].startswith('http'):
                st.image(images[0], use_container_width=True)
    else:
        st.info("Intet billede")
        
    st.markdown(f"### {row.get('Mærke', '')} {row.get('Model', '')} {row.get('Variant', '')}")
    st.write(f"**{lang_dict['vin']}:** {row.get('Stelnummer', 'Ukendt')}")
    st.write(f"**{lang_dict['loc']}:** {row.get('Lokation', '-')}")
    
    try:
        pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
        st.markdown(f"## € {pris_int:,}".replace(',', '.'))
    except:
        st.markdown(f"## {row.get('Pris', 'Bud ønskes')}")
        
    vin = str(row.get('Stelnummer', 'Ukendt'))
    mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
    modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
    emne = f"{lang_dict['mail_sub']} {mærke_model} (VIN: {vin})"
    tekst = f"{lang_dict['mail_body']} {vin}"
    mail_link = f"mailto:{modtagere}?subject={emne}&body={tekst}"
    
    st.markdown(f"""
    <a href='{mail_link}' target='_blank'>
        <button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 12px; cursor: pointer; font-size: 16px; font-weight: bold;'>
            {lang_dict['buy']}
        </button>
    </a>
    """, unsafe_allow_html=True)

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

        if search_q:
            df_b2b = df_b2b[df_b2b.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
        if moms_q != t["all"]:
            df_b2b = df_b2b[df_b2b['Moms status'] == moms_q]
        if afgift_q != t["all"]:
            df_b2b = df_b2b[df_b2b['Afgift status'] == afgift_q]

        st.write("---")
        
        cols_per_row = 3
        for i in range(0, len(df_b2b), cols_per_row):
            cols = st.columns(cols_per_row)
            chunk = df_b2b.iloc[i:i+cols_per_row]
            
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    with st.container(border=True):
                        # Billede (Viser kun det første på oversigten)
                        img_string = str(row.get('Billede URL', ''))
                        first_img = img_string.split(',')[0].strip() if img_string and img_string != 'nan' else ''
                        
                        if pd.notna(first_img) and first_img.startswith('http'):
                            st.image(first_img, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/400x250?text=No+image", use_container_width=True)
                        
                        st.markdown(f"#### {row.get('Mærke', '')} {row.get('Model', '')}")
                        st.markdown(f"*{row.get('Variant', '')}*")
                        
                        aarstal = str(row.get('Årgang', '-'))[:4]
                        
                        st.markdown(f"📅 **{aarstal}** &nbsp;|&nbsp; 📍 **{row.get('Lokation', '-')}**")
                        st.markdown(f"🏷️ {row.get('Moms status', '-')} &nbsp;|&nbsp; ⚖️ {row.get('Afgift status', '-')}")
                        
                        try:
                            pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
                            st.markdown(f"### € {pris_int:,}".replace(',', '.'))
                        except:
                            st.markdown(f"### {row.get('Pris', 'Make offer')}")
                        
                        # Knapperne
                        btn_c1, btn_c2 = st.columns(2)
                        
                        # "View" knap åbner pop-up funktionen
                        if btn_c1.button(t["view"], key=f"view_{row.name}"):
                            show_car_details(row, t)
                        
                        # Buy knap sender mail
                        vin = str(row.get('Stelnummer', 'Ukendt'))
                        mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
                        modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
                        emne = f"{t['mail_sub']} {mærke_model} (VIN: {vin})"
                        tekst = f"{t['mail_body']} {vin}"
                        mail_link = f"mailto:{modtagere}?subject={emne}&body={tekst}"
                        
                        btn_c2.markdown(f"""
                        <a href='{mail_link}' target='_blank'>
                            <button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 6px; cursor: pointer; font-size: 14px; font-weight: bold;'>
                                {t['buy']}
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
else:
    st.info(t["no_cars"])
