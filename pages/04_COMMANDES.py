import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns   
from matplotlib import pyplot as plt

st.set_page_config(page_title="Commande", page_icon="📝", layout="wide")
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
file_commande = st.sidebar.file_uploader("Télécharger un fichier exel", type=["xlsx"])
if file_commande:
    st.session_state['df_org_commande'] = pd.read_excel(file_commande)
    st.sidebar.success("Fichier chargé avec succès !")

# --- Vérifier si le DataFrame existe ---
if 'df_org_commande' in st.session_state:
    df_org = st.session_state['df_org_commande']
    df = df_org.copy()
    col_ville, col_site, col_enseigne, col_date, col_etat = st.columns(5)

    # --- Filtre Ville ---
    villes = ["Tout"] + sorted(df['Ville'].dropna().unique())
    selected_ville = col_ville.selectbox("Ville", options=villes, index=0)

    # --- Filtre Site dépendant de la ville ---
    if selected_ville != "Tout":
        sites = ["Tout"] + sorted(df[df['Ville'] == selected_ville]['Site'].dropna().unique())
    else:
        sites = ["Tout"] + sorted(df['Site'].dropna().unique())
    selected_site = col_site.selectbox("Site", options=sites, index=0)

    # --- Filtre Enseigne dépendant de la ville ---
    if selected_ville != "Tout":
        enseignes = ["Tout"] + sorted(df[df['Ville'] == selected_ville]['Enseigne'].dropna().unique())
    else:
        enseignes = ["Tout"] + sorted(df['Enseigne'].dropna().unique())
    selected_enseigne = col_enseigne.selectbox("Enseigne", options=enseignes, index=0)

    # --- Filtre Date de commande ---
    dates_dispo = ["Tout"] + sorted(df['Date de commande'].dropna().dt.date.unique())
    selected_date = col_date.selectbox("Date de commande", options=dates_dispo, index=0)

    # --- Filtre Etat de commande ---
    etats_dispo = ["Tout"] + sorted(df['Etat de commande'].dropna().unique())
    selected_etat = col_etat.selectbox("Etat de commande", options=etats_dispo, index=0)

    # --- Appliquer les filtres ---
    df_filtered = df.copy()
    if selected_ville != "Tout":
        df_filtered = df_filtered[df_filtered['Ville'] == selected_ville]
    if selected_site != "Tout":
        df_filtered = df_filtered[df_filtered['Site'] == selected_site]
    if selected_enseigne != "Tout":
        df_filtered = df_filtered[df_filtered['Enseigne'] == selected_enseigne]
    if selected_date != "Tout":
        df_filtered = df_filtered[df_filtered['Date de commande'].dt.date == selected_date]
    if selected_etat != "Tout":
        df_filtered = df_filtered[df_filtered['Etat de commande'] == selected_etat]
    
    tab1,tab2 = st.tabs(["📊 Vue Globale","📈 Évolution Mensuelle"])
    
    with tab1:
        # --- Métriques principales ---
        col1, col2,col3 = st.columns(3)

        with col1:
            df_filtered_sans_derniere = df_filtered.iloc[:-1]  # exclut la dernière ligne
            total_commandes = df_filtered_sans_derniere['Numéro de commande'].nunique()
            st.metric("Nombre total de commandes", f"{total_commandes:,}")


        with col2:
            total_quantite = df_filtered['Quantité commandée UVC'].sum()
            st.metric("Quantité totale commandée", f"{int(total_quantite):,} UVC")

        with col3:
            nombre_references = df_filtered['Libellé article'].nunique()
            st.metric("Nombre de références commandées", f"{nombre_references}")


        st.markdown("---")

        col_left, col_right = st.columns(2)
        with col_left:
            # Compter le nombre de commandes par état sur le DataFrame filtré
            etat_counts = df_filtered['Etat de commande'].value_counts().reset_index()
            etat_counts.columns = ['Etat de commande', 'Nombre de commandes']

            # Trier pour que la barre la plus grande soit en haut
            etat_counts = etat_counts.sort_values('Nombre de commandes', ascending=True)
            fig, ax = plt.subplots(figsize=(6,3))
            sns.barplot(
                data=etat_counts,
                x='Nombre de commandes',
                y='Etat de commande',
                palette="pastel",
                ax=ax
            )

            # Habillage
            ax.set_xlabel("Nombre de commandes")
            ax.set_ylabel("État de commande")
            ax.set_title("Répartition des commandes par état")

            st.pyplot(fig)
            with col_right:
            # Agréger la quantité commandée par article
                top10_articles = (
                    df_filtered.groupby('Libellé article')['Quantité commandée UVC']
                    .sum()
                    .reset_index()
                    .sort_values('Quantité commandée UVC', ascending=False) 
                    .tail(10) 
                )
                fig, ax = plt.subplots(figsize=(8,6))
                sns.barplot(
                    data=top10_articles,
                    x='Quantité commandée UVC',
                    y='Libellé article',
                    palette="viridis",
                    ax=ax
                )
                ax.set_xlabel("Quantité commandée (UVC)")
                ax.set_ylabel("Article")
                ax.set_title("Top 10 articles par quantité commandée")

                st.pyplot(fig)
    with tab2:
        df_filtered['Date de commande'] = pd.to_datetime(df_filtered['Date de commande'], errors='coerce')
        df_filtered = df_filtered.dropna(subset=['Date de commande'])

        # Créer une colonne Année-Mois
        df_filtered['Mois'] = df_filtered['Date de commande'].dt.to_period('M').astype(str)

        # Agréger les quantités par mois
        evolution_mensuelle = (
            df_filtered.groupby('Mois')['Quantité commandée UVC']
            .sum()
            .reset_index()
        )

        # Graphique en ruban (area chart)
        fig, ax = plt.subplots(figsize=(12,3))
        ax.fill_between(
            evolution_mensuelle['Mois'],
            evolution_mensuelle['Quantité commandée UVC'],
            color="skyblue",
            alpha=0.5
        )
        ax.plot(
            evolution_mensuelle['Mois'],
            evolution_mensuelle['Quantité commandée UVC'],
            color="royalblue",
            marker="o"
        )

        ax.set_title("Évolution mensuelle des quantités commandées")
        ax.set_xlabel("Mois")
        ax.set_ylabel("Quantité commandée (UVC)")
        plt.xticks(rotation=45)

        st.pyplot(fig)










