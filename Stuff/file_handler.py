from requests import get
from csv import writer
from re import sub
from os import mkdir, path


def CreateDir():
    """Crée les dossiers BookData et Img si inexistant"""

    if not path.isdir('Stuff/BookData'):
        mkdir('Stuff/BookData')
        mkdir('Stuff/Img')
    else:
        print("Directory exist")


def createCsv(file_name):
    """Crée et initialise les colonnes d'un fichier csv

    Args:
        file_name (str): nom du fichier à créer
    """

    file_name = sub(r'\s', "_", file_name)
    with open("./Stuff/BookData/" + str(file_name) + '.csv',
              'w',
              newline='') as csv_file:
        f_writer = writer(csv_file)
        f_writer.writerow([
            'product_page_url',
            'upc',
            'title',
            'price_including_tax',
            'price_excluding_tax',
            'number_available',
            'product_description',
            'category',
            'review_rating',
            'image_url'
        ])


def addToCsv(table, file_name):
    """Ajoute les informations d'un livre a un fichier csv

    Args:
        table (multiple type): tableau qui contient
        les différentes informations d'un livre
        file_name (str): nom du fichier auquel on ajoute le contenu du tableau
    """

    file_name = sub(r'\s', "_", file_name)
    with open("./Stuff/BookData/" + str(file_name) + '.csv',
              'a',
              newline='') as csv_file:
        f_writer = writer(csv_file)
        f_writer.writerow([
            table[0],
            table[1],
            table[2],
            table[3],
            table[4],
            table[5],
            table[6],
            table[7],
            table[8],
            table[9]
        ])


def writeImg(img_url, book_name):
    """Télécharge et enregistre dans le dossier Img une image depuis son url

    Args:
        img_url (string): url de l'image a télécharger
        book_name (string): nom que portera le fichier image
    """

    book_name = sub(r'\s', "_", book_name)
    with open("./Stuff/Img/" + book_name + ".jpg", "wb") as f:
        f.write(get(img_url).content)


print(__name__ + " was imported")
