import threading
from libraryprojetEmile import *
                          
X = None
Y = None
Z = None

def runT1():
    global X
    X = 1
    return X

def runT2():
    global Y
    Y = 2
    return Y

def runT3():
    global X
    X = X * 2
    return X
  
def runT4():
    global X
    X = X + 1
    return X
  
def runTsomme():
    global X, Y, Z
    if X is not None and Y is not None:
           Z = X + Y
           return Z
    else:
          print("Erreur: X ou Y est None")

t1 = Task(name="T1", writes=["X"], run=runT1)

t2 = Task(name="T2", writes=["Y"], run=runT2)

t3= Task(name="T3", writes=["X"], run=runT3)

t4= Task(name="T4", writes=["X"], run=runT4)

tSomme = Task(name="somme", reads=["X", "Y"], writes=["Z"], run=runTsomme)

precedence = {
    "T1": [],
    "T2": [],
    "T3": [],
    "T4": [],
    "somme": ["T1", "T2"]  # La tâche 'somme' dépend de 'T1' et 'T2'
}

taskSystem = TaskSystem(tasks=[t1, t2, t3, tSomme], precedence=precedence)

#taskSystem.run()
#taskSystem.draw()
#taskSystem.detTestRnd()
taskSystem.parCost()

# print("X:", X)
# print("Y:", Y)
# print("Z:", Z)