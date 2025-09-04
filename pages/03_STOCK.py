import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns   
from matplotlib import pyplot as plt

st.set_page_config(page_title="Stock", page_icon="📦", layout="wide")
st.markdown(
                """
                <style>
                /* Supprime la marge du haut du container principal */
                .block-container {
                    padding-top: 3rem;
                    padding-bottom: 1rem;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

st.sidebar.title("Téléchargement du fichier excel")
file_stock = st.sidebar.file_uploader("Télécharger un fichier exel", type=["xlsx"])
if file_stock:
    st.session_state['df_org'] = pd.read_excel(file_stock)
    st.sidebar.success("Fichier chargé avec succès !")

# --- Vérifier si le DataFrame existe ---
if 'df_org' in st.session_state:
    df_org = st.session_state['df_org']
    df = df_org.copy()
    
    site_ville = {
        "MM Agadir Talbojt": "Agadir",
        "MM AGADIR EL HOUDA": "Agadir",
        "MARJANE AGADIR FOUNTY": "Agadir",
        "MM AGADIR HAY MOHAMMADI": "Agadir",
        "MARJANE EL HOCEIMA": "Al Hoceima",
        "Marjane Market BENGRIR": "Bengrir",
        "Marjane Market beni Mellal Takadoum": "Beni Mellal",
        "MM BENI MELLAL": "Beni Mellal",
        "MARJANE BENI MELLAL": "Beni Mellal",
        "MM BENSLIMANE": "Benslimane",
        "MARJANE BERKANE": "Berkane",
        "MM BERRECHID": "Berrechid",
        "MARJANE BOUSKOURA": "Bouskoura",
        "MM BOUSKOURA BO VILLAGE 1": "Bouskoura",
        "MM.VILLE VERTE": "Bouskoura",
        "MM BOUZNIKA MANDARONA": "Bouznika",
        "MM CASA FOURAT": "Casablanca",
        "MM Sidi Maarouf O Village": "Casablanca",
        "MM CASA ALMAZ": "Casablanca",
        "MARJANE DERB SULTAN": "Casablanca",
        "MM AIN SEBAA MEKOUAR": "Casablanca",
        "MM PANORAMIQUE": "Casablanca",
        "MM. SIDI OTHMANE": "Casablanca",
        "MM CASA OULFA": "Casablanca",
        "MM. EMILE ZOLA": "Casablanca",
        "MM IBNOUTACHAFINE": "Casablanca",
        "MM. TWIN": "Casablanca",
        "MM ROCHE NOIRE": "Casablanca",
        "MM DAR BOUAAZA": "Casablanca",
        "MARJANE AIN SEBAA": "Casablanca",
        "MM LAMENAIS": "Casablanca",
        "MM DAR BOUAAZA CGI": "Casablanca",
        "MM.BEAUSEJOUR": "Casablanca",
        "MM HERMITAGE": "Casablanca",
        "MM CASA LAYMOUNE": "Casablanca",
        "MM QUARTIER LES HÔPITAUX": "Casablanca",
        "Marjane Market VERTINTA": "Casablanca",
        "MM. PAQUET": "Casablanca",
        "MM. 2 MARS": "Casablanca",
        "MM CASA PALMIER": "Casablanca",
        "MM. LIBERTE": "Casablanca",
        "MARJANE MARINA CASABLANCA": "Casablanca",
        "MARJANE IBN TACHFINE": "Casablanca",
        "MM AERIA MALL": "Casablanca",
        "MM TADDART": "Casablanca",
        "MARJANE SIDI OTHMAN": "Casablanca",
        "MM CIL": "Casablanca",
        "MARJANE HAY HASSANI": "Casablanca",
        "MARJANE MOROCCO MALL": "Casablanca",
        "MM INARA": "Casablanca",
        "MM CASA VAL FLEURI": "Casablanca",
        "MM.RYAD ANFA": "Casablanca",
        "Entrepot Sapino": "Casablanca",
        "MM. GHANDI": "Casablanca",
        "MM BERNOUSSI": "Casablanca",
        "MARJANE CALIFORNIE": "Casablanca",
        "Marjane Market CASA OASIS": "Casablanca",
        "MM ROMANA": "Casablanca",
        "MM. EL HAJEB": "El Hajeb",
        "MM EL JADIDA": "El Jadida",
        "MARJANE EL JADIDA": "El Jadida",
        "MARJANE EL KALAA SRAGHNA": "El Kelaa",
        "MM. ERRACHIDIA": "Errachidia",
        "MARJANE FQUIH BEN SALEH": "Fquih Ben Saleh",
        "MM. FES SEFROU": "Fès",
        "MM. FES SALAM": "Fès",
        "MM Fes Fontaine": "Fès",
        "MM Fes CDC": "Fès",
        "MARJANE FES II SAISS": "Fès",
        "MARJANE FES AGDAL": "Fès",
        "MARJANE GUELMIM": "Guelmim",
        "MARJANE INZEGANE": "Inzegane",
        "MARJANE KHOURIBGA": "Khouribga",
        "MM KHOURIBGA": "Khouribga",
        "MM KENITRA MAAMOURA": "Kénitra",
        "MM AHMED CHAOUQI": "Kénitra",
        "MM KENITRA": "Kénitra",
        "MARJANE KENITRA": "Kénitra",
        "Marjane LAAYOUNE": "Laayoune",
        "MARJANE LARACHE": "Larache",
        "MM.TARGA": "Marrakech",
        "MARJANE MARAKKECH MASSIRA": "Marrakech",
        "MM. GUELIZ": "Marrakech",
        "MM Marrakech SEMLALIA": "Marrakech",
        "MARJANE MARAKKECH MENARA": "Marrakech",
        "MM MARTIL": "Martil",
        "MARJANE MEKNES HAMRIA": "Meknès",
        "MARJANE MEKNES": "Meknès",
        "MM MEKNES HAMRIA": "Meknès",
        "MM MEKNES ZAITOUN": "Meknès",
        "MM. MIDELT": "Midelt",
        "MARJANE MOHAMMADIA": "Mohammedia",
        "MM MOHAMEDIA PARC": "Mohammedia",
        "MARJANE NADOR": "Nador",
        "MM. OUJDA MEDINA": "Oujda",
        "MM OUJDA": "Oujda",
        "MARJANE OUJDA": "Oujda",
        "MM Ouled Teima": "Oulad Teima",
        "MM RABAT MABELLA": "Rabat",
        "MM EL MENZEH MAJORELLE": "Rabat",
        "MM Rabat Océan 2": "Rabat",
        "MM RABAT CITY CENTER": "Rabat",
        "MM RABAT OCEAN": "Rabat",
        "MARJANE BOUREGREG": "Rabat",
        "MM ZAER": "Rabat",
        "MARJANE ARRIBAT CENTER": "Rabat",
        "MM RABAT CHAMPION": "Rabat",
        "MM. HAY RIAD": "Rabat",
        "MM DAR ESSALAM": "Rabat",
        "MARJANE HAY RIAD": "Rabat",
        "MARJANE SAAIDIA": "Saaidia",
        "MM SAFI 1": "Safi",
        "MARJANE SAFI": "Safi",
        "MM SALE ELJADIDA": "Salé",
        "MARJANE SALE": "Salé",
        "MARJANE SIDI SLIMANE": "Sidi Slimane",
        "MM Tanger MOUJAHIDINE": "Tanger",
        "MM TANGER": "Tanger",
        "MM TANGER TOROS": "Tanger",
        "MM TANGER CASTILLA": "Tanger",
        "MM TANGER IBERIA": "Tanger",
        "MM TANGER VAL FLEURI": "Tanger",
        "MM TANGER CITY CENTER": "Tanger",
        "MM TANGER BOULEVARD": "Tanger",
        "MARJANE TANGER II": "Tanger",
        "MARJANE TANGER": "Tanger",
        "MARJANE TAZA": "Taza",
        "MM TIFELT": "Tifelt",
        "MM. TEMARA": "Témara",
        "MM. HARHOURA": "Témara",
        "MM TETOUAN BOUJARAH": "Tétouan",
        "MM TETOUAN": "Tétouan",
        "MARJANE TETOUAN": "Tétouan"
    }
    # --- Ajout de la colonne Ville ---
    df['Ville'] = df['Site'].map(site_ville)

    # --- Avertissement si un site n'est pas trouvé ---
    missing_ville = df[df['Ville'].isna()]['Site'].unique()
    

    col_ville, col_site, col_enseigne, col_date = st.columns(4)

    # --- Filtre Ville ---
    villes = ["Tout"] + sorted(df['Ville'].dropna().unique())
    selected_ville = col_ville.selectbox("Ville", options=villes, index=0)  # "Tout" sélectionné par défaut

    # --- Filtre Site dépendant de la ville ---
    if selected_ville != "Tout":
        sites = ["Tout"] + sorted(df[df['Ville'] == selected_ville]['Site'].dropna().unique())
    else:
        sites = ["Tout"] + sorted(df['Site'].dropna().unique())
    selected_site = col_site.selectbox("Site", options=sites, index=0)  # "Tout" par défaut

    # --- Filtre Enseigne dépendant de la ville ---
    if selected_ville != "Tout":
        enseignes = ["Tout"] + sorted(df[df['Ville'] == selected_ville]['Enseigne'].dropna().unique())
    else:
        enseignes = ["Tout"] + sorted(df['Enseigne'].dropna().unique())
    selected_enseigne = col_enseigne.selectbox("Enseigne", options=enseignes, index=0)  # "Tout" par défaut

    # --- Filtre Date ---
    dates_dispo = ["Tout"] + sorted(df['Date stock'].dropna().dt.date.unique())
    selected_date = col_date.selectbox("Date", options=dates_dispo, index=0)  # "Tout" par défaut

    # --- Filtrer le DataFrame selon la sélection ---
    df_filtered = df.copy()
    if selected_ville != "Tout":
        df_filtered = df_filtered[df_filtered['Ville'] == selected_ville]
    if selected_site != "Tout":
        df_filtered = df_filtered[df_filtered['Site'] == selected_site]
    if selected_enseigne != "Tout":
        df_filtered = df_filtered[df_filtered['Enseigne'] == selected_enseigne]
    if selected_date != "Tout":
        df_filtered = df_filtered[df_filtered['Date stock'].dt.date == selected_date]


    tab1,tab2,tab3 = st.tabs(["Analyse 1","Analyse 2","matrice"])

    with tab1:
        # --- Ligne des métriques ---
        col1, col2, col3 = st.columns([1,1,1])

        with col1:
            st.metric("Somme de Quantité stock", f"{int(df_filtered['Quantité stock'].sum()):,}")

        with col2:
            produits_rupture = df_filtered.loc[df_filtered['Quantité stock'] <= 6, 'Libellé article'].nunique()
            st.metric("Produits en Rupture", produits_rupture)

        with col3:
            st.metric("Moyenne de Quantité stock", f"{df_filtered['Quantité stock'].mean():.2f}")

        st.markdown("---")

        # --- Graphiques ---
        col_left , col_right = st.columns([1,1])

        with col_left:
            st.markdown(
                "<h4 style='text-align: center;'>TOP 10 des articles en STOCK</h4>",
                unsafe_allow_html=True
            )
            top10_articles = (
                df_filtered.groupby('Libellé article')['Quantité stock']
                .sum()
                .reset_index()
                .sort_values(by='Quantité stock', ascending=False)
                .head(10)
            )
            plt.style.use("dark_background")  
            fig, ax = plt.subplots(figsize=(6,4))
            sns.barplot(
                data=top10_articles,
                x='Quantité stock',
                y='Libellé article',
                palette="viridis",
                ax=ax
            )
            ax.set_xlabel("Quantité en stock")
            ax.set_ylabel("Article")
            st.pyplot(fig)

        with col_right:
            st.markdown(
                "<h4 style='text-align: center;'>Évolution du stock dans le temps</h4>",
                unsafe_allow_html=True
            )
            df_filtered['Date stock'] = pd.to_datetime(df_filtered['Date stock'])

            # Grouper par date et sommer le stock
            df_evo = (
                df_filtered.groupby('Date stock')['Quantité stock']
                .sum()
                .reset_index()
                .sort_values(by='Date stock')
            )
            plt.style.use("dark_background")  # mode sombre
            fig, ax = plt.subplots(figsize=(8,3))
            sns.lineplot(
                data=df_evo,
                x="Date stock",
                y="Quantité stock",
                marker="o",
                color="#1f77b4",
                ax=ax
            )

            # Habillage
            ax.set_xlabel("Date", color="white")
            ax.set_ylabel("Quantité totale en stock", color="white")
            ax.tick_params(colors="white")

            st.pyplot(fig)


    with tab2:
        carte1 , carte2 = st.columns([1,1])
        with carte1:
            stock_magasins = df_filtered[df_filtered['Site'] != "Entrepot Sapino"]['Quantité stock'].sum()
            st.metric("Stock Magasins", f"{stock_magasins:,}")

        with carte2:
            stock_entrepot = df_filtered[df_filtered['Site'] == "Entrepot Sapino"]['Quantité stock'].sum()
            st.metric("Stock Entrepôt Sapino", f"{stock_entrepot:,}")

        st.markdown("---")   
        colm_left , colm_right = st.columns([1,1])
        with colm_left:
            st.markdown("<h4 style='text-align: center;'>Stock total par Enseigne</h4>", unsafe_allow_html=True)
            df_enseigne = df_filtered.groupby('Enseigne')['Quantité stock'].sum().reset_index().sort_values(by='Quantité stock', ascending=False)
            
            plt.style.use("dark_background")
            fig, ax = plt.subplots(figsize=(9,3))
            sns.barplot(
                data=df_enseigne,
                x='Quantité stock',
                y='Enseigne',
                palette="magma",
                ax=ax
            )
            ax.set_xlabel("Quantité en stock")
            ax.set_ylabel("Enseigne")
            st.pyplot(fig)
        with colm_right:
                st.markdown("<h4 style='text-align: center;'>TOP 10 Sites avec le plus de Stock</h4>", unsafe_allow_html=True)

                top10_sites = (df_filtered[df_filtered['Site'] != "Entrepot Sapino"].groupby('Site')['Quantité stock'].sum().reset_index().sort_values(by='Quantité stock', ascending=False).head(10))

                plt.style.use("dark_background")
                fig, ax = plt.subplots(figsize=(8,3))
                sns.barplot(
                    data=top10_sites,
                    x='Quantité stock',
                    y='Site',
                    palette="viridis",
                    ax=ax
                )
                ax.set_xlabel("Quantité en stock")
                ax.set_ylabel("Site")
                st.pyplot(fig)
    with tab3:  # Onglet Matrice
        # Ajouter colonne Marchant
            marchant_mapping = {
            "MARJANE AIN SEBAA": "NOUR EDDINE",
            "MARJANE BOUSKOURA": "HIND",
            "MARJANE CALIFORNIE": "HIND",
            "MARJANE DERB SULTAN": "NOUR EDDINE",
            "MARJANE HAY HASSANI": "SAAD",
            "MARJANE IBN TACHFINE": "NOUR EDDINE",
            "MARJANE MARINA CASABLANCA": "NOUR EDDINE",
            "Marjane Market CASA OASIS": "NOUR EDDINE",
            "MARJANE MOROCCO MALL": "SAAD",
            "MARJANE SIDI OTHMAN": "NOUR EDDINE",
            "MM AERIA MALL": "SAAD",
            "MM AIN SEBAA MEKOUAR": "NOUR EDDINE",
            "MM BERNOUSSI": "NOUR EDDINE",
            "MM BOUSKOURA BO VILLAGE 1": "HIND",
            "MM CASA ALMAZ": "HIND",
            "MM CASA FOURAT": "NOUR EDDINE",
            "MM CASA LAYMOUNE": "SAAD",
            "MM CASA OULFA": "SAAD",
            "MM CASA PALMIER": "SAAD",
            "MM CASA VAL FLEURI": "SAAD",
            "MM CIL": "NOUR EDDINE",
            "MM DAR BOUAAZA": "SAAD",
            "MM DAR BOUAAZA CGI": "SAAD",
            "MM HERMITAGE": "NOUR EDDINE",
            "MM IBNOUTACHAFINE": "NOUR EDDINE",
            "MM INARA": "SAAD",
            "MM PANORAMIQUE": "HIND",
            "MM QUARTIER LES HÔPITAUX": "NOUR EDDINE",
            "MM Sidi Maarouf O Village": "HIND",
            "MM TADDART": "HIND",
            "MM. 2 MARS": "NOUR EDDINE",
            "MM. EMILE ZOLA": "NOUR EDDINE",
            "MM. GHANDI": "SAAD",
            "MM. LIBERTE": "NOUR EDDINE",
            "MM. SIDI OTHMANE": "NOUR EDDINE",
            "MM. TWIN": "NOUR EDDINE",
            "MM.BEAUSEJOUR": "NOUR EDDINE",
            "MM.VILLE VERTE": "HIND"
        }

            df_filtered['Marchant'] = df_filtered['Site'].map(marchant_mapping)

        # Filtre Marchant
            marchant_options = ["Tout"] + sorted(df_filtered['Marchant'].dropna().unique())
            selected_marchant = st.selectbox("Marchant :", options=marchant_options)

        # Appliquer filtre
            if selected_marchant != "Tout":
                df_filtered = df_filtered[df_filtered['Marchant'] == selected_marchant]

        
        # Créer la matrice : lignes = EAN, colonnes = Site, valeurs = somme de Quantité stock
            matrice_stock = df_filtered.pivot_table(
            index='EAN',
            columns='Site',
            values='Quantité stock',
            aggfunc='sum',
            fill_value=np.nan
        )
        
        # Affichage dans Streamlit
            st.dataframe(matrice_stock)  # tableau interactif, scrollable

