import numpy as np
import matplotlib.pyplot as plt
from sympy import *

# Set x as symbol for math functions
x = Symbol('x')

# Second derivative function. In input the math function and point value
def secondDerivative(function, value):

    for i in range(0, 2):   # Calc of derivative two times
        function = function.diff(x)

    function = lambdify(x, function)    # Make the math function an executable function, so given a numeric input, it give the numeric result

    value = function(value)     # Numeric result of the input value

    return value

# Fourth derivative function
def fourthDerivative(function, value):

    for i in range(0, 4):   # Calc of derivative four times
        function = function.diff(x)

    function = lambdify(x, function)    # Make the math function an executable function, so given a numeric input, it give the numeric result

    value = function(value)     # Numeric result of the input value

    return value

# Trapezoidal rule plot function
def trapeziPlot(functionLambda, a, b, n, xValues):

    X = np.linspace(a, b, 100)      # Creation of an X axis with 100 points
    Y = functionLambda(X)       # Creation of a correspondent Y axis with point calculeted from the function
    plt.plot(X, Y)      # Plot of the function

    for i in range(n):      # Plot of trapezes
        xs = [xValues[i], xValues[i], xValues[i+1], xValues[i+1]]      
        ys = [0, functionLambda(xValues[i]), functionLambda(xValues[i+1]), 0]
        plt.fill(xs, ys, 'b', edgecolor='b', alpha=0.2)

    plt.show()

# Simpson rule plot function
def simpsonPlot(functionLambda, a, b, n, xValues):

    # Plot of the function
    X = np.linspace(a, b, 100)  
    Y = functionLambda(X)
    plt.plot(X, Y)

    for i in range(0, len(xValues)-1):      # Interpolation of second level (create a second degree function) for each interval and plotting
        
        xp = np.linspace(xValues[i], xValues[i+1], 3)
        yp = functionLambda(xp)

        z2 = np.polyfit(xp, yp, 2)
        p2 = np.poly1d(z2)

        subX = np.linspace(xValues[i], xValues[i+1], 100)
        
        plt.fill_between(subX, p2(subX))


    plt.show()

# Trapezoidal rule function
def trapezi(function, a, b, n):

    h = (b - a) / n     # Interval dimension
    xValues = np.linspace(a, b, n+1)    # Creation of n interval (points) between a and b (included)
    functionLambda = lambdify(x, function)      # Creation of a executable math function  
    
    s = functionLambda(a)   # Calc of values using trapezoidal algorithm
    for i in range(1, len(xValues)-1):
        s = s + 2 * functionLambda(xValues[i])
    s = s + functionLambda(b)  

    result = (h / 2) * s

    err = 0     # Calc of error using tapezoidal algorith for error
    for i in range(0, len(xValues)-1):    
        err = err + (-((h**3) / 12) * secondDerivative(function, xValues[i]))    
        #err = err + (-((b-a) / 12) * (h**2) * secondDerivative(function, xValues[i]))    

    print("Errore stimato: " + str(format(err, '.5f')))

    print("Approssimazione integrale: " + str(result) + "\n")

    trapeziPlot(functionLambda, a, b, n, xValues)

    return True

# Simpson rule function
def simpson(function, a, b, n):
    
    if(n % 2 != 0):     # Interval value must be even
        print('Il numero di sottointervalli per applicare Simpson deve essere pari')
        return False
    
    h = (b - a) / n     # Interval dimension
    xValues = np.linspace(a, b, n + 1)      # Creation of n interval (points) between a and b (included) 
    functionLambda = lambdify(x, function)      # Creation of a executable math function   

    s = 0       # Calc of values using simpson algorithm
    for i in range(1, len(xValues) -1):
        if(i % 2 == 0):
            s = s + 2 * functionLambda(xValues[i])
        else:
            s = s + 4 * functionLambda(xValues[i])
    
    s = s + functionLambda(a) + functionLambda(b)
    result = (h / 3) * s

    err = 0     # Calc of error using simpson algorith for error
    for i in range(0, len(xValues)-1):
        #err = err + (-(((h)**4) * (b - a) / 180) * fourthDerivative(function, xValues[i]))
        err = err + (-((1 / 90) * ((h / 2)**5) * fourthDerivative(function, xValues[i])))


    print("Errore stimato: " + str(format(err, '.9f')))

    print("Approssimazione integrale: " + str(result) + "\n")

    simpsonPlot(functionLambda, a, b, n, xValues)

    return True

if __name__ == "__main__":

    turnOn = True
    a = 0
    b = 0
    n = 0
    function = 0
    
    print("Programma per il calcolo degli integrali tramite formule di Trapezi e Cavalieri-Simpson")

    while turnOn:
        print("1 - Inserire una funzione \n2 - Modificare i dati di analisi \n3 - Metodo dei trapezi \n4 - Metdo di Cavalieri-Simpson \n0 - Quit")
        choice = int(input("Selezionare un numero: "))
        print("\n")

        if choice == 1:
            goInputFunction = True
            while goInputFunction:
                try:
                    inputFunction = input("Funzione (y in funzione di x): ")
                    function = eval(inputFunction)
                    testFunction = lambdify(x, function)    # Verifiy that the math function is ok
                    goInputFunction = False
                except SyntaxError:
                    print("Sintassi della funzione non corretta.")
            
            goInputData = True
            while goInputData:  
                try:    # Verify the input values
                    a = int(input("Punto a: "))
                    b = int(input("Punto b: "))
                    n = int(input("Numero di sottointervalli: "))
                    goInputData = False
                except ValueError:
                    print("Inserire un tipo di dato intero")

        if choice == 2:
            goInputData = True
            while goInputData:  
                try:    # As before
                    a = int(input("Punto a: "))
                    b = int(input("Punto b: "))
                    n = int(input("Numero di nodi: "))
                    goInputData = False
                except ValueError:
                    print("Inserire un tipo di dato intero")

        if choice == 3 and function != 0 and n != 0 and a != b: # Trapezoidal rule only if condition are ok
            trapezi(function, a, b, n)

        if choice == 4 and function != 0 and n != 0 and a != b: # Simpson rule only if condition are ok
            simpson(function, a, b, n)

        if choice == 0:
            turnOn = False
            quit()
