# downloadImages-OIDv6

## Général
*Objectif du programme:*  
Ce code permet en une seule ligne de commande de télécharger des images depuis OpenImages dataset. Vous pouvez choisir de les télécharger dans votre répertoire local ou bien de les stocker en mode objet sur un serveur Minio.

*Qu'est-ce que le stockage objet?*  
Un objet est composé d'un fichier (texte, image, vidéo, son...etc) auquel on associe ses métadonnées (date de création, auteur, taille, titre...etc). Un espace de stockage en mode objet permet donc un stockage à plat des données puisqu'il n'y a aucune hiérarchisation : les données sont dites non structurées. Ce type de stockage présente de nombreux intérêts: environnements facilement scalables, garantie pour le client de la disponibilité et de l'intégirité des données.

## Installation
_Python3 is required_

**1. Clone this repository**
```bash
git clone https://github.com/Adelanglais/downloadImages-OIDv6.git
```  
**2. Download the csv files**  
In the repository, create an under reperoty named _csv_files_ and download the following files
* https://storage.googleapis.com/openimages/v5/class-descriptions-boxable.csv
* https://appen.com/datasets/open-images-annotated-with-bounding-boxes/#download-preview-1
* https://storage.googleapis.com/openimages/2018_04/image_ids_and_rotation.csv  

**3. Installed the required packages**  
```bash
python3 install -r requirements.txt
```
**4. Create the Minio container**  
First, you have to create a file named docker-entrypoint.sh with the following syntaxe:
```bash
docker run -t -p 9000:9000 --name nameExample \
          -e "MINIO_ACCESSS_KEY=idexample" \
          -e "MINIO_SECRET_KEY=secretexample \
          -v /home/dev/mdate:/data \
          minio/minio server /data
```
Once this file is created, you can initialize your personnal Minio server
```bash
./docker-entrypoint.sh
```
You can now run the code and download images

## Utilisation
```bash
python3 OID_minio.py downloader --classes Dog --limit 10
```

## Commands list
1. *downloader* : download the images on the minio server
2. *getURL* : returns a list of URL of the reqested images
3. *listClasses* : returns a list of all the classes of the OpenImages Dataset

For other parameters:
1. *--classes* : wait a string of the requested class
2. *--limit* : wait the number of image you want to download
3. *--location*: wait "local" or "minio", the location you want the images to be downloaded
