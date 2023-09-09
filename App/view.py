"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
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
 * Contribuciones
 *
 * Dario Correal
 """

import config as cf
import sys
# import resource
import gc
# TODO completar con las importaciones de threading lab 5 (parte 2)
# muere start
import threading
# muere end
import controller
from DISClib.ADT import list as lt
assert cf

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones  y  por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""


def newController():
    """
    Se crea una instancia del controlador
    """
    control = controller.newController()
    return control


def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los Top x libros por promedio")
    print("3- Consultar los libros de un autor")
    print("4- Libros por género")
    print("5- Ordenar los libros por ISBN")
    print("6- Desordenar los libros por ISBN")
    # TODO agregar opciones al menu del lab 5 (parte 2)
    # MUERE START
    print("7- Buscar un libro por ISBN")
    print("8- Calcular el rating promedio de libros")
    print("9- Recuperar el primer libro con un rating dado")
    print("10- Cambiar tipo de algoritmos (recursivos o iterativos)")
    # MUERE END
    print("0- Salir")


def loadData():
    """
    Solicita al controlador que cargue los datos en el modelo
    """
    books, authors, tags, book_tags = controller.loadData(control)
    return books, authors, tags, book_tags


def printAuthorData(author):
    if author:
        print("Autor encontrado: " + author["name"])
        print("Promedio: " + str(author["average_rating"]))
        print("Total de libros: " + str(lt.size(author["books"])))
        for book in lt.iterator(author["books"]):
            print("Titulo:", book["title"], "ISBN:", book["isbn13"])
    else:
        print("No se encontro el autor")


def printBestBooks(books):
    size = lt.size(books)
    if size:
        print(" Estos son los mejores libros: ")
        for book in lt.iterator(books):
            print("Titulo:", book["title"], "ISBN:",
                  book["isbn13"], "Rating:", book["average_rating"])
    else:
        print("No se encontraron libros")


def printSortResults(sort_books, sample=3):
    size = lt.size(sort_books)
    if size <= sample*2:
        print("Los", size, "libros ordenados son:")
        for book in lt.iterator(sort_books):
            print("Titulo:", book["title"], "ISBN:",
                  book["isbn13"], "Rating:", book["average_rating"])
    else:
        print("Los", sample, "primeros libros ordenados son:")
        i = 1
        while i <= sample:
            book = lt.getElement(sort_books, i)
            print("Titulo:", book["title"], "ISBN:",
                  book["isbn13"], "Rating:", book["average_rating"])
            i += 1

        print("Los", sample, "últimos libros ordenados son:")
        i = size - sample + 1
        while i <= size:
            book = lt.getElement(sort_books, i)
            print("Titulo:", book["title"], "ISBN:",
                  book["isbn13"], "Rating:", book["average_rating"])
            i += 1


def printSearchResults(book):
    # TODO completar funcion para imprimir resultados search lab 5
    # MUERE START
    if book is not None:
        print("El libro es: ")
        for key in book.keys():
            print("\t'" + key + "': ", book[key])
    else:
        print("El libro no se encuentra en la lista!!!")
    # MUERE END


# Se crea el controlador asociado a la vista
control = newController()


# configurando el limite de recursion
default_limit = 1000

# variables utoles para el programa
# opciones de true
bool_lt_opt = ("s", "S", "1", True, "true", "True", "si", "Si", "SI")


def menu_cycle():

    """
    Menu principal
    """
    working = True
    # configurando si usa algoritmos recursivos
    rec = True

    # ciclo del menu
    while working:
        printMenu()
        # liberar memoria
        gc.collect()
        inputs = input("Seleccione una opción para continuar\n")
        if int(inputs) == 1:
            print("Cargando información de los archivos ....")
            bk, at, tg, bktg = loadData()
            print("Libros cargados: " + str(bk))
            print("Autores cargados: " + str(at))
            print("Géneros cargados: " + str(tg))
            print("Asociación de Géneros a Libros cargados: " + str(bktg))

        elif int(inputs) == 2:
            number = input("Buscando los TOP ?: ")
            books = controller.getBestBooks(control, int(number))
            printBestBooks(books)

        elif int(inputs) == 3:
            authorname = input("Nombre del autor a buscar: ")
            author = controller.getBooksByAuthor(control, authorname)
            printAuthorData(author)

        elif int(inputs) == 4:
            label = input("Etiqueta a buscar: ")
            book_count = controller.countBooksByTag(control, label)
            print("Se encontraron: ", book_count, " Libros")

        elif int(inputs) == 5:
            # TODO completar modificaciones para el lab 5
            result = controller.sortBooks(control)
            delta_time = f"{result[0]:.3f}"
            sorted_list = result[1]
            size = lt.size(sorted_list)
            print("===== Los libros ordenados por ISBN son: =====")
            print("Para", size, "elementos, tiempo:", str(delta_time), "[ms]")
            printSortResults(sorted_list)

        elif int(inputs) == 6:
            # TODO completar modificaciones para el lab 5
            result = controller.shuffleBooks(control)
            delta_time = f"{result[0]:.3f}"
            shuffled_list = result[1]
            size = lt.size(shuffled_list)
            print("===== Los libros desordenados por ISBN son: =====")
            print("Para", size, "elementos, tiempo:", str(delta_time), "[ms]")
            printSortResults(shuffled_list)

        elif int(inputs) == 7:
            # TODO modificar opcion 7 del menu en el lab 5 (parte 2)
            # MUERE START
            isbn = input("Ingrese el ISBN del libro a buscar: ")
            isbn = int(isbn)
            result = controller.findBookByISBN(control,
                                               isbn,
                                               recursive=rec)
            delta_time = f"{result[0]:.3f}"
            book = result[1]
            print("===== El libro encontrado es: =====")
            print("Para encontrar el libro con ISBN", isbn,
                  ", tiempo:", str(delta_time), "[ms]")
            print("Algoritmo recursivo:", rec)
            printSearchResults(book)
            # MUERE END

        elif int(inputs) == 8:
            # TODO modificar opcion 8 del menu en el lab 5 (parte 2)
            # MUERE START
            result = controller.getBooksAverageRating(control,
                                                      recursive=rec)
            delta_time = f"{result[0]:.3f}"
            average = result[1]
            print("===== El rating promedio de los libros es: =====")
            print("Para", controller.bookSize(control), "elementos, tiempo:",
                  str(delta_time), "[ms]")
            average = f"{average:.3f}"
            print("Algoritmo recursivo:", rec)
            print("El rating promedio es:", average)
            # MUERE END

        elif int(inputs) == 9:
            # TODO modificar opcion 9 del menu en el lab 5 (parte 2)
            # MUERE START
            print("Filtra los libros con un rating entre dos valores")
            lower = float(input("Ingrese el rating mínimo: "))
            upper = float(input("Ingrese el rating máximo: "))
            result = controller.filterBooksByRating(control,
                                                    lower,
                                                    upper,
                                                    recursive=rec)
            print("===== Los libros entre", lower, "y", upper, "son: =====")
            delta_time = f"{result[0]:.3f}"
            filtered_list = result[1]
            size = lt.size(filtered_list)
            print("Para", size, "elementos, tiempo:", str(delta_time), "[ms]")
            print("Algoritmo recursivo:", rec)
            printSortResults(filtered_list)
            # MUERE END

        elif int(inputs) == 10:
            # TODO modificar opcion 10 del menu en el lab 5 (parte 2)
            # MUERE START
            # configurar si usa algoritmos recursivos
            rec = input("Usar algoritmos recursivos? (S/N): ")
            if rec in bool_lt_opt:
                rec = True
            else:
                rec = False
            # MUERE END

        elif int(inputs) == 0:
            working = False
            print("\nGracias por utilizar el programa.")

        else:
            # confirmar salida del programa
            end_str = "¿desea salir del programa? (s/n): "
            opt_usr = input(end_str)
            # diferentes opciones de salida
            if opt_usr in bool_lt_opt:
                working = False
                print("\nGracias por utilizar el programa.")
    sys.exit(0)


# main del ejercicio
if __name__ == "__main__":
    # # MUERE START
    threading.stack_size(67108864*2)  # 128MB stack
    sys.setrecursionlimit(default_limit*1000000)
    thread = threading.Thread(target=menu_cycle)
    thread.start()
    # # MUERE END
    # menu_cycle()
