SmartStudent Analytics

Application Streamlit multi-pages d'analyse et de prédiction des performances académiques des étudiants, combinant tableaux de bord, visualisation de données et modèles de Machine Learning (Random Forest, K-Means).

Vue d'ensemble

SmartStudent Analytics permet de :

- Collecter les données d'étudiants via un formulaire (habitudes d'étude, mode de vie, bien-être, résultats).
- Visualiser ces données sous forme de tableaux de bord (KPI, distributions, corrélations, comparaisons par filière/niveau).
- Prédire la moyenne d'un étudiant selon différents scénarios ("What-If") grâce à un modèle de Random Forest entraîné par filière.
- Segmenter les étudiants en profils (Performants / Moyens / À risque) via un clustering K-Means.
- Évaluer un risque académique individuel (décrochage, baisse de performance) à partir d'indicateurs de stress, sommeil, motivation, etc.
- Générer un rapport PDF individuel par étudiant.
- Administrer les données (suppression sécurisée d'un enregistrement).

Toutes les pages partagent la même charte graphique : thème sombre, typographie Inter / IBM Plex Mono, cartes à bordure fine, graphiques Plotly harmonisés.

---

Structure de l'application

| Fichier | Page | Rôle |
|---|---|---|
| `app.py` |  Accueil | Tableau de bord général : objectifs du projet, indicateurs globaux, top 10 des étudiants, distributions, facteurs de réussite, recommandations automatiques |
| `page_formulaire.py` |  Formulaire | Saisie et enregistrement d'un nouvel étudiant dans `data_students.csv` |
| `page_analyse_globale.py` |  Analyse Globale | Statistiques descriptives complètes : histogrammes, répartitions, matrice de corrélation, comparaisons par filière/niveau, analyse intelligente, export CSV |
| `page_data_explorer.py` |  Data Explorer | Filtrage interactif des étudiants (filière / niveau / sexe) et consultation d'une fiche individuelle |
| `page_simulation_ia.py` |  Simulation IA | Simulateur "What-If" : prédiction de la moyenne selon des paramètres d'étude modifiables, via un modèle Random Forest entraîné par filière |
| `page_profil_etudiant.py` |  Profil Étudiant | Auto-évaluation : score de risque académique personnel, radar de profil, recommandations |
| `page_clustering.py` |  Clustering | Segmentation non supervisée (K-Means) des étudiants en 3 profils selon leurs indicateurs |
| `page_rapport_ia.py` |  Rapport IA | Génération d'un rapport PDF individuel (profil + diagnostic de risque) |
| `page_gestion_etudiants.py` |  Gestion | Interface d'administration pour supprimer un enregistrement étudiant |

> Dans Streamlit, la page de niveau racine (`app.py`) sert de page d'accueil ; les autres fichiers doivent être placés dans un dossier `pages/` pour apparaître automatiquement dans le menu latéral de navigation.

---

Données

Toutes les pages lisent/écrivent le même fichier : **`data_students.csv`**, créé automatiquement à la première soumission du formulaire.

Colonnes utilisées :

| Colonne | Description |
|---|---|
| `nom` | Nom complet de l'étudiant |
| `age` | Âge |
| `sexe` | Masculin / Féminin |
| `filiere` | Filière d'études |
| `niveau` | L1, L2, L3, Master1, Master2, PhD |
| `heures_etude` | Heures d'étude par jour |
| `methode` | Méthode d'apprentissage (seul / groupe) |
| `regularite` | Régularité de travail (1–10) |
| `sommeil` | Heures de sommeil |
| `sport` | Pratique d'une activité sportive (Oui/Non) |
| `telephone` | Temps passé sur téléphone (h/jour) |
| `stress` | Niveau de stress (1–10) |
| `concentration` | Niveau de concentration (1–10) |
| `motivation` | Niveau de motivation (1–10) |
| `moyenne` | Moyenne académique (/20) |
| `credits` | Crédits validés |

---

Modèles utilisés

- Random Forest Regressor (`page_simulation_ia.py`) — un modèle est entraîné par filière (minimum 5 étudiants requis) pour prédire la moyenne à partir des habitudes d'étude, du bien-être et du sexe. La précision est mesurée par la MAE (erreur absolue moyenne).
- K-Means (`page_clustering.py`) — segmentation en 3 groupes (Performants / Moyens / À risque) à partir de la moyenne, du stress, des heures d'étude, du sommeil, de la motivation et de la concentration, après normalisation (`StandardScaler`).
- Score de risque pondéré (`page_profil_etudiant.py`, `page_rapport_ia.py`) — formule non supervisée combinant stress, sommeil et heures d'étude pour classer un étudiant en risque faible / moyen / élevé.

---

Installation

```bash
pip install streamlit pandas numpy plotly scikit-learn reportlab seaborn matplotlib
```

 Lancement

```bash
streamlit run app.py
```

Placer les fichiers `page_*.py` dans un dossier `pages/` à la racine du projet pour qu'ils apparaissent dans le menu de navigation Streamlit, par exemple :

```
mon_projet/
├── app.py
├── data_students.csv        (généré automatiquement)
└── pages/
    ├── 1_Formulaire.py
    ├── 2_Analyse_Globale.py
    ├── 3_Data_Explorer.py
    ├── 4_Simulation_IA.py
    ├── 5_Profil_Etudiant.py
    ├── 6_Clustering.py
    ├── 7_Rapport_IA.py
    └── 8_Gestion_Etudiants.py
```

(renommer les fichiers avec un préfixe numérique permet de fixer l'ordre d'affichage dans le menu latéral)*

---

Charte graphique

Toutes les pages partagent les mêmes constantes de design (déclarées en tête de chaque fichier) :

- Couleurs : fond `#0A0B0E`, cartes `#131418`, accent `#6C8EF5`, plus teal / ambre / corail / violet pour les statuts.
- Typographies : Inter (texte), IBM Plex Mono (valeurs chiffrées / KPI).
- Composants réutilisés : `render_html()` (évite le bug d'indentation Markdown de Streamlit), `section_title()`, `style_chart()` / `style_heatmap()` pour les graphiques Plotly, `kpi_row()` pour les cartes d'indicateurs.

---

 Limites

- Les données sont stockées dans un simple fichier CSV local (`data_students.csv`) : pas de base de données, pas de gestion multi-utilisateurs concurrente.
- Les modèles (Random Forest, K-Means) sont ré-entraînés à chaque session via le cache Streamlit (`@st.cache_resource` / `@st.cache_data`) et nécessitent un minimum de données par filière pour être fiables (5 étudiants minimum).
- La suppression d'un étudiant (page Gestion) est définitive et irréversible.
