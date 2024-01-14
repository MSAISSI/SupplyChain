# SupplyChain
Projet file rouge, cas pratique dans le cadre de la formation Data Engineer de l'organisme DataScientest.

## Composants de projet  : 
	- Elasticsearch
		- Création de 3 noeuds elasticsearch pour la partie NoSql du projet, index des commentaires ‘reviews_per_category_new’
	- MySQL PHPMyAdmin 
		- Création de la base de données SQL, composée de deux tables (entreprise, analyse_sentiment)

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
     --> <img width="861" alt="image" src="https://github.com/MSAISSI/SupplyChain/assets/56922928/543528a3-2738-4326-aae6-3bf8159b85a5">
     Le premier conteneur qui se lance est celui nommé PythonScrappingEntreprise

   2 - 
