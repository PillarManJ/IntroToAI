import sys
import math
import struct
from collections import Counter


#Step 1 : First we must open the file and unpack our data
def input_file(input):
    vector = dict()
#    exemplar = dict()
    t = ()
    set = []
    k = 0
    c_value = []
    fp = open(input, "r")
    for line in fp.readlines():
        t = line[0:len(line)-4].rsplit(",")
        c_value = line[len(line)-2]
        for index, element in enumerate(t):
                a = float(element)
                set.append(a)
        vector[tuple(set)] = c_value
        set = set[0:-k]
        k = 0
    return vector



#Step 2 : We must make an exemplar function
def create_exemplar(vector):
    k = 0
    exemplar_value = 0
    denominator = 0
    numerator = 1
    representative = str()
    c_value = str()
    v1 = []
    c1 = []
    t_value = float()
    exemplar_vector = {}
    tmp = ()
    for kk,vv, in vector.items():
        c_value = vector.get(kk)
        if representative != c_value:
            c1.append(c_value)
            if denominator != 0:
                t_value = numerator/denominator
            denominator = 0
            denominator +=1
            representative = c_value
        else:
            c1.append(c_value)
            denominator += 1
    for index, element in enumerate(vector):
        tmp = element
        for x in tmp:
            v1.append(x*t_value)
            k+=1
        #print(k)
        exemplar_vector[tuple(v1)] = c1[exemplar_value]
        #print(exemplar_vector)
        exemplar_value+=1
        v1 = v1[:-k]
        k = 0
    #I need a way of adding all vectors of similar class variables, a definition would make it cleaner...
    exemplar_vector = vector_mathematics(exemplar_vector)
    return exemplar_vector

#Generate A Random number between the min and max for each predictive attribute.
#Basically for each exemplar I have, create a random vector. Random vector is just k random values.
#The purpose of that is that in Gradient Descent, there is a random parameter.
#If the random value is true
#Then
#exemplars = random_generate()
#else :
#exemplars = centroids

def vector_mathematics(vector):
    x1 = []
    y1 = []
    z1 = []
    tmp = []
    saved = []
    saved2 = []
    fin_vector = {}
    c_value = str()
    k = 0
    for kk, vv in vector.items():
        if k == 0:
            k+=1
            class_value = vv
            x1 = list(kk)
            continue
        if k > 0 and class_value == vv:
            if x1 != []:
                y1 = list(kk)
            else:
                x1 = list(kk)
            for i in range(0, len(y1)):
                tmp.append(x1[i] + y1[i])
                saved = tmp
            x1 = tmp
            tmp = tmp[0:-len(tmp)]
            k += 1
            if k == len(vector.items()):
                fin_vector[tuple(saved)] = class_value
        if k > 0 and class_value != vv:
            x1 = list(kk)
            for i in range(0, len(saved)):
                z1.append(saved[i])
                #print(saved[i])
            fin_vector[tuple(z1)] = class_value
            z1 = z1[:-len(z1)]
            class_value = vv
            k+=1
            #Update class value
    return(fin_vector)


def calculate_distance(vector_x, vector_y):
    #x2 = []
    #y2 = []
    distance = 0.0
    distance += 0.01
    #tmp = []
    #saved = []
    saved1 = float()
    saved2 = float()
    for i in range(0, len(vector_x)):
        saved1 = vector_x[i]
        saved2 = vector_y[i]
        distance += pow((saved1 - saved2),2)
    return(distance)

def classify(exemplar_vector, training_set):
    c_value = str()
    distance = 0
    lowest = 0
    x4 = []
    y4 = []
    #print("The exemplar vector:", exemplar_vector)
    #print("\n")
    #print("The training set:", training_set)
    z4 = dict()
    best_w = 0
    for kk, vv in exemplar_vector.items():
        x4 = list(kk)
        #print("x4 is:", x4)
        z4[vv] = training_set
        for xx, yy in z4.items():
            y4 = list(yy)
        #    print("y4 is:", y4)
            distance = calculate_distance(x4, y4)
            if lowest == 0:
                lowest = distance
                z4[xx]= list(yy)
                best_w = xx
            if distance < lowest:
                lowest = distance
                z4[xx] = list(yy)
                best_w = xx
            #print(distance)
            #print("Reclassifying vector", y4,"to", vv)
        lowest = 0
    return(z4, best_w)


def reclassify(exemplar_x, exemplar_y):
    distance = 0
    lowest = 0
    best_w = 0
    x = []
    y = []
    z = {}
    z = exemplar_y
    for xx, yy in exemplar_x.items():
        x = list(xx)
        for key, val in exemplar_y.items():
            y = list(key)
            distance = calculate_distance(x, y)
            if lowest == 0:
            #    print(distance)
                lowest = distance
                z[key] = yy
            if distance < lowest:
                lowest = distance
                z[key] = yy
        lowest = 0
    return(z)





