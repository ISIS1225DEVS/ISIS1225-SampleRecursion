"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """

import random
import config as cf
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import shellsort as sa
assert cf

"""
Se define la estructura de un catálogo de libros.
El catálogo tendrá tres listas, una para libros, otra para autores
y otra para géneros
"""

# Construccion de modelos


def newCatalog():
    """
    Inicializa el catálogo de libros. Crea una lista vacia para guardar
    todos los libros, adicionalmente, crea una lista vacia para los autores,
    una lista vacia para los generos y una lista vacia para la asociación
    generos y libros. Retorna el catalogo inicializado.
    """
    catalog = {"books": None,
               "authors": None,
               "tags": None,
               "book_tags": None}

    catalog["books"] = lt.newList("ARRAY_LIST",
                                  cmpfunction=comparebooks)
    catalog["authors"] = lt.newList("SINGLE_LINKED",
                                    cmpfunction=compareauthors)
    catalog["tags"] = lt.newList("SINGLE_LINKED",
                                 cmpfunction=comparetagnames)
    catalog["book_tags"] = lt.newList("ARRAY_LIST")

    return catalog


# Funciones para agregar informacion al catalogo

def addBook(catalog, book):
    # Se adiciona el libro a la lista de libros
    lt.addLast(catalog["books"], book)
    # Se obtienen los autores del libro
    authors = book["authors"].split(",")
    # Cada autor, se crea en la lista de libros del catalogo, y se
    # crea un libro en la lista de dicho autor (apuntador al libro)
    for author in authors:
        addBookAuthor(catalog, author.strip(), book)
    return catalog


def addBookAuthor(catalog, authorname, book):
    """
    Adiciona un autor a lista de autores, la cual guarda referencias
    a los libros de dicho autor
    """
    authors = catalog["authors"]
    posauthor = lt.isPresent(authors, authorname)
    if posauthor > 0:
        author = lt.getElement(authors, posauthor)
    else:
        author = newAuthor(authorname)
        lt.addLast(authors, author)
    lt.addLast(author["books"], book)
    return catalog


