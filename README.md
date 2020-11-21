# MyNetworkAPI
Mise en place d’une solution IA d’évaluation de la connectivité pour un itinéraire.

# Fichiers contenus dans MyNetworkAPI:
- .cfignore : Lorsque vous insérez l'application dans IBM Cloud, les fichiers et répertoires contenus dans .cfignore ne  sont pas transférés.
- Dockerfile : Fichier texte qui contient les commandes permettant de créer une image pour l'application Python dans IBM Cloud.
- manifest.yml : Présente les informations relatives à l'application dont vous aurez besoin pour insérer cette dernière dans IBM Cloud.
- Procfile : Fichier texte qui contient la commande permettant d'exécuter l'application dans IBM Cloud.
- requirements.txt : Répertorie les packages et versions requis par l'application dont vous aurez besoin pour insérer cette dernière dans IBM Cloud.
- app.py : Code de serveur Python Flask qui contrôle les fonctionnalités de l'application Web (par exemple : l'envoi des données utiles pour la prédiction du temps de disponibilité de la connectivité).
- NewDataSet : Notre ensemble de données utilisé pour le training.

# Étapes pour éxecuter ce projet: 

## Étape 1:
Ouvrez le terminal et collez cette commande pour cloner l'application. Un petit rappel que cette étape ne fonctionnera que si Git est installé sur votre ordinateur.

	git clone https://github.com/khouloudayadi/MyNetworkAPI.git

## Étape 2:
Ensuite, allez dans ce dossier en tapant.

	cd MyNetworkAPI

## Étape 3:
Créez d'abord un environnement virtuel et installez les dépendances en exécutant.   
- pour Ubuntu 16.04:

	python3 -m venv venv
	
	source venv/bin/activate
	
	pip install -r requirements.txt

- pour windows 10

	python -m venv venv
	
	.\venv\Scripts\activate
	
	pip install -r requirements.txt


## Étape 4:
exécutez le serveur localement en tapant 	

	python app.py

## Étape 5: 
Pour tester la méthode qui permet de prédire le temps de disponibilité de la connectivité réseau grâce à Postman:
	- Sélectionnez le type de requête à envoyer : POST
	- Ajoutez L'URL de l'API :  http://127.0.0.1:8000/predict
	- Cliquez sur l'onglet Body qui n'est plus grisé, puis sélectionnez raw pour définir manuellement le contenu de la requête Http
	- Sélectionnez à droite JSON à la place de Text afin d'indiquer dans notre requête le type de données que nous envoyons
	- Collez ensuite un JSON avec les informations d'un requête, par exemple :{"start_lat":35.8626285,"start_lon":10.5999459,"end_lat":35.677692,"end_lon":10.096388,"vitesse":0.11869553476572037,"timeStamp":"1604443367000","network":"3G"}

## Étape 6: 
Pour tester la méthode qui permet de prédire le temps de disponibilité de la connectivité réseau grâce à Postman, après le déploiement sur IBM Cloud :
	1- Sélectionnez le type de requête à envoyer : POST
	2- Ajoutez L'URL de l'API :  https://mynetworkapi.eu-gb.cf.appdomain.cloud/predict
	3- Cliquez sur l'onglet Body qui n'est plus grisé, puis sélectionnez raw pour définir manuellement le contenu de la requête Http
	4- Sélectionnez à droite JSON à la place de Text afin d'indiquer dans notre requête le type de données que nous envoyons
	5- Collez ensuite un JSON avec les informations d'un requête, par exemple : 		{"start_lat":35.8626285,"start_lon":10.5999459,"end_lat":35.677692,"end_lon":10.096388,"vitesse":0.11869553476572037,"timeStamp":"1604443367000","network":"3G"}

## Étape 7: 
Pour tester notre application mobile :
	1- Télécharger le fichier My-Network.apk de : https://github.com/khouloudayadi/AppNetwork.git
	2- Installer le fichier My-Network.apk sur votre smartphone.

