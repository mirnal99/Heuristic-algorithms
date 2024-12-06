import zad1 as parser
#import pandas as pd
import csv


def get_instances(csv_name):
    instances = []
    folder = []
    with open(csv_name) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            folder.append(row[0])
            instances.append(row[1])
    del instances[0]
    del folder[0]

    return folder, instances


def korak_traveltime(num_nodes, matrix):
    l = []
    for i in range(num_nodes):
        l.append(i)

    #print("l= ", l)
    depot = l[0]
    previous = depot
    posjeceno = [0]
    k = l[1:]
    time = 0

    for i in range(len(l)-1):
        if l == []:
            
            return posjeceno
        l.remove(previous)
        #print("l= ", l)
        a = l[0]
        #print("a= ", a)
        min = matrix[previous][a]
        #print("min = ", min)
        for j in l:
            #print("j: ", j)
            if matrix[previous][j] < min:
                min = matrix[previous][j]
                #print("new min: ", min)
                a = j
                #print("new a: ",a)

        time = time + min
        #print("time= ", time)
        posjeceno.append(a)
        #print("posjeceno: ", posjeceno)
        previous = a
        #print("previous: ", a)

    last = matrix[previous][0]
    #print("last: ", last)
    time = time + last
    #print("time: ", time)

    results = posjeceno[1:]
    time = round(time,2)

    return results, time


def korak_makespan(num_nodes, matrix, windows):
    l = []
    for i in range(num_nodes):
        l.append(i)

    #print("l: ", l)
    #print(windows)
    temp = l[1:]

    windows_earliest = []
    for w in windows:
        #print(w)
        windows_earliest.append(w[0])
    
    #print("windows: ", windows_earliest)

    rjecnik = dict(zip(l, windows_earliest))
    #print(rjecnik)

    sorted_by_earliest = sorted(rjecnik.items(), key=lambda x:x[1])
    #print(sorted_by_earliest) 

    time = 0
    #print("time ", time)
    a = sorted_by_earliest[0][0]
    #print("a ", a)
    time = time + matrix[0][a]
    #print("time ", time)
    temp3 = l[1:]
    #print("temp3 ", temp3)
    for i in temp3:
        #print("i: ", i)
        time = time + matrix[a][i]
        #print("time ", time)
        if time < sorted_by_earliest[i][1]:
            wait = sorted_by_earliest[i][1] - time
            time = time + wait
            #print("time after waiting ", time)
            a = i
            #print("a ", a)
        a = i
        #print("a ", a)

    last_elem = sorted_by_earliest[-1][0]
    #print("last elem ", last_elem)
    if time < sorted_by_earliest[-1][1]:
        wait = sorted_by_earliest[-1][1] - time
        time = time + wait

    depot = l[0]
    time = time + matrix[last_elem][depot]
    #print("final time ", time)

    permutation = []
    for i in sorted_by_earliest:
        a = i[0]
        permutation.append(a)

    time = round(time,2)

    return permutation, time


def pohlepno_traveltime(csv_file):
    folder, instances = get_instances(csv_file)
    k = -1

    l1 = []
    l2 = []
    l3 = []

    txt_pohlepno1 = './DZ1/Greedy/greedy_traveltime.txt'
    txt_pohlepno2 = './DZ1/Greedy/greedy_traveltime_solutions.txt'
    txt_pohlepno3 = './DZ1/Greedy/greedy_optimal_sol_traveltime.txt'
    num_optimal_sol = 0
    valid_sol = 0

    for i in instances:
        k = k+1
        file_name = i
        #print(i)
        name = folder[k]
        prefix = parser.add_prefix(name)
        #print("prefix : ", prefix)
        #print("FILE NAME ", file_name)
        full_file_name = prefix+file_name
        
        num_nodes, matrix, windows = parser.read_txt(full_file_name)
        #print(num_nodes, matrix,windows)

        permutation, time = korak_traveltime(num_nodes, matrix)
        cost = parser.calc_traveltime(permutation, matrix, full_file_name)

        #print(permutation, time)
        apsolutno, relativno, yn = parser.odstupanja(full_file_name, file_name, csv_file)
        #print(apsolutno, relativno, yn)
        
        l1.append(full_file_name)
        l2.append(permutation)
        l3.append(matrix)
        
        #--parser.writing_traveltime('pohlepno_traveltime.txt', csv_file)
        
        #--parser.write1(txt_pohlepno1, file_name, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1
        #--parser.write2(txt_pohlepno2, file_name, permutation, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1
        #print("res: ", full_file_name, permutation, cost)


    print(parser.write_num_optimal(txt_pohlepno3, num_optimal_sol, valid_sol))
    #return num_optimal_sol
    return folder, instances, permutation, time, l1, l2, l3

def pohlepno_makespan(csv_file):
    folder, instances = get_instances(csv_file)
    k = -1

    l1 = []
    l2 = []
    l3 = []

    txt_pohlepno1 = './DZ1/Greedy/greedy_makespan.txt'
    txt_pohlepno2 = './DZ1/Greedy/greedy_makespan_solutions.txt'
    txt_pohlepno3 = './DZ1/Greedy/greedy_optimal_sol_makespan.txt'
    num_optimal_sol = 0
    valid_sol = 0

    for i in instances:
        k = k+1
        file_name = i
        #print(i)
        name = folder[k]
        prefix = parser.add_prefix(name)

        full_file_name = prefix+file_name
        num_nodes, matrix, windows = parser.read_txt(full_file_name)
        #print(num_nodes, matrix,windows)
        
        permutation, time = korak_makespan(num_nodes, matrix, windows)
        cost = parser.calc_makespan(permutation, matrix, full_file_name)

        apsolutno, relativno, yn = parser.odstupanja(full_file_name, file_name, csv_file)
        #print(apsolutno, relativno, yn)

        
        #--parser.writing_makespan('pohlepno_makespan.txt', csv_file)
        #l1.append(name)
        #l2.append(permutation)
        l1.append(full_file_name)
        l2.append(permutation)
        l3.append(matrix)

        #--parser.write1(txt_pohlepno1, file_name, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1
        #--parser.write2(txt_pohlepno2, file_name, permutation, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1
        print("res: ", full_file_name, permutation, cost)


    print(parser.write_num_optimal(txt_pohlepno3, num_optimal_sol, valid_sol))
    #return num_optimal_sol

    #return folder, instances, permutation, time, l2
    return folder, instances, permutation, time,l1, l2, l3

"""
def printaj_sve(txt_name, csv_travel, csv_span):
    folder, instances, _, _, _ = pohlepno_traveltime(csv_travel)
    l1 = []
    l2 = []

    for i in range(len(instances)):
        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = prefix+instances[i]

        num_nodes, matrix, windows = parser.read_txt(name)
        permutation, time = korak_makespan(num_nodes, matrix, windows)
        _, traveltime = korak_traveltime(num_nodes, matrix)

        
        #parser.write_file(txt_name, name, permutation, traveltime, time)
        l1.append(name)
        l2.append(permutation)

    return(l1,l2)

"""


if __name__ == "__main__":
    csv_travel = 'Traveltime_Bounds.csv'
    csv_span = 'Makespan_Bounds.csv'

    #----uncomment for writing in 'pohlepno_traveltime.txt'
    print(pohlepno_traveltime(csv_travel))

    #----uncomment for writing in 'pohlepno_makespan.txt'
    print(pohlepno_makespan(csv_span))

    
    #print(printaj_sve('pohlepno_results.txt', csv_travel, csv_span))
    