def addTag(catalog, tag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newTag(tag["tag_name"], tag["tag_id"])
    lt.addLast(catalog["tags"], t)
    return catalog


def addBookTag(catalog, booktag):
    """
    Adiciona un tag a la lista de tags
    """
    t = newBookTag(booktag["tag_id"], booktag["goodreads_book_id"])
    lt.addLast(catalog["book_tags"], t)
    return catalog


# Funciones para creacion de datos

def newAuthor(name):
    """
    Crea una nueva estructura para modelar los libros de
    un autor y su promedio de ratings
    """
    author = {"name": "", "books": None,  "average_rating": 0}
    author["name"] = name
    author["books"] = lt.newList("ARRAY_LIST")
    return author


def newTag(name, id):
    """
    Esta estructura almancena los tags utilizados para marcar libros.
    """
    tag = {"name": "", "tag_id": ""}
    tag["name"] = name
    tag["tag_id"] = id
    return tag


def newBookTag(tag_id, book_id):
    """
    Esta estructura crea una relación entre un tag y
    los libros que han sido marcados con dicho tag.
    """
    booktag = {"tag_id": tag_id, "book_id": book_id}
    return booktag


# Funciones de consulta

def getBooksByAuthor(catalog, authorname):
    """
    Retorna un autor con sus libros a partir del nombre del autor
    """
    posauthor = lt.isPresent(catalog["authors"], authorname)
    if posauthor > 0:
        author = lt.getElement(catalog["authors"], posauthor)
        return author
    return None


def getBestBooks(catalog, number):
    """
    Retorna los mejores libros
    """
    books = catalog["books"]
    bestbooks = lt.newList()
    for cont in range(1, number+1):
        book = lt.getElement(books, cont)
        lt.addLast(bestbooks, book)
    return bestbooks


def countBooksByTag(catalog, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    tags = catalog["tags"]
    bookcount = 0
    pos = lt.isPresent(tags, tag)
    if pos > 0:
        tag_element = lt.getElement(tags, pos)
        if tag_element is not None:
            for book_tag in lt.iterator(catalog["book_tags"]):
                if tag_element["tag_id"] == book_tag["tag_id"]:
                    bookcount += 1
    return bookcount


def bookSize(catalog):
    return lt.size(catalog["books"])


def authorSize(catalog):
    return lt.size(catalog["authors"])


def tagSize(catalog):
    return lt.size(catalog["tags"])


def bookTagSize(catalog):
    return lt.size(catalog["book_tags"])


# Funciones utilizadas para comparar elementos dentro de una lista

def compareauthors(authorname1, author):
    if authorname1.lower() == author["name"].lower():
        return 0
    elif authorname1.lower() > author["name"].lower():
        return 1
    return -1


def comparetagnames(name, tag):
    if (name == tag["name"]):
        return 0
    elif (name > tag["name"]):
        return 1
    return -1


def comparebooks(bookid1, book):
    if bookid1 == book["goodreads_book_id"]:
        return 0
    elif bookid1 > book["goodreads_book_id"]:
        return 1
    return -1


# funciones para comparar elementos dentro de algoritmos de ordenamientos

def compareISBN(book1, book2):
    # TODO modificar operador de comparacion lab 4
    return (str(book1["isbn13"]) > str(book2["isbn13"]))


# Funciones de ordenamiento

def sortBooks(catalog):
    # TODO completar los cambios del return en el sort para el lab 5
    # toma la lista de libros del catalogo
    books = catalog["books"]
    # ordena la lista de libros
    sorted_list = sa.sort(books, compareISBN)
    # actualiza la lista de libros del catalogo
    catalog["books"] = sorted_list
    return sorted_list


def shuffleBooks(catalog):
    # TODO completar los cambios del return en el sort para el lab 5
    # toma la lista de libros del catalogo
    books = catalog["books"]
    element_num = lt.size(books)
    # creo la nueva lista desordenada vacia
    shuffled_list = lt.newList("ARRAY_LIST",
                               cmpfunction=comparebooks)
    i = 0
    # itero la lista de libros y agrego un libro aleatorio a la nueva lista
    while i < element_num:
        # reviso el numero de libros
        tsize = lt.size(books)
        # selecciono un indice aleatorio de un libro
        ridx = random.randint(1, tsize)
        # agregro el libro a la nueva lista y lo elimino de la lista original
        lt.addLast(shuffled_list, lt.getElement(books, ridx))
        lt.deleteElement(books, ridx)
        i += 1
    # actualizo la lista de libros del catalogo
    catalog["books"] = shuffled_list
    return shuffled_list


# Funciones de busqueda

def findBookByISBN(catalog, bookisbn, low, high):
    # TODO implementar recursivamente binary search para el lab 5
    # Se obtiene la lista de libros del catalogo
    books = catalog["books"]
    # si los limites son correctos
    if high >= low:
        # se obtiene el libro de la mitad
        mid = (high + low) // 2
        tb = lt.getElement(books, mid)
        # retorna la posicion si el ISBN del libro es igual al que se busca
        if tb["isbn13"] == bookisbn:
            return mid
        # si el ISBN del libro es mayor al de busqueda, va ala mitad inferior
        elif tb["isbn13"] < bookisbn:
            return findBookByISBN(catalog, bookisbn, low, mid - 1)
        # si el ISBN del libro es menor al de busqueda, va ala mitad inferior
        else:
            return findBookByISBN(catalog, bookisbn, mid + 1, high)
    # si la lista de libros esta vacia, retorna -1
    else:
        return -1


def recursiveFindBookByISBN(catalog, bookisbn):
    # TODO implementar la mascara de la busqueda recursiva para el lab 5
    # inicializa los limites de la lista de libros
    low = 1
    high = lt.size(catalog["books"])
    # ejecuta la busqueda recursiva
    bookidx = findBookByISBN(catalog, bookisbn, low, high)
    # preprocesa la respuesta
    book = None
    # si el libro existe, lo retorna
    if bookidx > 0:
        book = lt.getElement(catalog["books"], bookidx)
    # de lo contrario, devuelve None
    else:
        book = None
    return book


def iterativeFindBookByISBN(catalog, bookid):
    # TODO implementar iterativamente binary search para el lab 5
    # inicializa los limites de la lista de libros
    books = catalog["books"]
    print("buscando:", bookid)
    # el indice de las listas DISCLib empieza en 1
    low = 1
    high = lt.size(books)
    pos = -1
    found = False
    # itera mientras los limites sean correctos
    while (low <= high) and not found:
        # calcula la mitad
        mid = (low + high) // 2
        # toma el libro de la mitad
        tb = lt.getElement(books, mid)
        # print(tb["isbn13"])
        # retorna la posicion si el ISBN del libro es igual al que se busca
        if tb["isbn13"] == bookid:
            # print("encontre:", mid)
            pos = mid
            found = True
            # return mid
        # si el ISBN del libro es mayor al de busqueda, va ala mitad inferior
        elif tb["isbn13"] < bookid:
            high = mid - 1
        # si el ISBN del libro es menor al de busqueda, va ala mitad inferior
        else:
            low = mid + 1
    # si la lista de libros esta vacia, retorna -1
    book = None
    if pos > 0:
        book = lt.getElement(books, pos)
    return book


# funciones para calcular estadisticas

def AverageBookRatings(catalog, low, high):
    # TODO implementar recursivamente el calculo del promedio para el lab 5
    books = catalog["books"]
    if low < high:
        tr = float(lt.getElement(books, low)["average_rating"])
        _sum = tr + AverageBookRatings(catalog, low + 1, high)
        avg = _sum / (high - low + 1)
        return avg
    else:
        avg = float(lt.getElement(books, low)["average_rating"])
        return avg


def recursiveAvgBooksRating(catalog):
    low = 1
    high = lt.size(catalog["books"])
    return AverageBookRatings(catalog, low, high)


def iterativeAvgBooksRating(catalog):
    # TODO implementar iterativamente el calculo del promedio para el lab 5
    # inicializa la lista de libros y el promedio
    avg = 0
    books = catalog["books"]
    # itera sobre la lista de libros y suma los ratings
    for book in lt.iterator(books):
        avg += float(book["average_rating"])
    # calcula el promedio
    avg /= lt.size(books)
    # devuelve el promedio
    return avg
