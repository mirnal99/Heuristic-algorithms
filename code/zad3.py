import random
import zad1 as parser
import zad2 as greedy

#-------------- 2-opt --------------#

def getNeighbours2opt(solution, matrix, full_name, makespan = False):
    n = len(solution)
    n2 = int(n*0.1)
    #better_sol = False
    for i in range(n):
        print("i: ", i)
        for j in range(i+1, n2):
            curr1 = (solution[i], solution[i+1])
            curr2 = (solution[j], solution[(j+1)%n])
            curr_dist = matrix[solution[i]][solution[i+1]] + matrix[solution[j]][solution[(j+1)%n]]
            print(curr1, curr2, curr_dist)

            new1 = (solution[i], solution[j])
            new2 = (solution[i+1], solution[j+1])
            new_dist = matrix[solution[i]][solution[j]] + matrix[solution[i+1]][ solution[j+1]]

            if new_dist < curr_dist:
                #better_sol = True
                print("swap edges ", curr1, curr2, " with ", new1, new2)
                solution[i+1:j+1] = solution[i+1:j+1][::-1]
    
    if makespan == True:
        cost = parser.calc_makespan(solution, matrix, full_name)
    else:
        cost = parser.calc_traveltime(solution, matrix, full_name)

    return solution, cost

def localSearchMakespan(csv_file):
    folder, instances, permutation, time, l1, l2, l3 = greedy.pohlepno_makespan(csv_file)
    txt_local1 = './DZ1/LocalSearch/2opt_makespan.txt'
    txt_local2 = './DZ1/LocalSearch/2opt_makespan_solutions.txt'
    txt_local3 = './DZ1/LocalSearch/2opt_optimal_sol_makespan.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):
        folder_name = folder[i]
        pocetno_greedy = l2[i]
        full_name = l1[i]
        matrix = l3[i]
        name = instances[i]

        solution, cost = getNeighbours2opt(pocetno_greedy, matrix, full_name, makespan=True)
        #print("sol: ", solution, cost)

        instanca = name
        apsolutno, relativno, yn = parser.odstupanje(cost, instanca, csv_file)
        print("writing 1st file makespan")
        parser.write1(txt_local1, instanca, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1

        print("writing 2nd file makespan")
        parser.write2(txt_local2, instanca, solution, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, solution, cost)

    print(parser.write_num_optimal(txt_local3, num_optimal_sol, valid_sol))
    return num_optimal_sol

def localSearchTraveltime(csv_file):
    folder, instances, permutation, time, l1, l2, l3 = greedy.pohlepno_traveltime(csv_file)
    txt_local1 = './DZ1/LocalSearch/2opt_traveltime.txt'
    txt_local2 = './DZ1/LocalSearch/2opt_traveltime_solutions.txt'
    txt_local3 = './DZ1/LocalSearch/2opt_optimal_sol_traveltime.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):
        folder_name = folder[i]
        pocetno_greedy = l2[i]
        full_name = l1[i]
        matrix = l3[i]
        name = instances[i]

        solution, cost = getNeighbours2opt(pocetno_greedy, matrix, full_name, makespan=False)
        #print("sol: ", solution, cost)

        instanca = name
        apsolutno, relativno, yn = parser.odstupanje(cost, instanca, csv_file)
        print("writing 1st file makespan")
        parser.write1(txt_local1, instanca, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1

        print("writing 2nd file makespan")
        parser.write2(txt_local2, instanca, solution, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, solution, cost)

    print(parser.write_num_optimal(txt_local3, num_optimal_sol, valid_sol))
    return num_optimal_sol

#-------------- random swap --------------#

def getIndex(city, tsp):
    for i in range(len(tsp)):
        if tsp[i] == city:
            return i

def randomSwapMakespan(csv_file):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)
    txt_local1 = './DZ1/LocalSearch/swap_makespan.txt'
    txt_local2 = './DZ1/LocalSearch/swap_makespan_solutions.txt'
    txt_local3 = './DZ1/LocalSearch/swap_optimal_sol_makespan.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):
        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        print("instanca: ", name)

        #random pocetno rjesenje
        cities = [x for x in range(num_nodes)]
        cities = cities[1:]
        print("cities: ", cities)
        solution = cities

        n = len(solution)
        print("n: ", n)
        if n<=30:
            n2 = int(n*0.5)
        n2 = int(n*0.1)
        print("n2: ", n2)
        
        for k in range(n):
            temp_sol = solution
            visited = []
            for j in range(k+1, n2):
                print("k: ", k)
                print("j: ", j)
                curr1 = solution[k]
                index1 = getIndex(curr1, solution)
                print("curr1: ", curr1, index1)

                curr2 = random.choice(solution[k+1:n2])
                #drugi grad izaberi td nije vec posjecen i da nije jednak prvom
                while(curr2 in visited or curr2 == curr1):
                    curr2 = random.choice(solution[k+1:n2])
                    #print("curr2 iz while: ", curr2)

                visited.append(curr2)
                index2 = getIndex(curr2, solution)
                print("curr2: ", curr2, index2)
                print("visited: ", visited)

                #do swap
                for z in range(len(solution)):
                    if z == index1:
                        temp_sol[z] = curr2
                    if z == index2:
                        temp_sol[z] = curr1
    
                curr_dist = parser.calc_makespan(solution, matrix, full_name)
                new_dist = parser.calc_makespan(temp_sol, matrix, full_name)
    
                if new_dist < curr_dist:
                    solution = temp_sol
    
                print(curr1, curr2, curr_dist)

        cost = parser.calc_makespan(solution, matrix, full_name)

        instanca = name
        apsolutno, relativno, yn = parser.odstupanje(cost, instanca, csv_file)
        print("writing 1st file makespan")
        parser.write1(txt_local1, instanca, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1

        print("writing 2nd file makespan")
        parser.write2(txt_local2, instanca, solution, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, solution, cost)

    print(parser.write_num_optimal(txt_local3, num_optimal_sol, valid_sol))
    return num_optimal_sol
    
def randomSwapTraveltime(csv_file):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)
    txt_local1 = './DZ1/LocalSearch/swap_traveltime.txt'
    txt_local2 = './DZ1/LocalSearch/swap_traveltime_solutions.txt'
    txt_local3 = './DZ1/LocalSearch/swap_optimal_sol_traveltime.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):
        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        print("instanca: ", name)

        #random pocetno rjesenje
        cities = [x for x in range(num_nodes)]
        cities = cities[1:]
        print("cities: ", cities)
        solution = cities

        n = len(solution)
        print("n: ", n)
        if n<=30:
            n2 = int(n*0.5)
        n2 = int(n*0.1)
        print("n2: ", n2)
        
        for k in range(n):
            temp_sol = solution
            visited = []
            for j in range(k+1, n2):
                print("k: ", k)
                print("j: ", j)
                curr1 = solution[k]
                index1 = getIndex(curr1, solution)
                print("curr1: ", curr1, index1)

                curr2 = random.choice(solution[k+1:n2])
                while(curr2 in visited or curr2 == curr1):
                    curr2 = random.choice(solution[k+1:n2])
                    #print("curr2 iz while: ", curr2)
                visited.append(curr2)
                index2 = getIndex(curr2, solution)
                print("curr2: ", curr2, index2)
                print("visited: ", visited)
    
                #do swap
                for z in range(len(solution)):
                    if z == index1:
                        temp_sol[z] = curr2
                    if z == index2:
                        temp_sol[z] = curr1
    
                curr_dist = parser.calc_traveltime(solution, matrix, full_name)
                new_dist = parser.calc_traveltime(temp_sol, matrix, full_name)
    
                if new_dist < curr_dist:
                    solution = temp_sol
    
                print(curr1, curr2, curr_dist)

        cost = parser.calc_traveltime(solution, matrix, full_name)

        instanca = name
        apsolutno, relativno, yn = parser.odstupanje(cost, instanca, csv_file)
        print("writing 1st file makespan")
        parser.write1(txt_local1, instanca, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1

        print("writing 2nd file makespan")
        parser.write2(txt_local2, instanca, solution, cost)
        if cost != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, solution, cost)

    print(parser.write_num_optimal(txt_local3, num_optimal_sol, valid_sol))
    return num_optimal_sol

if __name__ == "__main__":

    csv_travel = 'Traveltime_Bounds.csv'
    csv_span = 'Makespan_Bounds.csv'

    #print(localSearchMakespan(csv_span))
    #print(localSearchTraveltime(csv_travel))

    #print(randomSwapMakespan(csv_span))
    #print(randomSwapTraveltime(csv_travel))