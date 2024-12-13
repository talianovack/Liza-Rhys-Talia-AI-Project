import math
from DummyData import flights, high_threshold, low_threshold, med_threshold
from collections import namedtuple
from operator import itemgetter
import random
#flights = getFlights(flight_ids, airportArrivals, airportDistances, fuelLevels)
 #TODO: simulate and backprop methods & implement a check for conflicting times, locations, or fuel levels       

class AirspaceState:
    #State of the airspace: all of the flight_ids, list of planes landed, and simulation time 
    def __init__(self, planes_to_land, landed =[], time=0):
        #Pulled the plane numbers from the data 
        self.planes_to_land = planes_to_land #CAN USE THIS TO PULL OUT JUST THE PLANES: map(lambda x: x[0], planes)
        self.landed = landed
        self.time = time
    
    def land_plane(self, action):
        #Land one of the planes and return the new airspace after the plane has landed
        #Basically, take action to create a new node
        #Select at random a plane to land (but need to update to land most pressing plane)
        plane = random.choice(self.planes_to_land)
        if (action == ("Land")):
            self.landed.append(plane)
            self.planes_to_land.remove(plane)
        #INCORPORATE DELAY?
        return AirspaceState(self.planes_to_land, self.landed, self.time+1) 
            
    
    
    def is_terminal(self):
        #checking to see if all of the planes have been landed
        if len(self.planes_to_land) == 0:
            return True
        return False

    #Method to show how each Node as Time: __ Queue of planes: ___ and Planes landed: ___
    def __repr__(self):
        return f"Time: {self.time}, Queue: {self.planes_to_land}, Landed: {self.landed}"
        

class Node():
    def __init__(self, AirspaceState, parent=None):
        self.visits = 1
        self.value = 0
        self.state = AirspaceState
        self.children = []
        self.parent=parent

    def getActions(self):
        #Legal actions are landing one of the planes in the queue 
        return self.state.planes_to_land
    
    def is_fully_expanded(self):
        #check that all of the possible actions have been tried
        if len(self.children) == 0:
            return True
        return False
    
    def has_parent(self):
        #Check if the node has a parent node
        if self.parent is not None:
            return True
        return False
    
    

    def expand(self):
    # Find all possible planes to land
        if not self.state.is_terminal():
            #For every plane that has not yet landed, create a new node landing that plane 
            #ASSIGN VALUES BASED ON FUEL AND DISTANCE HERE
            random.shuffle(self.state.planes_to_land)

            for plane_to_land in self.getActions():
                #Find most pressing plane to land
      
                for child in self.children:
                    if child.state.landed:
                        last_landed = child.state.landed[-1]
                        if plane_to_land == last_landed:
                            break
                newState = AirspaceState(self.state.planes_to_land.copy(), self.state.landed.copy(), self.state.time)
                newState.planes_to_land.remove(plane_to_land)
                newState.landed.append(plane_to_land)
                newState.time += 1

                # Make new child and append
                childNode = Node(newState, parent=self)
                self.children.append(childNode)
                return [childNode]
        return None


    
    #Finds the best child node
    def best_next_plane_to_land(self, exploration_weight = 1):
        #select the best child (max score) using the UCT
        best_child = None
        max_uct_val = float('-inf')
        self.expand()
        
        #Iterate over children to find all of their UCT scores, 1e-6 prevens division by 0
        for child in self.children:
            print("CHILD = ", child, "Time = ", self.state.time)
            exploitation = child.value / (child.visits + 1e-6)
            exploration = exploration_weight * math.sqrt(math.log(self.visits + 1) / (child.visits + 1e-6))
            
            #Combine exploration vs exploitation to get the uct value
            uct = exploration + exploitation 

            #Select the node with the max UCT value
            if uct > max_uct_val:
                max_uct_val = uct
                best_child = child
        #print("BEST CHILD = ", best_child)
        return best_child
    
def simulate(self):
    state = self.state
    total_time = state.time
    landing_planes = state.planes_to_land.copy()
    landed = state.landed.copy()

    #simulate landing until terminal
    reward = 0
    while landing_planes:
        #select most urgent plane to land
        plane = self.select_priority_plane(landing_planes)

        #take action
        landed.append(plane)
        landing_planes.remove(plane)

        #inc timestep
        time +=1

        #update reward depending on the fuel and distance
        total_reward = self.calculate_reward(plane,time)
    return total_reward
def select_priority_plane(self, planes_to_land):
    return min(planes_to_land, key=lambda plane: plane['fuel'])

def calculate_reward(self, plane, time):
    time_penalty = abs(time - plane['eta_arr'])*15
    fuel_penalty = (100000 - plane['fuel'])/1000
    return -(time_penalty +fuel_penalty)

def backpropagate(node, reward):
    #backprop the result of the simulation up the tree, updating the visits and value
    while node is not None:
        node.visits+=1
        node.value+=reward
        node = node.parent

    
        
def MCTS(root, iterations = 1000):
    for _ in range(iterations):
        node = root
        #Select!
        while node.children and node.is_fully_expanded():
            node = node.best_next_plane_to_land()

        #Expand!
        if not node.state.is_terminal():
            new_child = node.expand()
            if new_child:
                #pick first child for simulation
                node = new_child[0] 

        #Simulate/Rollout!
        reward = simulate(node.state)

        #Backprop!
        backpropagate(node, reward)

        iterations -=1
    #Tree built, now find the order of the landings 

    landing_order = []
    curNode = root
    while not curNode.state.is_terminal():
        curNode = curNode.best_next_plane_to_land()

        #If the node is defined, append in reverse order the landed planes list
        #since the most recently landed plane will be at the back
        if curNode:
            landing_order.append(curNode.state.landed[-1])
         
        else:
            break
        
    return landing_order


if __name__ == "__main__":
    initial_ordering = AirspaceState(flights)
    root = Node(initial_ordering)
    sequence = MCTS(root, iterations=1000)
    print()
    print()
    print("landing sequence = ", sequence)
    


