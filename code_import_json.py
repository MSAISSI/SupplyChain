from elasticsearch import Elasticsearch
import json

# Configuration d'Elasticsearch
es = Elasticsearch(hosts = "https://elastic:datascientest@localhost:9200", ca_certs="./ca/ca.crt")

# Nom de l'index Elasticsearch que je souhaite créer
index_name = "entreprise_reviews"

# Chemin vers le fichier JSON à importer
json_file_path = "/home/simo/elasticsearch/data_sources/yoga_meditation.json"

def create_index():
    # Vérifier si l'index existe déjà
    if es.indices.exists(index=index_name):
        print(f"L'index '{index_name}' existe déjà.")
        return
    else:
        # Créer un nouvel index
        es.indices.create(index=index_name)
        print(f"L'index '{index_name}' a été créé.")

def import_json_data():
    # Charger les données depuis le fichier JSON
    with open(json_file_path, 'r') as json_file:
        data = json.load(json_file)

    # Parcourir les documents et les indexer dans Elasticsearch
    for doc_id, document in enumerate(data["Entreprise"]):
        es.index(index=index_name, id=doc_id, body=document)

    print(f"{len(data)} documents ont été indexés dans '{index_name}'.")

if __name__ == "__main__":
    # Créer l'index
    create_index()

    # Importer les données JSON dans Elasticsearch
    import_json_data()
