import os # importation du module os

from flask import Flask #importation de la classe Flask dans le module flask
from flask import render_template # importation de la méthode render_template du module flask
from flask import request # importation de la methode request du module flask
from flask import redirect # importation de la methode redirect du module flask

from flask_sqlalchemy import SQLAlchemy # importation de la classe SQLAlchemy dans le module flask_sqlalchemy
from sqlalchemy import or_ # importation  de la méthode or_ dans sqlalchemy

project_dir = os.path.dirname(os.path.abspath(__file__)) #récupérer le chemin du ficher
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))# permet d'implémenter la base de donnée dans le fichier
# et s'il n'existe pas il la crée


app = Flask(__name__)# initialisation de   l'application
app.config["SQLALCHEMY_DATABASE_URI"] = database_file # On configure la base de donnée de l'application
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # on empêche l'avertisssement lors d'une modification dans la base de donnée

db = SQLAlchemy(app)# Intégration de SQLAlchemy dans notre application

class Book(db.Model):# création du modèle de base de donnée
    id = db.Column(db.Integer,  primary_key=True , unique=True)# on donne la forme de la clé primaire id qui est unique
    edition = db.Column(db.String(1000))# on donne la forme de l'edition
    title = db.Column(db.String(1000), nullable=False)# on donne la forme du title
    author = db.Column(db.String(1000))# on donne la forme de l'author
    year_of_publication = db.Column(db.String(100), nullable=False)# on donne la forme de year_of_publication


    def __repr__(self):# on crée une méthode qui nous permet de repésenter la classe Book
        return {'title':self.title,'edition':self.edition} # retourne un dictionnaire comme représentation


@app.route("/", methods=["GET", "POST"])# Nous permet de lier lier l'action "./" qui est au niveau de html
# à la fonction qu'on va créer à la ligne suivante
def home(a = 'disabled'):# on crée une fonction home
    books = None # on initialise une variable books vide

    if request.form:# on pose une condition sur la requête
        try:
            book = Book(title=request.form.get("title"),edition=request.form.get("edition"),\
                        author=request.form.get("author"),year_of_publication=request.form.get(str("year_of_publication")))
            # recupération des donnéee utlisateur pour construire un élément de type Book
            db.session.add(book) # ajouter l'élément dans la base de donnée
            db.session.commit()# on actualise la base de donnée
        except Exception as e: # configuration des exception
            print("Failed to add book")
            print(e)
    books = Book.query.all() # Recupère tous les élèments de type Book
    return render_template("home.html", books=books , a=a) #retourne les résultats obtenu au templates

@app.route("/update", methods=["POST"])# Nous permet de lier l'action "./update"
# qui est au niveau de html à la fonction qu'on va créer à la ligne suivante
def update():
    try:
        id = request.form.get("id")# permet de récupérer la valeur de l'élément nommé id au niveau de html
        newtitle = request.form.get("newtitle")# permet de récupérer la valeur de l'élément nommé newtiltle au niveau de html
        newauther = request.form.get("newauthor")# permet de récupérer la valeur de l'élément nommé newauthor au niveau de html
        newedition = request.form.get("newedition")# permet de récupérer la valeur de l'élément nommé newedition au niveau de html
        newyear_of_publication = request.form.get(str("newyear_of_publication"))# permet de récupérer la valeur de l'élément
        # nommé year_of_publication au niveau de html et de le caster en str
        #tous les élèments récupérés doit être dans le form d'action = './'
        book = Book.query.filter_by(id=id).first()#permet de récupérer le premier élément de type book dont le book.id = id
        book.title = newtitle # reaffectation du title du livre
        book.author = newauther # reaffectation du title du  author
        book.edition = newedition # reaffectation du title de l'edition
        book.year_of_publication = newyear_of_publication # reaffectation de l'année de puiblication du llivre
        db.session.commit()# enregistrement des données
    except Exception as e:#configuration des exceptions
        print("Couldn't update book title")
        print(e)
    return redirect("/")# effectue l'action '/'


@app.route("/delete", methods=["POST"])# nous permet de lier l'action "./delete" de html a la fonction qu'on va créer
def delete():
    id = request.form.get("id")# permet de récupérer la valeur de l'élément nommé id au niveau de html
    # dans le form d'action = "./update"
    book = Book.query.filter_by(id=id).first() #permet de récupérer le premier élément de type book dont le book.id = id
    db.session.delete(book)# effacer le livre de la base de donnée
    db.session.commit()# eneregistrer les modifications
    return redirect("/")# effectue l'action '/'


@app.route("/edit", methods=["POST"])# liaison de du buton edit de html a la fonction ci-dessous
def edit():
    return home(a="able")


@app.route("/delete_all", methods=["POST"])# nous permet de lier l'action "./delete_all" de html a la fonction qu'on va créer
def delete_all():
    books = Book.query.all()#permet tous les éléments de type Book
    for book in books:# création d'une boucle qui parcourt les éléments du type Book
        db.session.delete(book)# effacer chacun de tous les élèments du type Book
    db.session.commit()# enregistrer les modifications
    return redirect("/")# effectue l'action '/'

@app.route("/search", methods=["POST","GET"])# nous permet de lier l'action "./search" de html a la fonction qu'on va créer
def search():
    search_month = request.form.get(str("search_month"))# permet de récupérer la valeur de l'élément
        # nommé search_month au niveau de html et de le caster en str
    search_name  = request.form.get("search_name")# permet de récupérer la valeur de l'élément nommé
    # search_name au niveau de html

    if search_month!='' and search_name!='':#condition de recherche
        books =  Book.query.filter(or_(Book.title==search_name,Book.edition==search_name,\
                                       Book.author==search_name,Book.year_of_publication==search_month))
        #filtrage des éléments de books par title ou edition ou author ou year_of_publication
        return render_template("home.html", books=books ,a='disabled')#retourne les résultats obtenu au templates
    elif search_name!='':
        books = Book.query.filter(or_(Book.title==search_name,Book.edition==search_name,Book.author==search_name))
        #filtrage par title ,author et edition
        return render_template("home.html", books=books,a='disabled')#retourne les résultats obtenu au templates
    elif search_month!='':
        books = Book.query.filter_by(year_of_publication=search_month)
        #filtrage par date
        return render_template("home.html", books=books,a='disabled')#retourne les résultats obtenu au templates
    else:
        return redirect("/")# effectue l'action '/'



if __name__ == "__main__":# point d'entrée de l'application
    db.create_all()#création de la table a partir des modèle
    app.run(host='0.0.0.0', port=8087, debug=True)# démarre l'application et lui définit le port "8087" et affiche le debuggeur en cas d'erreur
