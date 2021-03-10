from src.file_handler import createCsv, CreateDir, writeImg, addToCsv
from src.setting import BTS_BASE, BTS_CATALOGUE, BTS_HOME
from requests import get
from re import search, sub
from bs4 import BeautifulSoup


def addBookData(url):
    """Stocke les différentes données d'un livre depuis son url
    Puis les ajoutes dans un fichier csv et télecharge son image

    Args:
        url (str): url du livre
    """

    response = get(url)

    if not response.ok:
        print('Error response is not 200')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text

    table = soup.findAll('tr')

    upc = table[0].find('td').text

    price_excluding_tax = table[2].find('td').text
    price_excluding_tax = price_excluding_tax[1:]

    price_including_tax = table[3].find('td').text
    price_including_tax = price_including_tax[1:]

    number_avaible = table[5].find('td').text
    number_avaible = search(r'\d+', number_avaible).group()

    rating = soup.find('article').findAll('p')
    for node in rating:
        if search('star-rating', str(node['class'])):
            rating = node['class']
            rating = rating[1]
            break

    img_url = soup.find('img')
    img_url = img_url['src']
    img_url = BTS_BASE + sub("../", "", img_url, 2)

    category = soup.find('ul', {'class': 'breadcrumb'}).findAll('li')
    category = category[2].find('a').text

    desc_proof = soup.find('div', {'id': "product_description"})
    product_description = ''
    if desc_proof is not None:
        description_finder = soup.find('article')
        description_finder = description_finder.findAll('p')
        for x in description_finder:
            if x.get('class') is None:
                product_description = x.text
                break

    table = []
    table.append(url)
    table.append(upc)
    table.append(title)
    table.append(price_including_tax)
    table.append(price_excluding_tax)
    table.append(number_avaible)
    table.append(product_description)
    table.append(category)
    table.append(rating)
    table.append(img_url)

    addToCsv(table, category)
    writeImg(img_url, title)


def getAllBooksFromCategory(url, category_name, index):
    """Parcoure tous les livres d'une catégories pour stocker leur url respectif
    Puis on passe dans la fonctions addBookData chaque lien stocké


    Args:
        url (str): Url de la catégorie
        category_name (str): Nom de la catégorie
        index (int): indice de recursivité
    """

    response = get(url)

    if not response.ok:
        print('Error response is not 200')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    nbr_result = soup.find('form').find('strong').text

    bookList = soup.find('ol').findAll('li')

    if index == 0:
        createCsv(category_name)

    for book in bookList:
        book = book.find('a')
        book = book['href']
        bookUrl = search(r'[\w,.,-]*[/][\w,.,-]*$', book)
        bookUrl = BTS_CATALOGUE + bookUrl[0]
        print(bookUrl)
        addBookData(bookUrl)

    if int(int(nbr_result)/20 - (index)) > 0:
        pager = soup.findAll('ul')
        page_link = ''
        for page in pager:
            if page.get('class') is not None \
                    and page.get('class') == ['pager']:
                page_link = page.findAll('li')
                for link in page_link:
                    if link.get('class') is not None and \
                            link.get('class') == ['next']:
                        page_link = link.find('a')
                        page_link = page_link['href']
                        break
                break

        url = sub(r'[\w,.,-]*$', page_link, url, 1)
        getAllBooksFromCategory(url, category_name, index+1)


def getAllBookFromAllCategory():
    """Stock le lien de chaque catégorie du site
    Que l'on passe a la fonction GetAllBookFromCategory
    """

    CreateDir()

    response = get(BTS_HOME)

    if not response.ok:
        print('Error response is not 200')
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    nav = soup.find('aside').find('ul').find('ul').findAll('li')

    for category in nav:
        category = category.find('a')
        category_name = search(r'([\w]+[ {1}]*)+', category.text).group()
        category_link = BTS_BASE + str(category['href'])
        getAllBooksFromCategory(category_link, category_name, 0)


print(__name__ + " was imported")
