# Third parties imports
import pandas as pd
from pathlib import Path
from tkinter import *
from tkinter import filedialog

# Creating Tk root
root = Tk()
# Hiding tkinter screen
root.withdraw()

print("¡Bienvenido!")
print(
    "¿Desea ingresar los datos desde un excel [1] o ingresarlos manualmente[2]?")

aux = 0
infiles = ""
option = 0
excel = True

# ask if by excel file or written
while True:
    try:
        option = int(input())
    except ValueError:
        print("Elija una opción válida, debe ser 1 o 2")
        print(
            "¿Desea ingresar los datos desde un excel [1] o ingresarlos manualmente[2]?")
        continue
    else:
        # validating if the option is 1 or 2
        if(option == 1 or option == 2):
            break
        else:
            print("Elija una opción válida, debe ser 1 o 2")
            print(
                "¿Desea ingresar los datos desde un excel [1] o ingresarlos manualmente[2]?")
            continue

if (option == 2):
    excel = False

# in case is not Excel, we have to ask all the data by console
while not excel:
    # first, we have to ask how many activities
    while True:
        print("¿Cuantas actividades ingresara? ")
        try:
            rows = int(input())
        except ValueError:
            print("Elija una opción válida, debe ser un numero")
            print("¿Cuantas actividades ingresara? ")
            continue
        else:
            if(option > 1):
                break
            else:
                print("Elija una opción válida, debe ser un numero")
                print("¿Cuantas actividades ingresara?")
                continue

    # we ask the use to introduce each activity with all the required data
    while True:
        print("A continuacion, ingrese los datos de la siguiente forma:")
        print("Identificador-Descripcion-Duracion-predecessors")
        print("Los predecessors, en caso de ser varios, seran separados por una coma ( , ). En el caso de no tenerlos, ingrese un punto (.)")
        print("Ejemplo:")
        print("A-Lijar la madera-5-.")
        aux = []
        for i in range(rows):
            print("Ingrese la actividad numero "+str(i + 1)+":")
            aux.append(input())
        break
    break


while excel:
    try:
        # open the window to select the file
        print("Por favor ingrese el archivo excel que desea leer")
        print("Recuerde que el archivo excel debe tener cuatro columnas con identificacion|descripcion|duracion|predecesor")

        infiles = filedialog.askopenfilename(multiple=True)

        if (infiles == ""):
            break

        # validate if it is an excel file
        if(str(infiles[0]).endswith('.xls') or str(infiles[0]).endswith('.xlsx')):
            archivo = infiles[0]

            # creating the dataframe
            data = pd.ExcelFile(archivo)
            df = data.parse()

            # the file must have four columns
            if(df.shape[1] != 4):
                print(
                    "El archivo no cuenta con las cuatro columnas, porfavor seleccione un archivo nuevo")
                continue
            else:
                for i in range(df.shape[0]):
                    if(isinstance(df["duracion"][i], str)):
                        aux = 1
                        break
                if(aux == 1):
                    print("Las duraciones deben ser numeros enteros")
                    continue
                else:
                    break

        else:
            print("El archivo debe ser un archivo Excel")
            continue
    except ValueError:
        print("El archivo debe ser un archivo Excel")
        continue


cont = False

if(infiles == "" and excel == True):
    print("No seleccionaste ningun archivo")
elif(infiles == "" and excel == False):
    # filling the matrix
    columns = 4
    matrix_data = []
    nodes = []
    cont = True

    for i in range(rows):
        matrix_data.append([])
        for j in range(columns):
            matrix_data[i].append("")

    # Save the info in the matrix
    for i in range(rows):
        tuplas = aux[i].split("-")
        for j in range(columns):
            if(j == 0):
                matrix_data[i][j] = tuplas[j]
                nodes.append(tuplas[j])
            if(j == 1):
                matrix_data[i][j] = tuplas[j]
            if(j == 2):
                matrix_data[i][j] = int(tuplas[j])
            if(j == 3):
                # if it is a dot, it doesnt have predecessors
                if(tuplas[j] == "."):
                    matrix_data[i][j] = [""]
                else:
                    matrix_data[i][j] = str(tuplas[j]).split(sep=",")

    cont = True

else:
    print("Archivo validado")
    # we fill the empty spaces in the df with null
    df = df.fillna("")

    # to know how many columns and rows, we will use shape
    rows = df.shape[0]
    columns = df.shape[1]
    matrix_data = []
    nodes = []
    cont = True

    # it's time to create the matrix mxn that will contain the data, it'll be a list of list
    for i in range(rows):
        matrix_data.append([])
        for j in range(columns):
            matrix_data[i].append("")

    # next, we fill the matrix with the data
    for i in range(rows):
        for j in range(columns):
            if(j == 0):
                matrix_data[i][j] = df["identificacion"][i]
                nodes.append(df["identificacion"][i])
            if(j == 1):
                matrix_data[i][j] = df["descripcion"][i]
            if(j == 2):
                matrix_data[i][j] = df["duracion"][i]
            if(j == 3):
                matrix_data[i][j] = str(df["predecessors"][i]).split(sep=",")

