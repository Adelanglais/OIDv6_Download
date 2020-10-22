import argparse
import random
import requests
import os
import os.path
import shutil
from multiprocessing.dummy import Pool as ThreadPool
import time
import sys
from minio import Minio
from minio.error import ResponseError
from PIL import Image
import getpass

def parser_arguments():
    """
    Manage the input from the terminal.
    :return : parser
    """
    parser = argparse.ArgumentParser(prog = 'OIDv6_ToolKit',
                                    usage = 'python3 %(prog)s [command] --classe [option] --limit [option] --location [option]',
                                    description='This programm allows to download images from OIDv6')
    parser.add_argument("command",
                        metavar= "<command>: 'getURL', 'downloader' or 'listClasses'.",
                        help = "'getURL' or 'listClasses'.")
    parser.add_argument('--classes', required=False, nargs='+',
                    metavar="list of classes",
                    help="Sequence of 'strings' of the wanted classes")
    parser.add_argument('--limit', required=False, type=int, default=None,
                    metavar="integer number",
                    help='Optional limit on number of images to download')
    parser.add_argument('--location',required=False, nargs='+',
                    metavar='where to download',
                    help="where to download: local repository or Minio serveur")

    args = parser.parse_args()
    return args

def getListClasses():
    """
    Access to the list of all classes present in the dataset
    :return: list
    """

    f=open('csv_files/class-descriptions-boxable.csv',"r",encoding='utf8') # file matching the name of the class and its identifier (ex: /m/011k07,Tortoise )
    for ligne in f:
        a=0
        while a < 600:
            ligne = f.readline() # Analysis of the file line by line
            mots = ligne.split(",")
            name_classe = (mots[1])
            print(name_classe)
            a+=1
        #reading the file line by line and displaying the name of each class

def getIdClass():
    """
    Access to the label Name of the requested class
    :return: id of the class asked in the terminal
    """
    name = parser_arguments().classes #list format
    classe = "-".join(name) #string format
    f=open('csv_files/class-descriptions-boxable.csv',"r",encoding='utf8')
    for l in f:
        a=0
        while a < 599:
            l = f.readline()
            mots = l.split(",")
            name = mots[1].replace(" ","")

            if classe in name:
                id_classe = mots[0]
                return id_classe
                # line by line of the file, we check if the name of the class passed in parameter is present.
                # if yes, we return the identifier of this class
                # if not, we test the file's following line
            else:
                a = a+1

def getImgList(id_classe):
    """
    List of images present in the class
    :return : list of identifier
    """
    f=open('csv_files/test-annotations-bbox.csv',"r",encoding='utf8')
    img_list0 = []
    img_list = []
    a = 0
    nb_img = parser_arguments().limit
    for l in f:
        if id_classe in l:
            mots = l.split(",")
            id_img = mots[0]
            img_list0.append(id_img)
    # lists all the identifiers of the images present in the requested class

    while a < nb_img:
        img_list.append(random.choice(img_list0))
        a = a+1
    return img_list
    # select randomly in the previous list the required number (requested in the terminal) of image identifiers and store them in a new list

def getImgURL(img_list):
    """
    Access to image's URL of the images list
    :return : url list
    """
    f = open('csv_files/test-images-with-rotation.csv',"r",encoding='utf8')
    url_list = []
    for l in f:
        mots = l.split(",")
        id = mots[0]
        for i in range(len(img_list)):
            if img_list[i] == id:
                url = mots[10]
                url_list.append(url)

    return url_list

def printURL(url_list):
    print(url_list)

if parser_arguments().command == 'listClasses':
    print("List of all classes.")
    getListClasses()

if parser_arguments().command == 'getURL':
    if parser_arguments().classes is None:
        print('Missing classes argument')
        exit (1)
    else:
        print("Get URL of {} class.".format(parser_arguments().classes))
        printURL(getImgURL(getImgList(getIdClass())))


    if parser_arguments().limit is None:
        print('Missing the desired number of images')
        exit (1)

def getMetadata(img_list):
    """
    Access to image's metadata of the images in the list
    :return : list of dictionnary with url / author / title / Original size / original MD5
    """
    f = open('csv_files/test-images-with-rotation.csv',"r",encoding='utf8')
    list_d = []
    d = dict()
    for l in f:
        mots = l.split(",")
        id = mots[0]
        for i in range(len(img_list)):
            if img_list[i] == id:
                d['url'] = mots[10].lower()
                d['author'] = mots[6].lower()
                d['title'] = mots[7].lower()
                d['size'] = mots[8].lower()
                d['mdfive'] = mots[9].lower()
                list_d.append(d) # Dictionnary added to list
                d={} # New dictionnary initialized for the next image

    return list_d
    # Returns a list of dictionnaries, each containing the metadata of an image in the list

