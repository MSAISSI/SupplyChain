import mysql.connector
from fastapi import FastAPI, HTTPException
from typing import List
from fastapi import Path

app = FastAPI()

# Configuration de la base de données
config = {
    'host': "localhost",
    'user': "root",
    'password': "simodb2@23",
    'database': 'projet',
    'auth_plugin': 'mysql_native_password',  # Utilisez 'mysql_native_password' au lieu de 'caching_sha2_password'
}

# Création de l'objet de connexion à la base de données
def get_database_connection():
    return mysql.connector.connect(**config)

# Endpoint pour récupérer la liste des catégories
@app.get("/categories", response_model=List[str])
async def get_categories():
    try:
        with get_database_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = "SELECT nom FROM categorie"
                cursor.execute(query)
                categories = cursor.fetchall()
                # Extraire les valeurs de la clé 'nom' de chaque dictionnaire
                category_names = [category['nom'] for category in categories]
                return category_names
    except Exception as e:
        # Gérer les erreurs de connexion ou d'exécution de requête
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {e}")
###########
###########
# Endpoint pour récupérer la liste des entreprises pour une catégorie spécifique:

@app.get("/categorie/{categorie}/entreprises", response_model=List[str])
async def get_entreprises_for_categorie(categorie: str):
    try:
        with get_database_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT nom FROM entreprise 
                    WHERE entreprise_id IN (
                        SELECT entreprise_id FROM entreprise_categorie 
                        WHERE categorie_id IN (
                            SELECT categorie_id FROM categorie WHERE nom = %s
                        )
                    )
                """
                cursor.execute(query, (categorie,))
                entreprises = cursor.fetchall()
                entreprises_names = [entreprise['nom'] for entreprise in entreprises]
                
                if not entreprises_names:
                    raise HTTPException(status_code=404, detail="Aucune entreprise trouvée pour cette catégorie")
                return entreprises_names
    except Exception as e:
        # Gérer les erreurs de connexion ou d'exécution de requête
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {e}")

####
####
# Endpoint pour récupérer le score moyen par entreprise en fonction du lien
@app.get("/score-moyen-par-entreprise/{lien}", response_model=dict)
async def get_score_moyen_par_entreprise(lien: str = Path(..., title="Nom de l'entreprise")):
    try:
        with get_database_connection() as conn:
            with conn.cursor(dictionary=True) as cursor:
                query = """
                    SELECT AVG(score) as score_moyen
                    FROM analyse_sentiment
                    WHERE lien = %s
                """
                cursor.execute(query, (lien,))
                score_moyen = cursor.fetchone()

                if score_moyen is None:
                    raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour cette entreprise")

                return {"lien": lien, "score_moyen": score_moyen["score_moyen"]}
    
    except Exception as e:
        # Gérer les erreurs de connexion ou d'exécution de requête
        raise HTTPException(status_code=500, detail=f"Erreur lors de la récupération des données: {e}")