if(cont == True):
    visited = []    # List to keep track of visited nodes.
    queue = []  # Initialize a queue
    matrix = {}  # Initialize forward pass table structure
    matrix2 = {}  # Initialize backward pass table structure
    critic = []  # Initialize Critical Path array
    successors = {}  # Initialize successors table
    predecessors = {}  # Initialize predecessors table
    duraciones = {}

    # we fill the successors and predecessors' table
    for el in matrix_data:
        matrix2[el[0]] = {'earlyStart': 0, 'earlyFinish': 0,
                          'lateStart': 0, 'lateFinish': 0, 'slack': 0}
        matrix[el[0]] = {'earlyStart': 0, 'earlyFinish': 0,
                         'lateStart': '-', 'lateFinish': '-', 'slack': '-'}
        duraciones[el[0]] = int(el[2])

        if(el[3] != ['']):
            predecessors[el[0]] = el[3]

        else:
            # we have to identify the origin node
            predecessors[el[0]] = []

        for item in el[3]:
            if item in successors:
                if(item != ['']):
                    aux = successors[item]
                    aux.append(el[0])
                    successors[item] = aux
            else:
                if(item != ""):
                    aux1 = []
                    aux1.append(el[0])
                    successors[item] = aux1

    # and the last activity, won't have a successor
    last = list(set(nodes)-set(successors.keys()))
    successors[last[0]] = []

    # the forward pass will be done with BFS
    def forward(visited, duraciones, graph, node):

        # each time we visit a node, we have to add it to the list and the queue
        visited.append(node)
        queue.append(node)

        # setting the initial values
        ES = 0
        EF = 0
        predecesor = []

        # as long the queue is not empty
        while queue:
            # get the next node that is waiting
            s = queue.pop(0)

            if len(predecesor) > 0:
                if s in matrix:
                    # the EF of the predecessors have to be compared to select the bigger value, this will be the ES of the node that we are visiting
                    if matrix[predecesor[0]]['earlyFinish'] > matrix[s]['earlyStart']:
                        ES = matrix[predecesor[0]]['earlyFinish']
                    else:
                        ES = matrix[s]['earlyStart']
                else:
                    ES = matrix[predecesor[0]]['earlyFinish']
                element = {'earlyFinish': ES+duraciones[s], 'earlyStart': ES,
                           'lateStart': '-', 'lateFinish': '-', 'slack': '-'}
            else:
                element = {'earlyFinish': EF+duraciones[s], 'earlyStart': ES,
                           'lateStart': '-', 'lateFinish': '-', 'slack': '-'}

            matrix[s] = (element)
            if(len(predecesor) > 0):
                predecesor.pop(0)

            # we have to visit the neighbors
            for neighbor in graph[s]:
                predecesor.append(s)
                visited.append(neighbor)
                queue.append(neighbor)

    # the backward pass will be done with BFS too
    def backward(visited, duraciones, graph, node):

        # this is pretty much the same as the forward pass but with some twists
        visited.append(node)
        queue.append(node)

        LF = 0
        LS = 0
        predecesor = []

        while queue:
            s = queue.pop(0)

            if len(predecesor) > 0:
                if matrix2[s]['lateFinish'] != 0:

                    # the LS of the node is compared to select the smaller value to be the LF of the visited node
                    if matrix2[predecesor[0]]['lateStart'] < matrix2[s]['lateFinish']:
                        LF = matrix2[predecesor[0]]['lateStart']
                    else:
                        LF = matrix2[s]['lateFinish']
                else:
                    LF = matrix2[predecesor[0]]['lateStart']
                LS = LF-duraciones[s]
                slack = LF-matrix[s]['earlyFinish']
                element = {'earlyStart': matrix[s]['earlyStart'], 'earlyFinish': matrix[s]
                           ['earlyFinish'], 'lateStart': LS, 'lateFinish': LF, 'slack': slack}
            else:
                LF = matrix[s]['earlyFinish']
                LS = LF-duraciones[s]
                slack = LF-matrix[s]['earlyFinish']
                element = {'earlyStart': matrix[s]['earlyStart'], 'earlyFinish': matrix[s]
                           ['earlyFinish'], 'lateStart': LS, 'lateFinish': LF, 'slack': slack}

            if(slack == 0 and s not in critic):
                # if the slack time is the same as 0, it means that it is part of the critical path
                critic.insert(0, s)

            matrix2[s] = (element)

            if(len(predecesor) > 0):
                predecesor.pop(0)

            for neighbor in graph[s]:
                predecesor.append(s)
                visited.append(neighbor)
                queue.append(neighbor)

    forward(visited, duraciones, successors, matrix_data[0][0])
    backward(visited, duraciones, predecessors,
             matrix_data[len(matrix_data)-1][0])

    forwardPass = pd.DataFrame.from_dict(matrix, orient="index")
    backwardPass = pd.DataFrame.from_dict(matrix2, orient="index")
    criticalPath = pd.DataFrame({'Critical Path': critic})

    print('------------')
    print('Forward Pass')
    print('')
    print(forwardPass)
    print('')
    print('-------------')
    print('Backward Pass')
    print('')
    print(backwardPass)
    print('')
    print('-------------')
    print('La ruta critica es' + str(critic))