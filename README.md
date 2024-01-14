# SupplyChain
Projet file rouge, cas pratique dans le cadre de la formation Data Engineer de l'organisme DataScientest.

## Composants de projet  : 
	- Elasticsearch
		- Création de 3 noeuds elasticsearch pour la partie NoSql du projet, index des commentaires ‘reviews_per_category_new’
	- MySQL PHPMyAdmin 
		- Création de la base de données SQL 'supply_chain', composée de deux tables (entreprise, analyse_sentiment)

	- Codes Python
		- Scrapping des entreprises (données overview) de la catégorie electronic_technology
			--> Création d'un fichier Entreprise.csv
		- Scrapping des commentaires de ces entreprises
			--> Création d'un dossier 'json' contenant des fichiers de commentaires 
		- Création et mapping de l'index ‘reviews_per_category_new’ dans elasticsearch en important les fichiers json des commentaires
		- Réalisation du score d'analyse de sentiments NLTK sur les commentaires importés de elasticsearch
			--> Création d'un fichier sentiment_analysis.csv contenant les scores 
	- FastAPi
		- API qui pointe sur la base de données et qui retourne certaines réponses selon la demande de l'utilisateur : 
			--> la liste des entreprises de la catégorie
			--> nombre d'avis et d'étoiles par entreprise choisie
			--> score moyen par entreprise

   ## Etapes d"utilisation
   1 - Lancer la commande bash suivante : docker-compose up --build -d dans le dossier du projet
      <img width="861" alt="image" src="https://github.com/MSAISSI/SupplyChain/assets/56922928/543528a3-2738-4326-aae6-3bf8159b85a5">

   2 - Pour visualiser la base de données dans MySQl (http://localhost:8080)
   	- Authentification : utilisateur =equipe_de, mot de passe=equipe_de23
    <img width="1045" alt="image" src="https://github.com/MSAISSI/SupplyChain/assets/56922928/d6fce4a9-c131-4af7-b82f-22e79cf84f4b">

   3 - Pour requêter l'API (http://localhost:8000/docs)
   	- Authentification : username =user1, password=abcd
   <img width="1027" alt="image" src="https://github.com/MSAISSI/SupplyChain/assets/56922928/0342419a-f6c3-4b44-a5d6-4a8bd734ec18">
   	- Pour récupérer par exemple le nombre d'avis par entreprise, aller chercher le lien de l'entreprise dans la table SQL 'analyse_sentiment' et le remplir dans le champs suivant : 
    <img width="1010" alt="image" src="https://github.com/MSAISSI/SupplyChain/assets/56922928/154f1f23-f1a7-4e8e-a7dd-e3c58372e5d1">

    



