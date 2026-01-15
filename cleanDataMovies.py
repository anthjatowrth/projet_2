import pandas as pd
import numpy as np

def clean_movie_dataset(df, verbose=True):
    """
    Nettoyage et clarification d'un DataFrame cinéma/films.

    Étapes principales :
    1. Supprimer doublons
    2. Standardiser les noms de colonnes
    3. Convertir les dates
    4. Traiter les valeurs manquantes
    5. Convertir les colonnes numériques
    6. Supprimer les colonnes vides ou quasi-vides
    7. Nettoyage texte (titres, genres, etc.)
    
    Args:
        df (pd.DataFrame): le DataFrame brut
        verbose (bool): afficher un résumé des actions
        
    Returns:
        pd.DataFrame: DataFrame nettoyé
    """

    # --- 1. Supprimer les doublons ---
    initial_rows = df.shape[0]
    df = df.drop_duplicates()
    if verbose:
        print(f"Suppression des doublons : {initial_rows - df.shape[0]} lignes supprimées")
    
    # --- 2. Standardiser les noms de colonnes ---
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('-', '_')
    
    # --- 3. Convertir les dates ---
    # On cherche les colonnes qui contiennent "date", "year", "release"
    date_cols = [c for c in df.columns if 'date' in c or 'year' in c or 'release' in c]
    for c in date_cols:
        df[c] = pd.to_datetime(df[c], errors='coerce')  # erreurs converties en NaT
        if verbose:
            print(f"Colonne {c} convertie en datetime")
    
    # --- 4. Traiter les valeurs manquantes ---
    # Remplacer chaînes vides par NaN
    df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
    
    # Optionnel : remplir ou supprimer certaines colonnes clés
    # Exemple : titre et année doivent idéalement être présents
    if 'title' in df.columns:
        df = df.dropna(subset=['title'])
    if 'year' in df.columns:
        df['year'] = pd.to_numeric(df['year'], errors='coerce')
    
    # --- 5. Convertir les colonnes numériques ---
    # Identifier les colonnes numériques potentielles
    num_cols = [c for c in df.columns if df[c].dtype == 'object' and df[c].str.replace('.', '', 1).str.isdigit().all()]
    for c in num_cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
        if verbose:
            print(f"Colonne {c} convertie en numérique")
    
    # --- 6. Supprimer les colonnes vides ou quasi-vides ---
    threshold = 0.8  # supprimer si >80% NaN
    drop_cols = df.columns[df.isna().mean() > threshold]
    df = df.drop(columns=drop_cols)
    if verbose and len(drop_cols) > 0:
        print(f"Colonnes supprimées (>80% manquantes) : {list(drop_cols)}")
    
    # --- 7. Nettoyage texte ---
    text_cols = df.select_dtypes(include='object').columns
    for c in text_cols:
        df[c] = df[c].str.strip().str.title()  # supprime espaces + capitalisation
        df[c] = df[c].replace('', np.nan)
    
    # --- Résumé final ---
    if verbose:
        print(f"Dataset nettoyé : {df.shape[0]} lignes, {df.shape[1]} colonnes")
    
    return df


#Summary

def quick_dataset_summary(df, top_n=5, verbose=True):
    """
    Présentation rapide et complète d'un DataFrame Pandas.
    
    Args:
        df (pd.DataFrame): le dataset à analyser
        top_n (int): nombre de valeurs uniques les plus fréquentes à afficher pour les colonnes qualitatives
        verbose (bool): afficher le résumé
    
    Returns:
        None
    """
    
    if not verbose:
        return
    
    print("=== Dimensions ===")
    print(f"Lignes : {df.shape[0]}, Colonnes : {df.shape[1]}\n")
    
    print("=== Aperçu des premières lignes ===")
    print(df.head(), "\n")
    
    print("=== Types de colonnes ===")
    print(df.dtypes, "\n")
    
    print("=== Valeurs manquantes ===")
    missing = df.isna().sum()
    missing_percent = (missing / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'missing_count': missing, 'missing_percent': missing_percent})
    print(missing_df[missing_df['missing_count'] > 0].sort_values('missing_count', ascending=False), "\n")
    
    print("=== Statistiques descriptives (numériques) ===")
    print(df.describe().T, "\n")
    
    print("=== Colonnes qualitatives ===")
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    if len(cat_cols) == 0:
        print("Aucune colonne qualitative détectée.\n")
    else:
        for col in cat_cols:
            print(f"\n-- {col} --")
            print(df[col].value_counts(dropna=False).head(top_n))
    
    print("\n=== Corrélations (numériques) ===")
    num_cols = df.select_dtypes(include=np.number).columns
    if len(num_cols) > 1:
        print(df[num_cols].corr().round(2))
    else:
        print("Pas assez de colonnes numériques pour calculer une corrélation.")