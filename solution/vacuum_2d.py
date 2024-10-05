#!/usr/bin/env python
# coding: utf-8

# # Agents réflexe : avec et sans mémoire.
# 
# 
# 
# L’objectif de ce TD est l’exploration de deux agents réflexe : avec et sans mémoire :
# - simple relex agent
# - model based agent
# 
# Il est fourni avec trois fichiers squelettes agents.py,  vacuum_trivial.py, et vacuum_2d.py.
# Ces fichiers ont été développés à base des codes Python fournis pour le livre Intelligence artificielle : une approche moderne (AIMA) https://github.com/aimacode/aima-python.  
# 
# Dans certaines questions, il vous est demandé de compléter des parties de codes. 
# 
#  #### Commençons par tout importer à partir du module agents.

# In[ ]:


from util import  *  
from agents import *
from trivial_vacuum import *


# # II. Agent aspirateur en 2D
# 
# Un robot est situé dans une piéce qui contient des obstacles et de la poussiére sur le plancher (voir la figure). Le robot doit nettoyer la plancher en aspirant toute la poussière qui s'y trouve et ce en minimisant l’énergie d ́epensée. Le monde est représenté de la manièe suivante. La pièce est de forme carrée et toutes les positions possibles dans la piéce sont représentées par une grille de n x n. Les positions (0, 0) et (n, n) correspondent à la case supérieure gauche et la case inférieure droite, respectivement. Un obstacle occupe entièrement un certain nombre de cases. Le robot ne pourra jamais se déplacer à une case occupée par un obstacle et, évidemment, n’aura pas de poussièe à aspirer àcet endroit. Il ne pourra pas non plus sortir de la grille (on suppose qu’un mur entoure toute la grille).
# 
# ![vacuum2d.png](attachment:vacuum2d.png)
# 
# 
# 

# ### Commençons  par comprendre les classes "Wall and Direction"

# In[ ]:


# First we need a class to represent an obstacle (wall)
class Wall(Thing):
    pass


# In[ ]:


psource(Direction)


# In[ ]:


d = Direction(Direction.R) # check also  'down', 'right' and 'left'
l1 = d + Direction.L
print(l1.direction)


l2 = d + Direction.R
print(l2.direction) 


# In[ ]:


d = Direction(Direction.L)
new_loc = d.move_forward((0, 0))
print((0, 0), "--move_forward-->", new_loc)


# In[ ]:


from vacuum_2d import VacuumEnvironment
psource(VacuumEnvironment)


# # Quelle est la valeur de retour la fonction  percept?

# put your answer here:
# 
# La fonction renvoie un tuple (statut, Bump) où status est l'état de la cellule dans laquelle se trouve l'agent (propre ou sale) et Bump est l'état de l'agent, qu'il ait affronté le mur ou non

# In[ ]:


class RandomVacuumAgent(RandomAgent):
    """ Randomly choose one of the actions from the 2d vacuum environment, 
    ignoring all percepts."""

    def __init__(self):
        RandomAgent.__init__(self, [Action.NoOp, Action.Suck, Action.TurnLeft, Action.TurnRight, Action.Forward])
        self.direction = Direction() 


# In[ ]:


randomAgent = RandomVacuumAgent()
print(randomAgent.program("Any thing!"))


# ### Complètez le code suivant pour implementer un agent asperateur à simple reflèxe 

# In[ ]:


class ReflexVacuumAgent(Agent):
    """This agent performs the action Suck if location status is Dirty,
     otherwise it randomly choose one of the other possible actions 
     for a 2d vacuum environment."""  
    def __init__(self):
        Agent.__init__(self)
        self.direction = Direction()  
        def  program(percept):  
            status, bump = percept
            if status== Dirty:
                return Action.Suck
            return random.choice([Action.TurnLeft, Action.TurnRight, Action.Forward])

        self.program =  program
 


# ### Testez votre code:
# 
# Utiliser l'agent de suivi TraceAgent pour visualiser le cycle perception/action

# In[ ]:



env = VacuumEnvironment()
env.add_thing(Dirt(), (2, 2))
env.add_thing(Dirt(), (3, 3))
env.add_thing(Dirt(), (4, 4))
#agent =  ReflexVacuumAgent() 
agent = TraceAgent(agent)
env.add_thing(agent, (1,1))

 
env.run()
print("agent performance:", agent.performance)


# In[ ]:


# if the agent is in location 2,1 with direction Down, what is the next location if it execute the action Forward 
agent = ReflexVacuumAgent()  
agent.location = (2,1)
agent.direction = Direction( Direction.D)
new_location = agent.direction.move_forward(agent.location)
print(new_location)


# ### Le script vacuum2d.py mis en oeuvre des classes  qui simulent l’environnement de notre agent.
# 1. Ouvrez le script vacuum2d.py  et complètez les code de la classe  ReflexVacuumAgent 
#  
# 2. Implementez dans la cellule suivante une classe MyModelBasedVacuumAgent qui simule un agent aspirateur 2d à simple réflèxe basé sur modèle

# In[ ]:


class ModelBasedVacuumAgent(Agent):
    """This agent  keeps track of what locations are clean or dirty, obstacle."
     it performs the action Suck if location status is Dirty, 
     otherwise it randomly choose one of the other possible actions 
     for a 2d vacuum environment. But, it tries not to return to a position 
     already visited (clean). More particularly, if it is about to move to a position 
     already clean, it will prevent itself from doing so if at least one of the other 
     three adjacent positions has not been visited and is accessible 
     (this is neither a wall or an obstacle). 
     """

    def __init__(self):
        Agent.__init__(self)
        self.direction = Direction()
        self.model = {'Obstacle': [], 'Clean': []}
        self.program = self.new_program

    def new_program(self, percepts):
        location_status, agent_status = percepts
        loc_to_forward_to = self.direction.move_forward(self.location)
        if agent_status == Bump:
            self.model['Obstacle'].append(loc_to_forward_to)
        if location_status == Dirty:
            return Action.Suck
        else:
            while True:
                action = random.choice([Action.Forward, Action.TurnLeft, Action.TurnRight])
                if not action == Action.Forward:
                    return action
                if loc_to_forward_to in self.model['Obstacle']:
                    continue
                elif not (loc_to_forward_to in self.model['Clean']):
                    return action
                else:
                    x, y = self.location
                    neighbours = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
                    neighbours.remove(loc_to_forward_to)
                    not_visited = list(filter(lambda z:
                                              not (z in self.model.get('Clean') and z in self.model.get('Obstacle')),
                                              neighbours))
                    if len(not_visited) == 0:
                        return action


# ### Lancez le simulateur par execution de la cellule suivante puis comparer les diffrents types d'agents
# 1. download this file as pyhton (.py) File --> Download as --> pyhton
# 2. decomenter la cellule suivante; le programme graphique simulator s'exectra puis repondre à
# 
# Q1. Interpretez les résultats obtenus par le teste des trois agents dans 4 environnements differents 
# 
# Q2. Proposez un environnement dans lequel l’agent réflexe simple surpasse l’agent aléatoire  
# 
# Q33. Proposez une implémentation qui simule les changement dynamique dans l’environnement  

# In[ ]:


#import simulator


# In[ ]:




