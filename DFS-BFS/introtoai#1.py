import sys
import os
import queue
from collections import deque
from collections import defaultdict
from collections import namedtuple
import re
#The input of the file needs to take the maximum size of the queue
#The input needs to choose a maximum number of states or depth
#The input needs to choose the set of dominoes
Domino = namedtuple("Domino", ['top', 'bottom'])
State = namedtuple("State", ["dominoes", "top","bot", "diff", "dif_let"])

def goal_State_Reach(top, bot):

    if top == bot:
        diff = "geminiMan"
        dif_let = top[len(bot):]

    elif top.startswith(bot):
        diff = "sadist"
        dif_let = top[len(bot):]

    elif bot.startswith(top):
        diff = "masochist"
        dif_let = bot[len(top):]
    else:
        return False
    return [diff , dif_let]

def BFS(maximum_queue, n_dominoes, dominoes, maximum_size):
    explored = {}
    frontier = []

    for n, d in dominoes.items():
        check = goal_State_Reach(d[0].strip(), d[1].strip())
        if check:
            frontier.insert(0, [d[0].strip(), d[1].strip()])
            if check[0] == "sadist":
                trash = ["", check[1]]
                if repr(trash) not in explored:
                    explored.update({str(trash): n})

            elif check[0] == "masochist":
                trash = [check[1], ""]
                if repr(trash) not in explored:
                    explored.update({str(trash): n})

    while frontier and len(frontier) < maximum_queue:
        state = frontier.pop()
        for n, d, in dominoes.items():
            a_ok = re.findall(r"[a-z]+", str(state))
            check = goal_State_Reach(a_ok[0].strip() + d[0].strip(), a_ok[1].strip() + d[1].strip())

            if check:
                if check[0] == "sadist":
                    trash = ["", check[1]]
                    if repr(trash) not in explored:
                        frontier.insert(0, [a_ok[0] + d[0], a_ok[1] + d[1]])
                        explored[str(trash)] = n

                elif check[0] == "masochist":
                    trash = [check[1], ""]
                    if repr(trash) not in explored:
                        frontier.insert(0, [a_ok[0] + d[0], a_ok[1] + d[1]])
                        explored[str(trash)] = n

                elif check[0] == "geminiMan":
                    return("Answer", a_ok[0].strip() + d[0].strip(), a_ok[1].strip() + d[1].strip(), frontier, explored)
    if not frontier:
        return "Failure"
    else:
        return iterative_deepening(maximum_size, maximum_queue, frontier, explored, dominoes)

def iterative_deepening(maximum, depth, frontier, explored, dominoes):

    for i in range(depth):
        state = frontier.pop()
        result = DFS(state, explored, 0, i, dominoes)
        if result:
            if "Solution Found!!!" == result[0]:
                return result
    return "Iterative deepening did not work"

def DFS(ctr, explored, phases, limit_depth, dominoes):
    if phases <= limit_depth:
        for n, d in dominoes.items():
            check = goal_State_Reach(ctr[0].strip() + d[0].strip(), ctr[1].strip() + d[1].strip())
            if check:
                if check[0] == "sadist":
                    trash = ["", check[1]]


                    if repr(trash) not in explored:
                        explored[str(trash)] = n
                        return DFS(trash, explored, phases + 1, limit_depth, dominoes)

                elif check[0] =="masochist":
                    trash = [check[1], ""]
                    if repr(trash) not in explored:
                        explored[str(trash)] = n
                        return DFS(trash, explored, phases + 1, limit_depth, dominoes)

                elif check[0] == "geminiMan":
                    return ("Answer", ctr[0].strip() + d[0].strip(), ctr[1].strip() + d[1].strip(), explored)
        if phases == limit_depth:
            return "Unfortunately, no solution was found in "  + str(phases)
    else :
        return "DFS did not succeed, try again next time champ"

def search_Argument(max_size_queue, n_dominoes, dominoes_in_dictionary, maximum_depth):
    mx_q = max_size_queue
    d_n = n_dominoes
    d_n_d = dominoes_in_dictionary
    m_d = maximum_depth
    result = BFS(mx_q, d_n, d_n_d, m_d)

    if result[0] == "Answer" :
        print("\nWe have found an answer.")
        sol = 0
        while sol < len(result):
            if sol != 0:
                if sol == 1:
                    print('\n')
                    print('top ' +'['+ result[1]+']')
                    print('\n')
                elif sol == 2:
                    print('bottom ' +'['+ result[2] +']')
                    print('\n')
                else:
                    print( '\n',result[sol],'\n')
            sol = sol+1
    else:
        print(result)

def remove(list):
    for i in list:
        list = [i.strip("0123456789\n \t") for i in list]
    print(list)

def make_dict(dominoes_file):
    domino_dictionary = {}
    for i in dominoes_file:
        split = i.split()
        domino_dictionary['D' + split[0]] = [split[1], split[2]]
    return domino_dictionary

def input_words(file_name):
    f = open(file_name, 'r')
    f = f.readlines()
    j = 0
    maxQueueSize = int(f[0])
    maxStates = int(f[1])
    outPutToken = bool(f[2])
    numberOfDominoes = int(f[3])
    dominoes_file = f[4: 7]
    for i in dominoes_file:
        domines_file = remove(dominoes_file)
    dominoes_input = make_dict(dominoes_file)
    print("\n")
    return maxQueueSize, maxStates, outPutToken, dominoes_input, numberOfDominoes


def main():
    maxQueueSize, maxStates, outPutToken, dominoes_input, numberOfDominoes  = input_words(sys.argv[1])
    print("Max Queue Size : " + str(maxQueueSize))
    print("The max depth is :" + str(maxStates))
    print("The output mode is :" + str(outPutToken))
    print("Number of dominoes is : " + str(numberOfDominoes) )
    print()

    print("Listed Dominoes: ")
    for k in dominoes_input:
        print('\n' ,k ,'[' , str(dominoes_input[k]), ']')
    print("\nSearching. . . .\n")
    answer = search_Argument(maxQueueSize, numberOfDominoes, dominoes_input, maxStates)


main()
