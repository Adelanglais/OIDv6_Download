# downloadImages-OIDv6

## Général
*Objectif du programme:*  
Ce code permet en une seule ligne de commande de télécharger des images depuis OpenImages dataset. Vous pouvez choisir de les télécharger dans votre répertoire local ou bien de les stocker en mode objet sur un serveur Minio.

*Qu'est-ce que le stockage objet?*  
Un objet est composé d'un fichier (texte, image, vidéo, son...etc) auquel on associe ses métadonnées (date de création, auteur, taille, titre...etc). Un espace de stockage en mode objet permet donc un stockage à plat des données puisqu'il n'y a aucune hiérarchisation : les données sont dites non structurées. Ce type de stockage présente de nombreux intérêts: environnements facilement scalables, garantie pour le client de la disponibilité et de l'intégirité des données.

## Installation
_fonctionne avec python3_

**1. Cloner le projet git**
```bash
git clone https://github.com/Adelanglais/downloadImages-OIDv6.git
```  
**2. Télécharger les fichers csv**  
Dans le répertoire du projet, créer un dossier *csv_files* et y télécharger les fichiers suivants:
* https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
* https://appen.com/datasets/open-images-annotated-with-bounding-boxes/#download-preview-1
* https://storage.googleapis.com/openimages/2018_04/image_ids_and_rotation.csv  

**3. Installation des paquets nécessaires**  
```bash
python3 install -r requirements.txt
```

**4. Placer vous dans un environnement virtuel**
```bash
virtualenv venv
source venv/bin/activate
```

**5. Initialisation du serveur Minio**  
Dans le répertoire du projet, créer le fichier _docker-entrypoint.sh_ avec la syntaxe suivante:
```bash
docker run -t -p 9000:9000 --name nameExample \
          -e "MINIO_ACCESSS_KEY=idexample" \
          -e "MINIO_SECRET_KEY=secretexample \
          -v /home/dev/mdate:/data \
          minio/minio server /data
```
Modifier _nameExample, idexample,secretexample_ selon votre propre endpoint, identifiante et mot de passe.

## Utilisation
_Démarrer le conteneur Minio_
```bash
./docker-entrypoint.sh
```
_Exemple d'utilisation du programme_
```bash
python3 downloader_OIDv6.py downloader --classe Dog --limit 10 --location local
```

## Commands list
1. *downloader* : pour effectuer un téléchargement (en local ou sur Minio)
```bash
python3 downloader_OIDv6.py downloader --classe [exemple] --limit [exemple] --location [local ou minio]
```
2. *getURL* : pour accéder aux URL des images d'une certaine classe
```bash
python3 downloader_OIDv6.py get URL --classe [exemple] --limit [exemple]
```
3. *listClasses* : returns a list of all the classes of the OpenImages Dataset
```bash
python3 downloader_OIDv6.py listClasses
```

Arguments
1. *--classes* : attend le nom de la classe souhaitée
2. *--limit* : attend le nombre d'image à télécharger
3. *--location*: attend "local" ou "minio", l'endroit où seront téléchargées les images

## Fonctionnement général du programme
<img src="https://github.com/Adelanglais/OIDv6_Download/blob/main/Capture%20d%E2%80%99%C3%A9cran%20du%202020-10-23%2011-26-19.png"/>