def getPath():
    name = "-".join(parser_arguments().classes)
    path = os.path.abspath(name)
    return path

def mkdir ():
    """
    Create a repository at the name of the requested class
    to put all the downloaded images.
    """
    name = "-".join(parser_arguments().classes)
    if not os.path.exists(name):
        os.mkdir(name)
        print('The repository {} have been created'.format(parser_arguments().classes))
    else:
        print('The repository {} already exists.'.format(parser_arguments().classes))
        pass

def downloadLocal(url_list,path):
    """
    Download the image with the url of the list
    """
    print("You are downloading {} images".format(parser_arguments().limit),end=" ");print("of {} class.".format(parser_arguments().classes))
    print("Please, be patient :)")
    for i in range(len(url_list)):
        filename= url_list[i].split("/")[-1] # name of the picture file
        r = requests.get(url_list[i], stream =True)
        print(filename)

        with open(filename,'wb') as f : # create the file locally in binary-write mode
            r = requests.get(url_list[i], stream =True)
            shutil.copyfileobj(r.raw, f) #write our image to the file
            shutil.move(filename,path)
    print('Done!')

def getEndpoint():
    print("Please, identify yourself.")
    url = input("Port number : ")
    url = 'localhost:'+url
    return url

def getID():
    ID = getpass.getpass("Enter your username : ")
    return ID

def getMP():
    MP = getpass.getpass("Enter your password : ")
    return MP

def getMinioClient(url,ID,MP):
    """
    Minio Client initialisation
    """
    return Minio(
        url,
        access_key= ID,
        secret_key= MP,
        secure=False
    )

if parser_arguments().command == 'downloader':
    if parser_arguments().classes is None:
        print('Missing classes argument')
        exit (1)

    if parser_arguments().limit is None:
        print('Missing the desired number of images')
        exit (1)

    if parser_arguments().location is None:
        print("Missing download location")
        exit(1)

    if parser_arguments().location is not None:
        location = "-".join(parser_arguments().location)
        location = location.lower()
        if location == 'local':
            mkdir()
            downloadLocal(getImgURL(getImgList(getIdClass())),getPath())
            exit(1)

if __name__ == "__main__":

    minioClient = getMinioClient(getEndpoint(),getID(),getMP())

    def makeBucket():
        """
        Create a bucket at the name of the requested class in the Minio server
        """
        name = "-".join(parser_arguments().classes)
        name = name.lower()
        if(not minioClient.bucket_exists(name)):
            minioClient.make_bucket(name)
            print('The bucket {} have been created'.format(parser_arguments().classes))
        else:
            print('The bucket {} already exists.'.format(parser_arguments().classes))
            pass

    def downloadMinio(url_list,list_d,threads = 5):
        """
        Download the image and its metadata with the url of the list
        """
        print("You are downloading {} images".format(parser_arguments().limit),end=" ");print("of {} class.".format(parser_arguments().classes))
        print("Please, be patient :)")
        name = "-".join(parser_arguments().classes)
        name = name.lower()
        pool = ThreadPool(10)
        for i in range(len(url_list)):
            filename= url_list[i].split("/")[-1] # name of the picture file
            r = requests.get(url_list[i], stream =True)


            if r.status_code == 200:
                r.raw.decode_content = True

                with open(filename,'wb') as f : # create the file locally in binary-write mode
                    metadata = list_d[i]
                    r = requests.get(url_list[i], stream =True)
                    shutil.copyfileobj(r.raw, f) #write our image to the file
                    path = os.getcwd()+'/'+filename # image path
                    minioClient.fput_object(name,filename,path,'image/jpg',metadata)
                    os.remove(filename)
                    print(filename,'have been successfuly uploaded')

        pool.close()
        pool.join()
        print('Done!')

        if parser_arguments().location is not None:
            location = "-".join(parser_arguments().location)
            location = location.lower()

            if location == 'minio':
                makeBucket()
                downloadMinio(getImgURL(getImgList(getIdClass())), getMetadata(getImgList(getIdClass())))
                exit(1)
