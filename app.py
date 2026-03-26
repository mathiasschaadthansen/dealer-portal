import streamlit as st
import pandas as pd

st.set_page_config(page_title="B2B Varelager", layout="wide", page_icon="🚘")

# Skjul Streamlits egen menu for at gøre den mere "hjemmeside-agtig"
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("🚘 Forhandler-Portal (B2B Varelager)")
st.write("Velkommen til vores B2B-portal. Her finder du vores aktuelle biler klar til handel.")

@st.cache_data(ttl=60)
def load_b2b_data():
    # Dit specifikke Google Sheet ID
    sheet_id = "1Tx8pe8tgo0qpoiTcrTo6kbVZwkx5_uMYaoeYf3mJP6M" 
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    try:
        return pd.read_csv(url)
    except Exception as e:
        return None

df_b2b = load_b2b_data()

if df_b2b is not None and not df_b2b.empty:
    if 'Status' in df_b2b.columns:
        # Filtrer kun biler der står som 'Aktiv'
        df_b2b = df_b2b[df_b2b['Status'].astype(str).str.strip().str.lower() == 'aktiv']
    
    if df_b2b.empty:
        st.info("Der er i øjeblikket ingen aktive biler til salg på B2B-portalen.")
    else:
        # Søge og filterfunktioner
        c_search, c_moms, c_afgift = st.columns(3)
        search_q = c_search.text_input("🔍 Søg efter mærke/model")
        
        moms_opts = ["Alle"] + list(df_b2b['Moms status'].dropna().unique()) if 'Moms status' in df_b2b.columns else ["Alle"]
        moms_q = c_moms.selectbox("🏷️ Moms", moms_opts)
        
        afgift_opts = ["Alle"] + list(df_b2b['Afgift status'].dropna().unique()) if 'Afgift status' in df_b2b.columns else ["Alle"]
        afgift_q = c_afgift.selectbox("⚖️ Afgift", afgift_opts)

        # Udfør filtrering
        if search_q:
            df_b2b = df_b2b[df_b2b.astype(str).apply(lambda x: x.str.contains(search_q, case=False)).any(axis=1)]
        if moms_q != "Alle":
            df_b2b = df_b2b[df_b2b['Moms status'] == moms_q]
        if afgift_q != "Alle":
            df_b2b = df_b2b[df_b2b['Afgift status'] == afgift_q]

        st.write("---")
        
        cols_per_row = 3
        for i in range(0, len(df_b2b), cols_per_row):
            cols = st.columns(cols_per_row)
            chunk = df_b2b.iloc[i:i+cols_per_row]
            
            for col, (_, row) in zip(cols, chunk.iterrows()):
                with col:
                    with st.container(border=True):
                        # Billede
                        img_url = row.get('Billede URL', '')
                        if pd.notna(img_url) and str(img_url).startswith('http'):
                            st.image(img_url, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/400x250?text=Intet+billede", use_container_width=True)
                        
                        # Info
                        st.markdown(f"#### {row.get('Mærke', '')} {row.get('Model', '')}")
                        st.markdown(f"*{row.get('Variant', '')}*")
                        
                        # Viser kun årstal (f.eks. "2017" i stedet for "2017-02-23")
                        aarstal = str(row.get('Årgang', '-'))[:4]
                        
                        st.markdown(f"📅 **{aarstal}** &nbsp;|&nbsp; 📍 **{row.get('Lokation', '-')}**")
                        st.markdown(f"🏷️ {row.get('Moms status', '-')} &nbsp;|&nbsp; ⚖️ {row.get('Afgift status', '-')}")
                        
                        # Pris opsætning (EUR)
                        try:
                            pris_int = int(float(str(row.get('Pris', '0')).replace('€', '').replace('.', '').replace(',', '').strip()))
                            st.markdown(f"### € {pris_int:,}".replace(',', '.'))
                        except:
                            st.markdown(f"### {row.get('Pris', 'Bud ønskes')}")
                        
                        # Knap med Email Logik til begge modtagere
                        vin = str(row.get('Stelnummer', 'Ukendt'))
                        mærke_model = f"{row.get('Mærke', '')} {row.get('Model', '')}"
                        modtagere = "matsc@maulbiler.dk,brmau@maulbiler.dk"
                        emne = f"Køb af {mærke_model} (VIN: {vin})"
                        tekst = f"Hej Mathias og Brian,%0D%0A%0D%0AJeg vil gerne købe bilen med stelnummer: {vin}"
                        
                        mail_link = f"mailto:{modtagere}?subject={emne}&body={tekst}"
                        
                        # HTML for "Buy now" knappen
                        st.markdown(f"""
                        <a href='{mail_link}' target='_blank'>
                            <button style='width: 100%; border-radius: 5px; background-color: #2e7b32; color: white; border: none; padding: 12px; cursor: pointer; font-size: 16px; font-weight: bold;'>
                                🛒 Buy now
                            </button>
                        </a>
                        """, unsafe_allow_html=True)
else:
    st.info("Der er i øjeblikket ingen aktive biler til salg på B2B-portalen.")
