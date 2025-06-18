import threading
from libraryprojetEmile import *
                          
X = None
Y = None
Z = None

def runT1():
    print("runT1: on rentre dedans")
    print("*******************")
    global X
    X = 1

def runT2():
    print("runT2: on rentre dedans")
    print("*******************")
    global Y
    Y = 2

def runTsomme():
    print("runTsomme: on rentre dedans")
    print("*******************")
    global X, Y, Z
    if X is not None and Y is not None:
           Z = X + Y
    else:
          print("Erreur: X ou Y est None")

t1 = Task(name="T1", writes=["X"], run=runT1)

t2 = Task(name="T2", writes=["Y"], run=runT2)

tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

precedence = {
    "T1": [],
    "T2": [],
    "somme": ["T1", "T2"]  # La tâche 'somme' dépend de 'T1' et 'T2'
}

    
taskSystem = TaskSystem(tasks=[t1, t2, tSomme], precedence=precedence)

taskSystem.run()
taskSystem.draw()

print("X:", X)
print("Y:", Y)
print("Z:", Z)