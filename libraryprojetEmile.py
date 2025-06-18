import threading
import time
from timeit import timeit
import networkx as nx
import matplotlib.pyplot as plt
import random
import timeit



class Task:
     def __init__(self, name="", reads =None, writes =None, run=None):
           if reads is None:
              reads = []
           if writes is None :
              writes = []
     
    
           self.name = name
           self.reads = reads
           self.writes = writes
           self.run = run
           #ajout du semaphore
           self.semaphore = threading.Semaphore(0)

class TaskSystem:
       
       def __init__(self, tasks, precedence):
              self.tasks = tasks
              self.precedence = precedence

       def getDependencies(self, nomTache):
              #Retour les dépendances d'une tâche donnée
              if nomTache not in self.precedence:
                    return print(f"Erreur : La Tache '{nomTache}' n'existe pas dans la liste de précédence")   
              return self.precedence.get(nomTache, [])
       
       def runSeq(self):
              for t in self.tasks:
                     t.run()
       
       def run(self):

              def run_task(task_name):
                    
                     #Recherche de la tâche
                    task = next((t for t in self.tasks if t.name == task_name), None)

                    if task is None:
                      #print(f"Erreur: la tâche '{task_name}' n'a pas été trouvée.")
                      return

                    #Recherche et exécution des dépendences avant l'exécution de la tâche

                    dependence = self.getDependencies(task_name)
                    #print(f"Tableau des dépenses de {task_name} : {dependence}")
                    for dep in dependence:
                          run_task(dep)

                     #Exécution de la tâche en elle-meme
                    #print(f"Exécution de la tâche {task_name}")
                    task.run()
                    
                    #Liberation du sémaphore seulement si la tache n'est pas déjà terminé 

                    if task.semaphore._value==0:
                     task.semaphore.release()

              #Appel en iteration de toutes les tâches
              for t in self.tasks:
                    #print(f"Lancement de la tâche {t.name}")
                    run_task(t.name)

              #Attente que toutes les tâches soit terminé
              for t in self.tasks:
                    #on rentre ici a la fin, pour confirmer que chaque threads est fini
                    t.semaphore.acquire()

       def _valide_input(self):
        # vérifier si la liste des tâches est valide
        #détection des doublons
        task_names = set(self.tasks.keys())

        if len(task_names) != len(self.tasks):
            raise ValueError("Doublons dans les noms de tâches")
        
        #détection des dépendances avec des tâches inexistantes
        for t in self.tasks:
            for d in self.tasks[t].reads + self.tasks[t].writes:
                if d not in task_names:
                    raise ValueError(f"Tâche {t} dépend de tâche inexistante {d}")

        #détection à un systeme de tâche intermédiaire
        for t in self.tasks:
            for d in self.tasks[t].reads + self.tasks[t].writes:
                if d in self.tasks:
                    raise ValueError(f"Tâche {t} dépend de tâche intermédiaire {d}")
       
       def draw(self):
            
            #Initialisation d'une liste vide qui prendra les sommets et arêtes
            
            edge_list = set()

            #Faire que chaque tâches recoivent en entrée une sortie de leur dépendence
            
            for t in self.tasks:
                 dependence = self.getDependencies(t.name)
                 if dependence != []:
                      for dep in dependence:
                            edge_list.add((dep,t.name))
                      print("edge_list",edge_list)

            #Dessine le Graphe, avec les arêtes et les sommetes corespondant
                      
            G = nx.MultiDiGraph() 

            G.add_edges_from(edge_list)

            pos = nx.spring_layout(G, seed=42)

            nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightgreen", font_size=10, font_weight="bold", arrows=True)

            plt.show()

       def detTestRnd(self):
            
            taskTab = []
            resultTab = set()
            
            for t in self.tasks:
                 print(f"... t_name : {t.name}")
                 taskTab.append(t.name)

            for t in self.tasks:
                if self.precedence is not None:
                     pass
                result = t.run()
                print(f"Résultat de {t.name} (1ère exécution) : {result}")
                resultTab.add(result)

            print(resultTab,", => ResultTab")

            #Choisir les tasks ayant des précédences et les enlevés

            random.shuffle(taskTab)
            
            resultRandom = set()

            #Recherche de la tâche par son nom 
            for t_name in taskTab[:]: #[:] crée une copie de la liste
               
                t = next((t for t in self.tasks if t.name == t_name), None)
                dependence = self.getDependencies(t_name)

                for i in range(len(taskTab)-1):
                    if dependence != []:
                            print(f"Suppression de {t_name} de taskTab")
                            taskTab.remove(t_name)
                            break

                result = t.run()
                print(f"Résultat de {t.name} (exécution après mélange) : {result}")
                resultRandom.add(result)

            print(resultRandom,", => ResultTab (Après exécution avec l'ordre mélangé)")

             # Vérifier le déterminisme après mélange
            if sum(resultTab) != sum(resultRandom):
              print(f"*PAS DETERMINISTE* (resultTab = {resultTab} != resultRandom = {resultRandom}).")
            else:
              print(f"*DETERMINISTE* (resultTab = {resultTab} == resultRandom = {resultRandom}).")
              

       def parCost(self):
            # temps1 = timeit.timeit(lambda: self.run() ,number = 1000)
            # print(f"temps d'exécution de run() : {temps1:0.2} secondes")

            # temps2 = timeit.timeit(lambda: self.runSeq(), number = 1000)
            # print(f"temps d'exécution de runSeq() : {temps2:0.2} secondes")

            start_time = time.perf_counter()

            for i in range(100000):
                self.run()

            end_time = time.perf_counter()

            elapsed_time = end_time - start_time
            
            print(f" Le temps de run() : {elapsed_time: .6f} seconds")

            start_time2 = time.perf_counter()

            for i in range(100000):
                self.runSeq()

            end_time2 = time.perf_counter()

            elapsed_time2 = end_time2 - start_time2
            
            print(f" Le temps de runSeq() : {elapsed_time2: .6f} seconds")




