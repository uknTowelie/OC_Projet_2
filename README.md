# Projet_2 Web Scrapping


Ce script permet de parcourire le site http://books.toscrape.com/ par catégorie de livre et d'enregistrer 
dans un fichier csv diffèrentes informations à propos de chaque livre (Titre, prix, image ...)

Les différents fichiers et images sont stockés dans les dossiers, générés automatiquement, nommés respectivement BookData et Img


# Setup environement

Pour installer l'environement virtuel 
<hr/>

Sous Linux :

    python3 -m venv .venv

Pour l'activer :
 
    source .venv/bin/activate
<hr/>

Sous Windows :
    
    py -3 -m venv .venv
    
Pour l'activer :

    .venv/scripts/activate

# Liste des modules ou packages à intsaller

Pour le télécharger : 
  
    pip install bs4
 
# Exécuter le programme

Pour l'éxecuter :

     python3 __main__.py


