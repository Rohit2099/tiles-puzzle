from queue import PriorityQueue

"""
Puzzle is a class that encompasses the whole black and white tile puzzle problem
which includes an uninformed(BFS) and an informed(A*) search algorithm defined to solve the 
problem.
Every state of the puzzle eg. "BWBW BW" is termed as "tray" inside the class and is defined as 
a list for the ease of operations to be performed on it.
"""
class Puzzle:

    def __init__(self, input_string):
        self.tray = list(input_string)
        self.n = len(input_string)                                #length of puzzle
        self.bfs = {}                                           #Used in BFS to store the node's data
        self.astar = {}                                         #Used in A* to store the node's data
        self.priority_queue = PriorityQueue()                   #Used in A*
        self.closed = {}                                        #Used to check the visited nodes in A*
        self.astar_goal = []                                    #Saves the goal state for A* algorithm
        self.bfs_goal = []                                      #Saves the goal state for BFS
        self.a_count = 0                                        #Number of nodes in A*
        self.covered_goal_states = []                           #List of explored goal states when generating all goal states
        self.goal_states = ["WWW BBB", "WWWB BB", "WWWBB B", "WWWBBB ", " WWWBBB", "W WWBBB", "WW WBBB"]


    # Returns the tray after performing shift operation 
    def shiftTile(self, i, direction, tray):
        if direction == 'left':
            if i < self.n - 1:
                tray[i] = tray[i + 1]
                tray[i + 1] = ' '
                return tray
            else:
                return []

        if direction == 'right':
            if i > 0:
                tray[i] = tray[i - 1]
                tray[i - 1] = ' '
                return tray
            else:
                return []
        

    # Returns the tray after performing hop operation 
    def hopOneTile(self, i, direction, tray):
        if direction == 'left':
            if i < self.n - 2:
                tray[i] = tray[i + 2]
                tray[i + 2] = ' '
                return tray
            else:
                return []

        if direction == 'right':
            if i > 1:
                tray[i] = tray[i - 2]
                tray[i - 2] = ' '
                return tray
            else:
                return []
        

    # Returns the tray after performing double hop operation
    def hopTwoTiles(self, i, direction, tray):
        if direction == 'left':
            if i < self.n -3:
                tray[i] = tray[i + 3]
                tray[i + 3] = ' '
                return tray
            else:
                return []

        if direction == 'right':
            if i > 2:
                tray[i] = tray[i - 3]
                tray[i - 3] = ' '
                return tray
            else:
                return []


    # Checks it the tray is in goal state
    def isGoal(self, tray):
        black, white, index = 0, 0, 0
        while black != 1:
            if tray[index] == 'B':
                black += 1
            elif tray[index] == 'W':
                white += 1
            if white == (self.n // 2):
                return True
            index += 1
        
        return False


    # Returns the index of empty space in the tray
    def getEmptyIndex(self, tray):
        return tray.index(' ')


    # Returns all the poosible children nodes that can be
    # generated from a parent(tray) by performing hops and shifts.
    def getPossibleChildren(self, parent):
        results = []
        empty = self.getEmptyIndex(parent)

        results.append(self.hopOneTile(empty, 'left', list(parent)))
        results.append(self.hopOneTile(empty, 'right', list(parent)))        
        results.append(self.shiftTile(empty, 'left', list(parent)))
        results.append(self.shiftTile(empty, 'right', list(parent)))
        results.append(self.hopTwoTiles(empty, 'left', list(parent)))
        results.append(self.hopTwoTiles(empty, 'right', list(parent)))

        children = [child for child in results if len(child) > 0]
        return children


    # Converts a list to string
    def convertToString(self, tray):
        return ''.join(tray)


    # The core function to solve the puzzle using Breadth First Search
    # This method only solves and saves the required information and does not
    # print the required path or cost.
    def solveBFS(self, print_tree=False):
        self.bfs = {}
        parents = []
        new_parents = []

        if print_tree:
            print('--------------------------------')
            print('Resulting search graph of BFS\n--------------------------------')
            print('\nRoot - 0 || Parent - -1')
            self.printTray(self.tray)

        new_parents.append(self.tray)
        self.bfs[self.convertToString(new_parents[0])] = {}
        self.bfs[self.convertToString(new_parents[0])]['parent'] = -1
        self.bfs[self.convertToString(new_parents[0])]['count'] = 0

        count = 1
        finished = False

        while not finished:
            parents = list(new_parents)
            new_parents = []
            for parent in parents:
                children = self.getPossibleChildren(parent)
                for child in children:
                    if self.convertToString(child) not in self.bfs:
                        self.bfs[self.convertToString(child)] = {}
                        self.bfs[self.convertToString(child)]['count'] = count
                        self.bfs[self.convertToString(child)]['parent'] = self.bfs[self.convertToString(parent)]['count']

                        new_parents.append(child)
                        count += 1

                        if print_tree:
                            print('Node - ' + str(self.bfs[self.convertToString(child)]['count']), end='')
                            print(' || Parent - ' + str(self.bfs[self.convertToString(child)]['parent']), end='')
                            action = self.getCost(child, parent)
                            hop = ""
                            if action == 1:
                                hop = "Hop/Slide"
                            else:
                                hop = "Double hop"
                            print(' || Action - ' + str(hop))
                            self.printTray(child)

                    if (self.isGoal(child)):
                        self.bfs_goal = child
                        finished = True
                        break
                
                if finished:
                    break


    # Returns the cost to go from state 'a' to state 'b'
    def getCost(self, a, b):
        diff = abs(a.index(' ') - b.index(' '))

        if diff == 1:
            return diff
        return diff - 1


    # Prints the cost and the solution path for BFS.
    # solveBFS() needs to be called before calling this method
    def getSolutionBfs(self):
        temp = list(self.bfs_goal)
        result = []
        result.append(temp)
        cost = []
        while (self.convertToString(temp) != self.convertToString(self.tray)):
            parent_node_num = self.bfs[self.convertToString(temp)]['parent']
            get_parent = self.getKey(parent_node_num, False)
            result.append(list(get_parent))
            temp_cost = self.getCost(self.convertToString(temp), get_parent)
            cost.append(temp_cost)
            temp = list(get_parent)

        cost.append(0)

        print('-----------------------\nSolution Path for BFS\n-----------------------\n')
        for i in range(len(result) - 1, -1, -1):
            print('Node - ' + str(self.bfs[self.convertToString(result[i])]['count']) + " || Cost: " + str(sum(cost[i:])), end='')
            action = cost[i]
            hop = ""
            if action == 1:
                hop = "Hop/Slide"
                print(' || Action - ' + str(hop))
            elif action == 2:
                hop = "Double hop"
                print(' || Action - ' + str(hop))
            else:
                print('\n')
            self.printTray(result[i])
            
        print('Total Cost of minimum solution path for BFS: ' + str(sum(cost)))


    # Heuristic Function defined for A* search algorithm
    def wrongSideHeuristic(self, tray):
        cost = 0
        index = self.n - 1
        black = self.n // 2

        while index >= 0 and black != 0:
            if tray[index] == 'W':
                cost += black
            if tray[index] == 'B':
                black -= 1
            index -= 1
        
        return cost
        

    # Generates children for a particular parent in A* and saves the cost
    # to reach the children node to the priority queue.
    def generateChildren(self, parent):
        results = []
        empty = self.getEmptyIndex(parent)
        results.append(self.shiftTile(empty, 'left', list(parent)))
        results.append(self.shiftTile(empty, 'right', list(parent)))
        results.append(self.hopOneTile(empty, 'left', list(parent)))
        results.append(self.hopOneTile(empty, 'right', list(parent)))
        results.append(self.hopTwoTiles(empty, 'left', list(parent)))
        results.append(self.hopTwoTiles(empty, 'right', list(parent)))

        ref = [1, 1, 1, 1, 2, 2]
        aux = [(element, hop) for element, hop in zip(results, ref) if len(element) > 0]
        results = aux

        for node in results:
            g_n = node[1] + self.astar[self.convertToString(parent)]['f(n)'] - self.wrongSideHeuristic(parent)
            h_n = self.wrongSideHeuristic(node[0])
            current_cost = g_n + h_n

            if self.convertToString(node[0]) not in self.closed:
                if self.convertToString(node[0]) not in self.astar:
                    self.priority_queue.put((current_cost, (node[0], self.astar[self.convertToString(parent)]['count'])))
                    self.astar[self.convertToString(node[0])] = {}
                    self.astar[self.convertToString(node[0])]['f(n)'] = current_cost
                    self.a_count += 1                    
                    self.astar[self.convertToString(node[0])]['count'] = self.a_count
                    self.astar[self.convertToString(node[0])]['parent'] = self.astar[self.convertToString(parent)]['count']


                else:
                    if self.astar[self.convertToString(node[0])]['f(n)'] > current_cost:
                        self.astar[self.convertToString(node[0])]['f(n)'] = current_cost

            else:
                if self.astar[self.convertToString(node[0])]['f(n)'] > current_cost:
                    self.astar[self.convertToString(node[0])]['f(n)'] = current_cost
                    self.astar[self.convertToString(node[0])]['parent'] = self.astar[self.convertToString(parent)]['count']



    # The core function to solve the puzzle using A*. 
    # This method only solves the puzzle and stores the relevant information
    # and is not used for printing the cost and the solution path.
    def solveAStar(self, print_tree=False):
        self.astar = {}
        self.closed = []
        self.priority_queue = PriorityQueue()

        if print_tree:
            print('--------------------------------')
            print('Resulting search path of A*\n--------------------------------')

        parent = list(self.tray)
        self.priority_queue.put((self.wrongSideHeuristic(parent), (parent, -1)))
        self.a_count = 0

        self.astar[self.convertToString(parent)] = {}
        self.astar[self.convertToString(parent)]['f(n)'] = self.wrongSideHeuristic(parent)
        self.astar[self.convertToString(parent)]['count'] = self.a_count
        self.astar[self.convertToString(parent)]['parent'] = -1

        finished = False

        while not finished:
            parent_node = self.priority_queue.get(False)
            self.priority_queue.task_done()

            parent = parent_node[1][0]
            parent_node_num = parent_node[1][1]

            self.closed.append(self.convertToString(parent))
            self.generateChildren(parent)

            if print_tree:                        
                print('Node - ' + str(self.astar[self.convertToString(parent)]['count']), end='')
                print(' || Parent - ' + str(parent_node_num), end='')
                print(' || f(n) - ' + str(self.astar[self.convertToString(parent)]['f(n)']), end='')
                action = self.getCost(parent, self.getKey(self.astar[self.convertToString(parent)]['parent']))
                hop = ""
                if action == 1:
                    hop = "Hop/Slide"
                    print(' || Action - ' + str(hop))
                elif action == 2:
                    hop = "Double hop"
                    print(' || Action - ' + str(hop))
                if parent_node_num == -1:
                    print('\n')
                self.printTray(parent)

            if (self.isGoal(parent)):
                self.astar_goal = parent
                finished = True
                break


    # Return the state of the puzzle(tray) according to the node number
    def getKey(self, val, informed = True): 
        if informed:
            for key, value in self.astar.items(): 
                if val == value['count']: 
                    return key 
        
            return "key doesn't exist"
        
        else:
            for key, value in self.bfs.items(): 
                if val == value['count']: 
                    return key 
        
            return "key doesn't exist"


    # Prints the cost at each step and the solution path of the A* algorithm
    # solveAStar() needs to be called before this method
    def getSolutionAStar(self):
        temp = list(self.astar_goal)
        result = []
        result.append(temp)
        while (self.convertToString(temp) != self.convertToString(self.tray)):
            parent_node_num = self.astar[self.convertToString(temp)]['parent']
            get_parent = self.getKey(parent_node_num, True)
            result.append(list(get_parent))
            temp = list(get_parent)
        
        print('-----------------------\nSolution Path for A*\n-----------------------\n')
        for i in range(len(result) - 1, -1, -1):
            print('Node ' + str(self.astar[self.convertToString(result[i])]['count']) + " || f(n): " + str(self.astar[self.convertToString(result[i])]['f(n)']), end='')
            action = self.getCost(result[i], self.getKey(self.astar[self.convertToString(result[i])]['parent']))
            hop = ""
            if action == 1:
                hop = "Hop/Slide"
                print(' || Action - ' + str(hop))
            elif action == 2:
                hop = "Double hop"
                print(' || Action - ' + str(hop))
            else:
                print('\n')
            self.printTray(result[i])
        
        print('Total Cost of minimum solution path for A*: ' + str(self.astar[self.convertToString(self.astar_goal)]['f(n)']))


    # An A* variation which generates paths for all the possible goal states.
    # This method is used only to solve the problem and not for printing the cost.
    def generateAllGoalsAStar(self, print_tree=False):
        self.astar = {}
        self.closed = []
        self.priority_queue = PriorityQueue()
        self.covered_goal_states = []

        if print_tree:
            print('----------------------------------------------------------')
            print('Resulting search path of A* for finding all goal states\n----------------------------------------------------------')
            print('\nRoot - 0 || Parent - -1')

        parent = list(self.tray)
        self.priority_queue.put((self.wrongSideHeuristic(parent), (parent, -1)))
        self.a_count = 0

        self.astar[self.convertToString(parent)] = {}
        self.astar[self.convertToString(parent)]['f(n)'] = self.wrongSideHeuristic(parent)
        self.astar[self.convertToString(parent)]['count'] = self.a_count
        self.astar[self.convertToString(parent)]['parent'] = -1

        finished = False     

        while not finished:
            parent_node = self.priority_queue.get(False)
            self.priority_queue.task_done()

            parent = parent_node[1][0]
            parent_node_num = parent_node[1][1]

            self.closed.append(self.convertToString(parent))
            self.generateChildren(parent)

            if print_tree:                        
                print('Node - ' + str(self.astar[self.convertToString(parent)]['count']), end='')
                print(' || Parent - ' + str(parent_node_num), end='')
                print(' || f(n) - ' + str(self.astar[self.convertToString(parent)]['f(n)']), end='')
                action = self.getCost(parent, self.getKey(self.astar[self.convertToString(parent)]['parent']))
                hop = ""
                if action == 1:
                    hop = "Hop/Slide"
                    print(' || Action - ' + str(hop))
                elif action == 2:
                    hop = "Double hop"
                    print(' || Action - ' + str(hop))
                if parent_node_num == -1:
                    print('\n')

            if (self.convertToString(parent) in self.goal_states and parent not in self.covered_goal_states):
                self.covered_goal_states.append(parent)
                if print_tree:
                    print('Goal State Reached!')
                if len(self.covered_goal_states) == len(self.goal_states):
                    finished = True
                    self.printTray(parent)
                    break  
            
            if print_tree:
                self.printTray(parent)



    # Used to print all the solution paths for all the goal states.
    # generateAllGoalsAStar() needs to be called before this method
    def printAllGoals(self):
        for num, goal in enumerate(self.covered_goal_states):
            temp = list(goal)
            result = []
            result.append(temp)
            print('-----------------------\nGoal State - {} path for A*\n-----------------------\n'.format(num + 1))
            while (self.convertToString(temp) != self.convertToString(self.tray)):
                parent_node_num = self.astar[self.convertToString(temp)]['parent']
                get_parent = self.getKey(parent_node_num, True)
                result.append(list(get_parent))
                temp = list(get_parent)

            for i in range(len(result) - 1, -1, -1):
                print('Node ' + str(self.astar[self.convertToString(result[i])]['count']) + " || f(n): " + str(self.astar[self.convertToString(result[i])]['f(n)']), end='')

                action = self.getCost(result[i], self.getKey(self.astar[self.convertToString(result[i])]['parent']))
                hop = ""
                if action == 1:
                    hop = "Hop/Slide"
                    print(' || Action - ' + str(hop))
                elif action == 2:
                    hop = "Double hop"
                    print(' || Action - ' + str(hop))
                else:
                    print('\n')
                self.printTray(result[i])
        
            print('Total Cost of Goal {} solution path for A*: '.format(num + 1) + str(self.astar[self.convertToString(goal)]['f(n)']) + '\n')



    # Prints the current state(tray) in a readable format
    def printTray(self, tray):
        print(' =============================')
        print(" | ", end = '')

        for i in tray:
            print(i, end = " | ")

        print('\n =============================\n\n')


if __name__ == '__main__':

    input_string = 'BBW WWB'
    puzzle = Puzzle(input_string)

    #puzzle.solveBFS(print_tree=True)          # Uncomment this to run BFS
    #puzzle.getSolutionBfs()                   # Uncomment this to display solution for BFS
    # puzzle.solveAStar(print_tree=True)        # Uncomment this to run A*
    # puzzle.getSolutionAStar()                 # Uncomment this to display solution for A*
    # puzzle.generateAllGoalsAStar(print_tree=True)     # Uncomment to get all goals
    # puzzle.printAllGoals()                            # Uncomment to display all goals