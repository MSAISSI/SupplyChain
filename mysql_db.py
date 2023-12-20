import csv
import re  
import mysql.connector as mc


config = {
        'host':"localhost",
        'user':"root",
        'password':"simodb2@23"
}

# Nom de la base de données
nom_base_de_donnees = 'projet'

# Connexion à la base de données
con = mc.connect(**config)
cur = con.cursor(buffered=True)
try:
        cur.execute("DROP DATABASE IF EXISTS {}".format(nom_base_de_donnees))
        cur.execute("CREATE DATABASE IF NOT EXISTS {}".format(nom_base_de_donnees))
        print("Base de données créée avec succès.")

        # Utilisation de la base de données
        cur.execute("USE {}".format(nom_base_de_donnees))
        # Création de la table entreprise
        cur.execute("""CREATE TABLE IF NOT EXISTS entreprise (
                                entreprise_id int NOT NULL,
                                nom varchar(255),
                                domaine varchar(255),
                                nombre_avis int,
                                note_trustscore float,
                                lien varchar(255),
                                PRIMARY KEY (entreprise_id)
                        )""")


        # Ouverture du fichier CSV
        with open("DonneesCategories.csv", "r") as csvfile:
                # Création d'un objet DictReader pour lire le fichier CSV
                csvreader = csv.DictReader(csvfile)
                
                # Initialisation de l'entreprise_id à 1
                entreprise_id = 1
                
                # Itération à travers chaque ligne du fichier CSV
                for row in csvreader:
                # Extraction des données de chaque colonne
                        nom = row["Nom"]
                        domaine = row["Domaine"]
                        lien = row["Lien"]
                        # Utilisation d'une expression régulière pour extraire le nombre d'avis
                        nombre_avis_texte = row["Avis"]
                        nombre_avis_match = re.search(r'\d+(?:,\d+)?', nombre_avis_texte)
                        if nombre_avis_match:
                                nombre_avis = int(nombre_avis_match.group().replace(',', ''))
                        else:
                                nombre_avis = 0  # Valeur par défaut si aucun nombre n'est trouvé
                        
                        note_trustscore = row["Note"]
                        if note_trustscore !='N/A':
                                note_trustscore = round(float(row["Note"]), 2)  # Round to 2 decimal places
                        else:
                                note_trustscore = None
                        # Requête SQL d'insertion des données dans la table
                        cur.execute("INSERT INTO entreprise (entreprise_id, nom, domaine, nombre_avis, note_trustscore, lien) VALUES (%s, %s, %s, %s, %s, %s)",
                                (entreprise_id, nom, domaine, nombre_avis, note_trustscore, lien))
                
                        # Incrémentation de l'entreprise_id pour la prochaine itération
                        entreprise_id += 1
                        
        # Afficher un échantillon de la table entreprise:
        cur.execute("SELECT * FROM entreprise LIMIT 20")
        resultats = cur.fetchall()
        for row in resultats:
                print(row)


        cur.execute("""CREATE TABLE IF NOT EXISTS categorie (
                                categorie_id int NOT NULL,
                                nom varchar(255),
                                PRIMARY KEY (categorie_id)
                        )""")

        # Ouverture du fichier CSV
        with open("DonneesCategories.csv", "r") as csvfile:
                # Création d'un objet DictReader pour lire le fichier CSV
                csvreader = csv.DictReader(csvfile)
                
                # Ensemble pour stocker temporairement les catégories uniques
                categories_uniques = set()
                
                # Itération à travers chaque ligne du fichier CSV
                for row in csvreader:
                        # Extraction de la catégorie de chaque ligne
                        categorie = row["Categorie"].strip()  # Utilisez la colonne appropriée
                        
                        # Ajout de la catégorie à l'ensemble
                        categories_uniques.add(categorie)

                        # Initialisation de la categorie_id à 1
                categorie_id = 1

                # Itération à travers chaque catégorie triée
                for categorie in categories_uniques:
                        # Requête SQL d'insertion sans doublon dans la table categorie
                        cur.execute("INSERT INTO categorie (categorie_id, nom) VALUES (%s,%s)", (categorie_id, categorie))
                        categorie_id += 1
                        

        # Afficher un échantillon de la table categorie:
        cur.execute("SELECT * FROM categorie LIMIT 30")
        resultats = cur.fetchall()
        for row in resultats:
                print(row)

        # Création de la table entreprise_categorie:
        cur.execute("""CREATE TABLE IF NOT EXISTS entreprise_categorie (
                    entreprise_id int NOT NULL,
                    categorie_id int NOT NULL,
                    FOREIGN KEY (entreprise_id) REFERENCES entreprise (entreprise_id),
                    FOREIGN KEY (categorie_id) REFERENCES categorie (categorie_id)
               )""")
        # Ouverture du fichier CSV (remplacez "votre_fichier.csv" par le nom de votre fichier CSV)
        with open("DonneesCategories.csv", "r") as csvfile:
                # Création d'un objet DictReader pour lire le fichier CSV
                csvreader = csv.DictReader(csvfile)
                # Itération à travers chaque ligne du fichier CSV
                for row in csvreader:
                        # Extraction des données de chaque colonne
                        nom_entreprise = row["Nom"]
                        categorie = row["Categorie"].strip()  # Utilisez la colonne appropriée
        
                        # Obtention de l'ID de l'entreprise en fonction du nom
                        cur.execute("SELECT entreprise_id FROM entreprise WHERE nom = %s", (nom_entreprise,))
                        entreprise_id = cur.fetchone()
        
                        # Obtention de l'ID de la catégorie en fonction du nom
                        cur.execute("SELECT categorie_id FROM categorie WHERE nom = %s", (categorie,))
                        categorie_id = cur.fetchone()
                        # Vérification si les IDs ont été trouvés
                        if entreprise_id and categorie_id:
                                # Insertion dans la table entreprise_categorie
                                cur.execute("INSERT INTO entreprise_categorie (entreprise_id, categorie_id) VALUES (%s, %s)", (entreprise_id[0], categorie_id[0]))
 
        # Afficher un échantillon de la table entreprise_categorie:
        cur.execute("SELECT * FROM entreprise_categorie LIMIT 30")
        resultats = cur.fetchall()
        for row in resultats:
                print(row)

                query = '''
                SELECT COUNT(a.entreprise_id) AS nombre_entreprises_plusieurs_categories
                FROM (
                SELECT entreprise_id, COUNT(categorie_id) AS nombre_categories
                FROM entreprise_categorie
                GROUP BY entreprise_id
                HAVING nombre_categories > 1
        ) AS a
        '''

        # Exécution de la requête
        cur.execute(query)
        result = cur.fetchone()

        # Affichage du résultat
        if result:
                nombre_entreprises = result[0]
                print(f"Nombre d'entreprises avec plus d'une catégorie : {nombre_entreprises}")

       
        # Ajout d'index à la colonne 'lien' dans la table 'entreprise'
        cur.execute("ALTER TABLE entreprise ADD INDEX lien_index (lien)")
        # Création de la 4éme table contenant le score de l'analyse de sentiment
        cur.execute("""CREATE TABLE IF NOT EXISTS analyse_sentiment (
                    elasticsearch_id varchar(255) NOT NULL,
                    lien varchar(255) NOT NULL,
                    contenu TEXT,
                    score float,
                    FOREIGN KEY (lien) REFERENCES entreprise (lien)
               )""") 

        # Ouverture du fichier CSV 'sentiment_analysis.csv'
        with open("sentiment_analysis.csv") as csvfile:
                # Création d'un objet DictReader pour lire le fichier CSV
                csvreader = csv.DictReader(csvfile)
                
                # Itération à travers chaque ligne du fichier CSV
                for row in csvreader:
                # Extraction des données de chaque colonne
                        elasticsearch_id = row["ID"]
                        lien = row["Entreprise"]
                        contenu = row["Contenu"]
                        score = row["Résultat analyse de sentiment"]
                        # Check if the lien value exists in the entreprise table
                        cur.execute("SELECT lien FROM entreprise WHERE lien = %s", (lien,))
                        existing_lien = cur.fetchone()

                        if existing_lien:
                                # Inserting data into the table
                                cur.execute("INSERT INTO analyse_sentiment (elasticsearch_id, lien, contenu, score) VALUES (%s, %s, %s, %s)", (elasticsearch_id, lien, contenu, score))
        # Afficher un échantillon de la table analyse_sentiment:
        cur.execute("SELECT * FROM analyse_sentiment LIMIT 20")
        resultats = cur.fetchall()
        for row in resultats:
                print(row)

except mc.Error as err:
        print("Erreur: {}".format(err))
        #ne pas valider les changements en cas d'erreur:
        con.rollback()
finally:
        # Valider les changements dans la base de données
        con.commit()
        # Fermer le curseur et la connexion:
        cur.close()
        con.close()
