import argparse as ap

import re

import platform

import numpy as np


"""
    Name: Miji Kim
    Date: 12th May, 2020
"""
"""
    Create a class for node
    parent means current node's parent
    pos means current node's position
    id means node identifier (e.g. N0, N1, etc.)
    operator means actions that triggered the node (e.g. S-D, S-D-D, etc.)
    counter means order of expansion
    g means cost of reaching the current node
    h means heuristic value
    f means total cost where f = g + h
"""
class Node:
    def __init__(self, parent=None, pos=None):
        self.parent=parent
        self.pos=pos
        self.id=""
        self.operator=""
        self.counter=0
        self.g=0
        self.h=0
        self.f=0

#Create a function to show path
def show_path(node,map):
    current_node = node
    matrix = map
    solution = current_node.operator.split("-")
    solution += "G"
    operator = ""
    g_cost = 0
    counter = 0
    string_matrix = ""
    temp_pos = (0,0)
    temp_path = ""

    #First, convert matrix to string in order to visualise the matrix after S replaced with *
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == "S":
                matrix[i][j] = "*"
                temp_pos = (i,j)
            string_matrix += matrix[i][j] + " "
            counter += 1
            if counter % len(matrix) == 0:
                string_matrix += "\n"

    #Replace * with S to reuse to matrix
    matrix[temp_pos[0]][temp_pos[1]] = "S"
    #Insert space and comment representing the path and g value
    string_matrix += "\n"
    string_matrix += "S" + " " + str(g_cost)
    string_matrix += "\n"
    #Every path starts with S
    temp_path += "S"

      #R    #RD    #D     #LD      #L      #LU       #U      #RU
    #[[0, 1],[1, 1],[1, 0],[1, -1],[0, -1],[-1, -1], [-1, 0],[-1, 1]]
    for index, z in enumerate(solution):
        if solution[index] == "S":
            continue
        operator = solution[index]
        if operator == "R":
            temp_pos = (temp_pos[0],temp_pos[1]+1)
            #Call solution_matrix function and update matrix, actions(path), and g value
            string_matrix,temp_path,g_cost = solution_matrix(matrix, temp_pos, "R", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "RD":
            temp_pos = (temp_pos[0]+1,temp_pos[1]+1)
            string_matrix,temp_path,g_cost = solution_matrix(matrix, temp_pos, "RD", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "D":
            temp_pos = (temp_pos[0]+1,temp_pos[1])
            string_matrix,temp_path,g_cost = solution_matrix(matrix, temp_pos, "D", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "LD":
            temp_pos = (temp_pos[0]+1,temp_pos[1]-1)
            string_matrix,temp_path,g_cost = solution_matrix(matrix, temp_pos, "LD", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "L":
            temp_pos = (temp_pos[0],temp_pos[1]-1)
            string_matrix,temp_path,g_cost = solution_matrix(matrix, temp_pos, "L", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "LU":
            temp_pos = (temp_pos[0],temp_pos[1]-1)
            string_matrix, temp_path, g_cost = solution_matrix(matrix, temp_pos, "LU", string_matrix,
                                            solution, index, temp_path, g_cost)
        if operator == "U":
            temp_pos = (temp_pos[0]-1,temp_pos[1])
            string_matrix,temp_path,g_cost = solution_matrix(matrix,temp_pos, "U", string_matrix,
                                            solution,index,temp_path,g_cost)
        if operator == "RU":
            temp_pos = (temp_pos[0]-1,temp_pos[1]+1)
            string_matrix,temp_path,g_cost = solution_matrix(matrix,temp_pos, "RU", string_matrix,
                                            solution,index,temp_path,g_cost)
    return string_matrix

#Called by show_path function to update the matrix and the string (string_matrix)
def solution_matrix(matrix,pos,char,string,sol_list,ind, path,cost):
    map = matrix
    temp_pos = pos
    operator = char
    string_matrix = string
    solution = sol_list
    index = ind
    temp_path = path
    g_cost = cost

    #Call update_matrix function to represent ROBBIE's position with *
    new_matrix = update_matrix(map, temp_pos)
    string_matrix += "\n"
    string_matrix += new_matrix  # add matrix to the string
    string_matrix += "\n"
    before_temp = "-" + solution[index]
    #if it is the last position prior to "G", add "G" to the end of the path
    if index == int((len(solution)-2)):
        before_temp  += "-G"
    temp_path += before_temp  # update actions(path)
    if operator == "R" or operator == "D" or operator == "L" or operator == "U":
        g_cost += 2  # update g value
    else:
        g_cost += 1
    string_matrix += temp_path + " " + str(g_cost)  # add comment to the string
    string_matrix += "\n"
    return string_matrix,temp_path,g_cost

#Called by solution_matrix function to visualise ROBBIE's position with *
def update_matrix(map,pos):
    matrix = map
    temp_pos = pos
    counter = 0
    original_char = ""
    string_matrix = ""
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if (i,j) == temp_pos:
                original_char = matrix[i][j]
                matrix[i][j] = "*"
                temp_pos = (i, j)
            string_matrix += matrix[i][j] + " "
            counter += 1
            if counter % len(matrix) == 0:
                string_matrix += "\n"
    #reset matrix; otherwise a series of * is shown in the output file
    matrix[temp_pos[0]][temp_pos[1]] = original_char
    return string_matrix

#Change the function name from graphsearch to astarsearch in main()
#solution_string = astarsearch(map, flag)
def astarsearch(map, flag):
    diag_flag = flag
    #Initial input map --> ['5\n', 'SRRXG\n', 'RXRXR\n', 'RRRXR\n', 'XRXRR\n', 'RRRRR\n']
    temp_matrix = []
    #Use rstrip() function to remove trailing whitespace

    #After for loop, temp_matrix -->  [['5'], ['SRRXG'], ['RXRXR'], ['RRRXR'], ['XRXRR'], ['RRRRR']]
    for i in range(len(map)):
        temp_matrix.append(map[i].rstrip('\n').split(","))

    #N specifies the number of columns and rows (e.g. 5 means a grid of size 5 X 5)
    n = int(''.join(temp_matrix.pop(0)))

    #After sum, temp_matrix --> ['SRRXG', 'RXRXR', 'RRRXR', 'XRXRR', 'RRRRR']
    temp_matrix = sum(temp_matrix,[])

    #After the below function, temp2_matrix --> [['SRRXG'], ['RXRXR'], ['RRRXR'], ['XRXRR'], ['RRRRR']]
    temp2_matrix = []
    temp2_matrix = [[x] for x in temp_matrix]

    #matrix, separate string into characters
    #[['S', 'R', 'R', 'X', 'G'], ['R', 'X', 'R', 'X', 'R'], ['R', 'R', 'R', 'X', 'R'], ['X', 'R', 'X', 'R', 'R'],
    #['R', 'R', 'R', 'R', 'R']]
    matrix = []
    for i in range(len(temp2_matrix)):
        str_list = list(temp2_matrix[i][0])
        matrix.append(str_list)

    #Check if S and G are in the map
    matrix_string_format = ""
    present_in_map = True
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            matrix_string_format += matrix[i][j] + " "
    if ('S' not in matrix_string_format) or ('G' not in matrix_string_format):
        present_in_map = False
        print("S or G not found in map: NO-PATH")
        return "S or G not found in map: NO-PATH"

    start = []
    finish = []
    #Find the position of 'S' and 'G'
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 'S':
                start=[i,j]
            if matrix[i][j] == 'G':
                finish=[i,j]

    #Create a node and initialise its value; parent, pos
    start_node = Node(None, tuple(start))
    finish_node = Node(None, tuple(finish))
    finish_node.g = finish_node.h = finish_node.f = 0
    start_node.g = 0
    #Heuristic function to calculate the distance, considering diagonal movement
    #Diagonal movement costs 1, other movements cost 2
    x_row = abs(start_node.pos[0] - finish_node.pos[0])

    y_col = abs(start_node.pos[1] - finish_node.pos[1])
    start_node.h = max(x_row,y_col)
    start_node.f = start_node.g + start_node.h
    start_node.operator = "S"
    start_node.id = "N"+str(0)

    #Create and initialise open (list to visit) and closed (list already visited) list
    open_list = []
    closed_list = []
    #Append the start node in the list to visit
    open_list.append(start_node)

    #Create a stop condition if it has gone through too many iterations
    out_iter = 0
    max_iter = len(matrix) * 30

    #id_counter used as node identifier
    id_counter = 0
    #expand_counter used to count order of expansion
    expand_counter = 0

    #Create a list for children
    children_list=[]

    #To record already visited tile and tile that is "X"
    visited_tile = np.zeros([n,n], dtype=int)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] == 'X':
                visited_tile[i][j] == 1

    #Use while loop to reach the goal
    while len(open_list) > 0:
        out_iter += 1
        expand_counter += 1
        #Find the current node
        current_node = open_list[0]
        current_index = 0
        #Get node in open list which has lower f value
        for index, x in enumerate(open_list):
            if x.f < current_node.f:
                current_node = x
                current_index = index
            if x.f == current_node.f: #tie-breaking rule, get node which has lower h value
                if x.h < current_node.h:
                    current_node = x
                    current_index = index
        #Assign the order of expansion to current_node
        current_node.counter = expand_counter

        #Return the path if iterating too much
        if out_iter > max_iter:
            print("Too Many Iterations: NO-PATH")
            return show_path(current_node, matrix)

        #Current node is popped out of open list, then added to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)
        #Mark visited tile as 1
        visited_tile[current_node.pos[0]][current_node.pos[1]] = 1

        #When the goal is found, search is ended
        if matrix[current_node.pos[0]][current_node.pos[1]] == 'G':
            visited_tile[current_node.pos[0]][current_node.pos[1]] = 1
            print()
            string_operator = str(current_node.operator + "-G")
            print(current_node.id, ":", string_operator,current_node.counter, current_node.g,
                  current_node.h, current_node.f)
            print()
            path_solution = str(show_path(current_node,matrix))
            return path_solution

        #Call children function to generate children
        id_count,openList,childrenList,visitedTile = children(current_node,matrix,id_counter,
                                                              open_list,closed_list,finish_node,visited_tile)
        id_counter = id_count
        open_list = openList
        children_list = childrenList
        visited_tile = visitedTile

        # Sample Output Format
        # Output N0:S 1 0 8 8
        #        Children: {N1: S-4, N2: S-D}
        #        OPEN: {(N1: S-R 2 6 8), (N2: S-D 2 7 9)}
        #        CLOSED: {(N0: S 0 8 8}
        print()
        print(current_node.id,":",current_node.operator, current_node.counter,current_node.g,
              current_node.h, current_node.f)
        string_children = []
        for ch in children_list:
            string_children.append(ch.id + ": " + ch.operator)
        print("Children: {",', '.join(string_children),"}")

        #Call print_flag function to show OPEN and CLOSED
        if diag_flag > 0:
            print_flag(open_list,closed_list)
            diag_flag -= 1

    #If no path was found
    print()
    print("NO-PATH")
    print()
    return show_path(current_node, matrix)

#If flag > 0, print OPEN list and CLOSED list
def print_flag(openList,closedList):
    open_list = openList
    closed_list = closedList

    string_open = []
    for op in open_list:
        string_open.append(op.id + ": " + op.operator + " " + str(op.g) + " " + str(op.h) + " " + str(op.f))
    print("OPEN: {", ', '.join(string_open), "}")
    string_close = []
    for cl in closed_list:
        string_close.append(cl.id + ": " + cl.operator + " " + str(cl.g) + " " + str(cl.h) + " " + str(cl.f))
    print("CLOSED: {", ', '.join(string_close), "}")

#Generate children nodes
def children(current,matrix_map,id_count,openList,closedList,end_node,visitedTile):
    current_node = current
    matrix = matrix_map
    id_counter = id_count
    open_list = openList
    closed_list = closedList
    finish_node = end_node
    visited_tile = visitedTile
    grandparent_node = current.parent
    if matrix[current_node.pos[0]][current_node.pos[1]] != 'S':
        grandparent_pos = (grandparent_node.pos[0],grandparent_node.pos[1])
    #Possible 8 actions
         #R    #RD    #D     #LD      #L      #LU       #U      #RU
    #[[0, 1],[1, 1],[1, 0],[1, -1],[0, -1],[-1, -1], [-1, 0],[-1, 1]]
    move = [[0, 1], [1, 1],[1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],  [-1, 1]]
    #Create a list for children
    children_list = []
    child_move_cost = 0
    operator = ""
    node_id = ""

    #Loop through possible move to find eligible child node
    for new_pos in move:
        #Get the position
        node_pos = (current_node.pos[0] + new_pos[0], current_node.pos[1] + new_pos[1])
        #Check if it is feasible
        if (node_pos[0]>(len(matrix) - 1)) or (node_pos[0]<0) or (node_pos[1]>(len(matrix) -1)) or (node_pos[1]<0):
            continue
        if (matrix[node_pos[0]][node_pos[1]] == 'X'):
            continue
        #Avoid going backward
        if (matrix[current_node.pos[0]][current_node.pos[1]] != 'S' and node_pos == grandparent_pos):
            continue
        #Skip visited tile
        if (visited_tile[node_pos[0]][node_pos[1]] == 1):
            continue

        #Check if it is within matrix map
        #RD [1,1] LD [1,-1], LU [-1,-1], RU [-1,1]
        #For a diagonal move, if x is top, below, left, or right of the child, the child cannot be visited
        x_top = (node_pos[0] - 1, node_pos[1])
        x_left = (node_pos[0], node_pos[1] - 1)
        x_below = (node_pos[0] + 1, node_pos[1])
        x_right = (node_pos[0], node_pos[1] + 1)

        if (new_pos == [1,1]):
            if (matrix[x_top[0]][x_top[1]]=='X' or matrix[x_left[0]][x_left[1]]=='X'):
                continue
        if (new_pos == [1,-1]):
            if (matrix[x_top[0]][x_top[1]]=='X' or matrix[x_right[0]][x_right[1]]=='X'):
                continue
        if (new_pos == [-1, -1]):
            if (matrix[x_right[0]][x_right[1]]=='X' or matrix[x_below[0]][x_below[1]]=='X'):
                continue
        if (new_pos == [-1, 1]):
            if (matrix[x_left[0]][x_left[1]]=='X' or matrix[x_below[0]][x_below[1]]=='X'):
                continue
        if (new_pos == [1,1] or new_pos == [1,-1] or new_pos == [-1, -1] or new_pos == [-1, 1]):
            child_move_cost = 1
            if (new_pos == [1,1]):
                operator = "RD"
            if (new_pos == [1,-1]):
                operator = "LD"
            if (new_pos == [-1, -1]):
                operator = "LU"
            if (new_pos == [-1, 1]):
                operator = "RU"

        #R [0,1] D [1,0], L [0,-1], U [-1,0]
        if (new_pos == [0, 1] or new_pos == [1, 0] or new_pos == [0, -1] or new_pos == [-1, 0]):
            child_move_cost = 2
            if (new_pos == [0,1]):
                operator = "R"
            if (new_pos == [1,0]):
                operator = "D"
            if (new_pos == [0,-1]):
                operator = "L"
            if (new_pos == [-1,0]):
                operator = "U"

        #Increase node id counter, create a child node, then append to the children list
        id_counter += 1
        #Create a node for new child
        new_child = Node(current_node, node_pos)
        new_child.operator = current_node.operator + "-" + operator
        new_child.id = "N" + str(id_counter)
        children_list.append(new_child)

        #Assign g value
        new_child.g = child_move_cost

    for ch in children_list:
        #Check if child is in the closed list
        for visited_ch in closed_list:
            if ch == visited_ch:
                continue
        #Assign g, h, f value for the child
        ch.g = ch.g + current_node.g
        # Heuristic function to calculate the distance, considering diagonal movement
        # Diagonal movement costs 1, other movements cost 2
        x_row = abs(ch.pos[0] - finish_node.pos[0])
        y_col = abs(ch.pos[1] - finish_node.pos[1])
        ch.h = max(x_row,y_col)
        ch.f = ch.g + ch.h

        #Child is already in open list
        for to_visit in open_list:
            if (ch == to_visit) and ch.g > to_visit.g:
                continue
        #If not in the open list, add child to the list to visit
        open_list.append(ch)

    return id_counter,open_list,children_list,visited_tile




def read_from_file(file_name):
    # You can change the file reading function to suit the way

    # you want to parse the file

    file_handle = open(file_name)

    map = file_handle.readlines()

    return map


###############################################################################

########### DO NOT CHANGE ANYTHING BELOW ######################################

###############################################################################


def write_to_file(file_name, solution):
    file_handle = open(file_name, 'w')

    file_handle.write(solution)


def main():
    # create a parser object

    parser = ap.ArgumentParser()

    # specify what arguments will be coming from the terminal/commandline

    parser.add_argument("input_file_name", help="specifies the name of the input file", type=str)

    parser.add_argument("output_file_name", help="specifies the name of the output file", type=str)

    parser.add_argument("flag", help="specifies the number of steps that should be printed", type=int)

    # parser.add_argument("procedure_name", help="specifies the type of algorithm to be applied, can be D, A", type=str)

    # get all the arguments

    arguments = parser.parse_args()

    ##############################################################################

    # these print statements are here to check if the arguments are correct.

    #    print("The input_file_name is " + arguments.input_file_name)

    #    print("The output_file_name is " + arguments.output_file_name)

    #    print("The flag is " + str(arguments.flag))

    #    print("The procedure_name is " + arguments.procedure_name)

    ##############################################################################

    # Extract the required arguments

    operating_system = platform.system()

    if operating_system == "Windows":

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("\\")

        if not re.match(r"(INPUT\\input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT\input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("\\")

        if not re.match(r"(OUTPUT\\output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT\output#.txt")

            return -1

    else:

        input_file_name = arguments.input_file_name

        input_tokens = input_file_name.split("/")

        if not re.match(r"(INPUT/input)(\d)(.txt)", input_file_name):
            print("Error: input path should be of the format INPUT/input#.txt")

            return -1

        output_file_name = arguments.output_file_name

        output_tokens = output_file_name.split("/")

        if not re.match(r"(OUTPUT/output)(\d)(.txt)", output_file_name):
            print("Error: output path should be of the format OUTPUT/output#.txt")

            return -1

    flag = arguments.flag

    # procedure_name = arguments.procedure_name

    try:

        map = read_from_file(input_file_name)  # get the map

    except FileNotFoundError:

        print("input file is not present")

        return -1

    # print(map)

    solution_string = ""  # contains solution

    solution_string = astarsearch(map, flag)

    write_flag = 1

    # call function write to file only in case we have a solution

    if write_flag == 1:
        write_to_file(output_file_name, solution_string)


if __name__ == "__main__":
    main()