def cost_function(M, exemplar_vector, training_set):
    closest_exemplar = False
    x5 = []
    y5 = []
    closest_ex_vec = []
    lowest = 0
    cost = 0
    for kk, vv in exemplar_vector.items():
            x5 = list(kk)
            for xx, yy in training_set.items():
                y5 = list(xx)
                if lowest == 0:
                    distance = calculate_distance(x5, y5)
                    lowest = distance
                distance = calculate_distance(x5, y5)
                #print(distance)
                if lowest > distance:
                    lowest = distance
                    closest_ex_vec = list(xx)
                    closest_exemplar = True
                    cost = min(M, (calculate_distance(x5, y5) - calculate_distance(closest_ex_vec, y5)))
                else:
                    continue
                closest_exemplar = False
            #print("the cost is of re-classification is", cost)
    return(cost)

#TODO VECTOR ADD AND VECTOR SUBTRACT:


def computeAccuracy(exemplar_vector, training_set):
    k = 0
    numerator = 0
    accuracy = float()
    #print("the exemplar vector of computeAccuracy is: ",exemplar_vector)
    #print("\n")
    #print("the training set of computeAccuracy is: ", training_set)
    new_set = reclassify(exemplar_vector, training_set)
    #print("\n")
    #print("The exemplar vector is : ", exemplar_vector)
    #print("\nThe new set is :", new_set)
    #print("\n")
    #print("This is the training set:" , training_set)

    for kk, vv in zip(new_set.items(), training_set.items()):
        if (vv == kk):
    #        print("vv is :", vv)
    #        print("kk is :", kk)
            numerator += 1
        k+=1
    accuracy = numerator/k
    #print("Accuracy: ", accuracy)
    return(accuracy)

def vec_sub(vector_x, vector_y):
    diff = float()
    for i, j in zip(vector_x, vector_y):
        diff += (i - j)
    return(diff)

def vec_add(vector_x, vector_y):
    sum = float()
    for i, j in zip(vector_x, vector_y):
        sum += (i + j)
    return(sum)



def gradDescent(training_set, stepSize, epsilon, M, random_val):
    if random_val == True:
        exemplars = create_exemplar(training_set)
        #print(exemplars)
        #TODO Create random_generate() function and it will be assigned exemplar if random_val == True
    else:
        exemplars = create_exemplar(training_set)
        #print(exemplars)
    PrevCost = float('inf')
    #print("The exemplars in gradient descent are", exemplars)
    #PrevAccuracy = computeAccuracy(exemplars, training_set)
    while True:
        TotalCost = 0.0
        n = dict()
        for key,value in exemplars.items():
            c = exemplars[key]
            exemplar_key = key
            #TODO c needs to be printed
            #n[c] = [0.0]*len(exemplars[c])
        for y in training_set:
            v = training_set[y]
            y = list(y)
            #print("v is :",v)
            #print("The exemplar vectors: ",exemplars)
            g_w, w = classify(exemplars, y)
            #print("The vector of g_w is: ", g_w)
            if v != w :
                Cost = calculate_distance(exemplar_key, y) - calculate_distance(y, g_w[w])
                if Cost < M :
                    #n[v]
                    print(exemplar_key)
                    #Need a way to add and subtract two vectors.
                    #TODO
                    #s = vec_sub(y, exemplar[v])
                    s = vec_sub(y, exemplar_key)
                    vec_add(n[v], s)
                    n[w] = vec_add(n[w], vec_sub(exemplar[w], y))
                    TotalCost+= Cost
                else :
                    TotalCost += M

        if TotalCost < epsilon :
            return exemplars
        if TotalCost > (1-epsilon)*PrevCost :
            return exemplars
        h = {}
        for vec in exemplars:
            c = exemplars[vec]
            h[c] = vec_add(exemplars[c], vec_multiply(stepsize, n[v]))
        NewAccuracy = computeAccuracy(h, training_set)
        if NewAccuracy < PrevAccuracy:
            return exemplars
        for vec in exemplars:
            c = exemplars[vec]
            exemplars[c] = h[c]




def main():
    distance_vector = []
    vector = dict()
    accuracy = 0
    x3 = []
    y3 = []
    exemplar = dict()
    vector = input_file(sys.argv[1])
    M = float(sys.argv[2])
    stepSize = float(sys.argv[3])
    epsilon = float(sys.argv[4])
    randomRestarts = int(sys.argv[5])

    #exemplar = create_exemplar(vector)
    #print(exemplar)
    #print("\n")
    exemplars = gradDescent(vector, stepSize, epsilon, M, False)
    #accuracy = computeAccuracy(exemplars, vector)
    #accuracy = computeAccuracy(list(kk), list(vv))
    #print(accuracy)
    for i in range(0, randomRestarts):
        exemplars = gradDescent(vector, stepSize, epsilon, M, True) #Returns the exemplars
        accuracy = computeAccuracy(exemplars, vector)
    print("The accuracy is: ", accuracy)
    #computeAccuracy(exemplar, vector)
    #print(vector)
    #print(exemplar)
    #cost_function(M, exemplar, vector)
    #vector = classify(exemplar, vector)




if __name__ == '__main__':
    main()
