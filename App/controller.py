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
 * Contribuciones
 *
 * Dario Correal
 """

import config as cf
import model
import time
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


# Inicialización del controller

def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        "model": None
    }
    control["model"] = model.newCatalog()
    return control


# Funciones para la carga de datos

def loadData(control):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    catalog = control["model"]
    books, authors = loadBooks(catalog)
    tags = loadTags(catalog)
    booktags = loadBooksTags(catalog)
    return books, authors, tags, booktags


def loadBooks(catalog):
    """
    Carga los libros del archivo.  Por cada libro se toman sus autores y por
    cada uno de ellos, se crea en la lista de autores, a dicho autor y una
    referencia al libro que se esta procesando.
    """
    # TODO cambiar nombre del archivo (parte 1)
    booksfile = cf.data_dir + "GoodReads/books-small.csv"
    input_file = csv.DictReader(open(booksfile, encoding="utf-8"))
    for book in input_file:
        # preprocesamiento de los datos para convertirlos al tipo correcto
        if book["isbn13"] not in (None, ""):
            book["isbn13"] = int(float(book["isbn13"]))
        else:
            book["isbn13"] = 0
        model.addBook(catalog, book)
    return model.bookSize(catalog), model.authorSize(catalog)


def loadBooksTags(catalog):
    """
    Carga la información que asocia tags con libros.
    """
    # TODO cambiar nombre del archivo (parte 1)
    booktagsfile = cf.data_dir + "GoodReads/book_tags-small.csv"
    input_file = csv.DictReader(open(booktagsfile, encoding="utf-8"))
    for booktag in input_file:
        model.addBookTag(catalog, booktag)
    return model.bookTagSize(catalog)


def loadTags(catalog):
    """
    Carga todos los tags del archivo y los agrega a la lista de tags
    """
    tagsfile = cf.data_dir + "GoodReads/tags.csv"
    input_file = csv.DictReader(open(tagsfile, encoding="utf-8"))
    for tag in input_file:
        model.addTag(catalog, tag)
    return model.tagSize(catalog)


# Funciones de ordenamiento

def sortBooks(control):
    """
    Ordena los libros por average_rating y toma el los tiempos en los
    que se inició la ejecución del requerimiento y cuando finalizó
    con getTime(). Finalmente calcula el tiempo que demoró la ejecución
    de la función con deltaTime()
    """
    # TODO examinar el redireccionamiento (parte 1)
    start_time = getTime()
    sorted_list = model.sortBooks(control['model'])
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return delta_time, sorted_list


def shuffleBooks(control):
    """
    Desordena los libros por average_rating y toma el los tiempos en los
    que se inició la ejecución del requerimiento y cuando finalizó
    con getTime(). Finalmente calcula el tiempo que demoró la ejecución
    de la función con deltaTime()
    """
    # TODO examinar el redireccionamiento (parte 1)
    start_time = getTime()
    unsorted_list = model.shuffleBooks(control['model'])
    end_time = getTime()
    delta_time = deltaTime(start_time, end_time)
    return delta_time, unsorted_list


# Funciones de consulta sobre el catálogo

def getBooksByAuthor(control, authorname):
    """
    Retrona los libros de un autor
    """
    author = model.getBooksByAuthor(control["model"], authorname)
    return author


def getBestBooks(control, number):
    """
    Retorna los mejores libros
    """
    bestbooks = model.getBestBooks(control["model"], number)
    return bestbooks


def countBooksByTag(control, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    return model.countBooksByTag(control["model"], tag)


def bookSize(control):
    """
    Retorna el número de libros
    """
    return model.bookSize(control["model"])


def authorSize(control):
    """
    Retorna el número de autores
    """
    return model.authorSize(control["model"])


def tagSize(control):
    """
    Retorna el número de tags
    """
    return model.tagSize(control["model"])


def bookTagSize(control):
    """
    Retorna el número de libros etiquetados
    """
    return model.bookTagSize(control["model"])


# funciones de busqueda

def findBookByISBN(control, isbn, recursive=True):
    """
    Busca un libro por su ISBN
    """
    # inicializa el tiempo de procesamiento
    star_time = getTime()
    # Analiza si se desea realizar la busqueda recursiva o iterativamente e invoca a la funcion correspondiente
    if recursive:
        book = model.searchBookByISBN(control["model"],
                                isbn)
    else:
        book = model.iterativeSearchBookByISBN(control["model"],
                                isbn)
    stop_time = getTime()
    # retorna el tiempo de procesamiento y el libro encontrado
    delta_time = deltaTime(star_time, stop_time)
    return delta_time, book


# Funciones para calcular estadísticas

def getBooksAverageRating(control, recursive=True):
    """
    Retorna el promedio de los ratings de los libros
    """
    # inicializa el tiempo de procesamiento
    star_time = getTime()
    # Analiza si se desea realizar obtener el promedio recursiva o iterativamente e invoca a la funcion correspondiente
    if recursive:
        avg = model.AvgBooksRatings(control["model"])
    else:
        avg = model.iterativeAvgBooksRating(control["model"])

    end_time = getTime()
    # retorna el tiempo de procesamiento y el promedio
    delta_time = deltaTime(star_time, end_time)
    return delta_time, avg


# funciones para filtrar libros

def filterBooksByRating(control, lower, upper, recursive=True):
    """
    Retorna los libros que tienen un rating entre lower y upper
    """
    star_time = getTime()
    # Analiza si se desea realizar el filtro recursiva o iterativamente e invoca a la funcion correspondiente.
    if recursive:
        books = model.filterBooksByRating(control["model"], lower, upper)
    else:
        books = model.iterativeFilterBooksByRating(control["model"], lower, upper)
    end_time = getTime()
    # retorna el tiempo de procesamiento y los libros encontrados
    delta_time = deltaTime(star_time, end_time)
    return delta_time, books


# Funciones para medir tiempos de ejecucion

def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
