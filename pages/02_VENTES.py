import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns   
from matplotlib import pyplot as plt

st.set_page_config(page_title="VENTES", page_icon="💲", layout="wide")
st.markdown(
                """
                <style>
                /* Supprime la marge du haut du container principal */
                .block-container {
                    padding-top: 2rem;
                    padding-bottom: 1rem;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

st.sidebar.title("Téléchargement du fichier excel")
file_ventes = st.sidebar.file_uploader("Télécharger un fichier exel", type=["xlsx"])
if file_ventes:
    st.session_state['df_org_ventes'] = pd.read_excel(file_ventes)
    st.sidebar.success("Fichier chargé avec succès !")

# --- Vérifier si le DataFrame existe ---
if 'df_org_ventes' in st.session_state:
    df_org = st.session_state['df_org_ventes']
    df = df_org.copy()

        # --- Filtres pour Ventes ---
    col_ville, col_site, col_enseigne, col_date = st.columns(4)

    # --- Filtres pour Ventes ---
    col_ville, col_site, col_enseigne, col_date = st.columns(4)

    # --- Filtre Ville ---
    villes = ["Tout"] + sorted(df['VILLE'].dropna().unique())
    selected_ville = col_ville.selectbox("Ville", options=villes, index=0)

    # --- Filtre Site dépendant de la ville ---
    if selected_ville != "Tout":
        sites = ["Tout"] + sorted(df[df['VILLE'] == selected_ville]['Site'].dropna().unique())
    else:
        sites = ["Tout"] + sorted(df['Site'].dropna().unique())
    selected_site = col_site.selectbox("Site", options=sites, index=0)

    # --- Filtre Enseigne dépendant de la ville ---
    if selected_ville != "Tout":
        enseignes = ["Tout"] + sorted(df[df['VILLE'] == selected_ville]['Enseigne'].dropna().unique())
    else:
        enseignes = ["Tout"] + sorted(df['Enseigne'].dropna().unique())
    selected_enseigne = col_enseigne.selectbox("Enseigne", options=enseignes, index=0)

    # --- Filtre Date ---
    dates_dispo = ["Tout"] + sorted(df['Date de début'].dropna().dt.date.unique())
    selected_date = col_date.selectbox("Date", options=dates_dispo, index=0)

    # --- Appliquer les filtres ---
    df_filtered = df.copy()
    if selected_ville != "Tout":
        df_filtered = df_filtered[df_filtered['VILLE'] == selected_ville]
    if selected_site != "Tout":
        df_filtered = df_filtered[df_filtered['Site'] == selected_site]
    if selected_enseigne != "Tout":
        df_filtered = df_filtered[df_filtered['Enseigne'] == selected_enseigne]
    if selected_date != "Tout":
        df_filtered = df_filtered[df_filtered['Date de début'].dt.date == selected_date]


    analyse1 ,analyse2 = st.tabs(["Analyse des ventes", "MAP"])
    with analyse1:
        col1, col2, col3 = st.columns(3)
        with col1:
            produit_top = (df_filtered.groupby('Libellé article')['Quantité'].sum().reset_index().sort_values(by='Quantité', ascending=False).iloc[0])
            st.metric("Produit le plus vendu", produit_top['Libellé article'], f"{int(produit_top['Quantité']):,} unités")
        
        with col2:
            total_ventes = df_filtered['Quantité'].sum()
            st.metric("Total des ventes", f"{int(total_ventes):,} unités")

        with col3:
            moyenne_vente = df_filtered['Quantité'].mean()
            st.metric("Vente moyenne par produit", f"{moyenne_vente:.2f} unités")
        
        st.markdown("---")

        col3, col4 = st.columns(2)
        with col3:
            st.markdown("<h4 style='text-align: center;'>TOP 10 Sites avec les plus de Ventes</h4>", unsafe_allow_html=True)
            top10_sites = (df_filtered.groupby('Site')['Quantité'].sum().reset_index().sort_values(by='Quantité', ascending=False).head(10))
            # Création du graphique
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=(8,3))
            sns.barplot(
                data=top10_sites,
                x='Quantité',
                y='Site',
                palette="viridis",
                ax=ax
            )

            # Habillage
            ax.set_xlabel("Quantité vendue")
            ax.set_ylabel("Site")
            st.pyplot(fig)

        with col4:
            st.markdown("<h4 style='text-align: center;'>Evolution des ventes par mois</h4>", unsafe_allow_html=True)
            df_date = df_filtered.groupby('Date de début')['Quantité'].sum().reset_index()
            fig, ax = plt.subplots(figsize=(12,3))
            sns.lineplot(
                data=df_date,
                x='Date de début',
                y='Quantité',
                marker='o',
                color="#1f77b4",
                ax=ax
            )
            ax.set_xlabel("Date")
            ax.set_ylabel("Quantité vendue")
            ax.tick_params(axis='x', rotation=45)
            st.pyplot(fig)
    
    with analyse2:
            col_left, col_right = st.columns([1,1])
            with col_left:
                st.markdown("<h4 style='text-align: center;'>repartition des sites</h4>", unsafe_allow_html=True)
                coord_villes = {
                'RABAT': (34.020882, -6.841650),
                'CASABLANCA': (33.573110, -7.589843),
                'MARRAKECH': (31.6295, -7.9811),
                'AGADIR': (30.4278, -9.5981),
                'TANGER': (35.7595, -5.83395),
                'FES': (34.0346, -5.0003),
                'MOHAMMEDIA': (33.6781, -7.4169),
                'TETOUAN': (35.5761, -5.3683),
                'MEKNES': (33.8935, -5.5473),
                'SAFI': (32.2960, -9.2339),
                'KENITRA': (34.2617, -6.5803),
                'OUJDA': (34.6826, -1.9113),
                'NADOR': (35.1681, -2.9331),
                'KHOURIBGA': (32.8844, -6.9062),
                'BENI MELLAL': (32.3370, -6.3493),
                'EL KELAA SRAGHNA': (32.0572, -7.3203),
                'SALE': (34.0308, -6.8130),
                'EL HOCEIMA': (35.2519, -3.9380),
                'FKIH BEN SALEH': (32.1333, -6.9333),
                'TAZA': (34.2104, -4.0203),
                'BERKANE': (34.9740, -2.3210),
                'SIDI SLIMANE': (34.2167, -6.2000),
                'EL JADIDA': (33.2489, -8.4960),
                'INEZGANE': (30.4034, -9.5987),
                'LARACHE': (35.1685, -6.1609),
                'GUELMIM': (28.9875, -10.0566),
                'BOUSKOURA': (33.5230, -7.5510),
                'LAAYOUNE': (27.1213, -13.2034),
                'BEN GUERIR': (32.3141, -7.9853),
                'SAIDIA': (35.1500, -2.5333)
            }

                    # Ajouter Latitude et Longitude
                df_filtered['lat'] = df_filtered['VILLE'].map(lambda x: coord_villes.get(x, (None, None))[0])
                df_filtered['lon'] = df_filtered['VILLE'].map(lambda x: coord_villes.get(x, (None, None))[1])

                # Filtrer seulement les lignes avec lat/lon valides
                df_map = df_filtered.dropna(subset=['lat', 'lon'])

                # Afficher la carte
                st.map(df_map[['lat', 'lon']])

            with col_right:
                st.markdown("<h4 style='text-align: center;'>Ventes par ville</h4>", unsafe_allow_html=True)
                df_villes = df_filtered.groupby('VILLE')['Quantité'].sum().reset_index().sort_values(by='Quantité', ascending=False)
                # Créer le graphique
                fig, ax = plt.subplots(figsize=(8,6))
                sns.barplot(
                    x='Quantité',
                    y='VILLE',
                    data=df_villes,
                    palette="viridis",
                    ax=ax
                )

                # Habillage
                ax.set_xlabel("Quantité vendue")
                ax.set_ylabel("Ville")
                ax.set_title("Ventes par ville (Top ou toutes les villes)")

                # Afficher dans Streamlit
                st.pyplot(fig)





