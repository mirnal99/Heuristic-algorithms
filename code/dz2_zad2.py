# -*- coding: utf-8 -*-
import zad1 as parser
import dz2_zad1
import random
import math
    
def getRandomNeighbour(solution): #zamjena dva random odabrana grada za dobivanje susjeda
    i = random.randint(0,len(solution)-1) # od 0 do n-1 jer randint uključuje oba ruba za razliku od range-a
    j = random.randint(0,len(solution)-1)
    while j==i: #ako su slučajno odabrani dva grada generiraj ponovno slučajni broj za j sve dok ne bude odabran grad različit od i
        j = random.randint(0,len(solution)-1)
    neighbour = solution.copy()
    neighbour[i] = solution[j]
    neighbour[j] = solution[i]
    return neighbour

#SA s prosljeđenom instancom, početnim rješenjem, početnom temperaturom, 
#temperaturom pri kojoj se zaustavlja i brojem iteracija na svakoj temperaturi
def simulatedAnnealingMakespan(csv_file,T0,Tmin,alpha,nbIterPerT):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)
    txt_SA1 = './DZ2/SA/SA_makespan.txt'
    txt_SA2 = './DZ2/SA/SA_makespan_solutions.txt'
    txt_SA3 = './DZ2/SA/SA_optimal_sol_makespan.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):

        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        #print(full_name, num_nodes,  matrix, windows)
        print("instanca: ", name)

        tsp = [x for x in range(num_nodes)]
        tsp = tsp[1:]
        print("cities: ", tsp)

        random.shuffle(tsp)
        solution = tsp
        print("sol= ",solution)


        T=T0
        fs = parser.calc_makespan(solution, matrix, full_name)
        s_best=solution.copy()
        f_best = fs
        while T>Tmin:
            i = 0
            c = 0
            d = 0
            while i < nbIterPerT:
                #print(i)
                s_1 = getRandomNeighbour(solution)
                fs_1 = parser.calc_makespan(s_1, matrix, full_name)
                diff = fs_1 - fs

                #POBOLJŠANJE ALGORITMA
                if fs_1 == f_best:
                    c = c+1
                    if c == 5:
                        i = i + 1

                        break
                else:
                    c=0

                if f_best < fs_1:
                    d = d+1
                    if d == 5:
                        i = i + 1

                        break
                else:
                    d=0

                if fs_1 < f_best:
                    f_best = fs_1
                    s_best = s_1.copy()
                if diff <=0:
                    solution = s_1
                    fs = fs_1
                else:
                    bound = math.exp(-1*diff/T)
                    rnb = random.random()
                    if rnb <= bound:
                        solution = s_1
                        fs = fs_1
                i+=1
                #print('T=%f, i=%d, s=%s, fs=%f'%(T,i,str(solution),fs))
            T = T*alpha

        instanca = name

        apsolutno, relativno, yn = dz2_zad1.odstupanja(f_best, instanca, csv_file)

        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1

        if f_best != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, s_best, f_best)
    #end for i

    return s_best, f_best
    

def simulatedAnnealingTraveltime(csv_file,T0,Tmin,alpha,nbIterPerT):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)
    txt_SA1 = './DZ2/SA/SA_traveltime.txt'
    txt_SA2 = './DZ2/SA/SA_traveltime_solutions.txt'
    txt_SA3 = './DZ2/SA/SA_optimal_sol_traveltime.txt'
    
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(instances)):

        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        #print(full_name, num_nodes,  matrix, windows)
        print("instanca: ", name)

        tsp = [x for x in range(num_nodes)]
        tsp = tsp[1:]
        print("cities: ", tsp)

        random.shuffle(tsp)
        solution = tsp
        print("sol= ",solution)

        T=T0
        #fs = routeLength(tsp,solution)
        fs = parser.calc_traveltime(solution, matrix, full_name)
        s_best=solution.copy()
        f_best = fs
        while T>Tmin:
            i = 0
            c = 0
            d = 0
            while i < nbIterPerT:
                print(i)
                s_1 = getRandomNeighbour(solution)
                #fs_1 = routeLength(tsp,s_1)
                fs_1 = parser.calc_traveltime(s_1, matrix, full_name)
                diff = fs_1 - fs

                #POBOLJŠANJE ALGORITMA
                if fs_1 == f_best:
                    c = c+1
                    if c == 5:
                        i = i + 1
                        #print("BREAK")
                        break
                else:
                    c=0

                if f_best < fs_1:
                    d = d+1
                    if d == 5:
                        i = i + 1
                        
                        break
                else:
                    d=0

                if fs_1 < f_best:
                    f_best = fs_1
                    s_best = s_1.copy()
                if diff <=0:
                    solution = s_1
                    fs = fs_1
                else:
                    bound = math.exp(-1*diff/T)
                    rnb = random.random()
                    if rnb <= bound:
                        solution = s_1
                        fs = fs_1
                i+=1
                #print('T=%f, i=%d, s=%s, fs=%f'%(T,i,str(solution),fs))
            T = T*alpha

        instanca = name

        apsolutno, relativno, yn = dz2_zad1.odstupanja(f_best, instanca, csv_file)
        parser.write1(txt_SA1, instanca, apsolutno, relativno, yn)
        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1
        parser.write2(txt_SA2, instanca, s_best, f_best)
        if f_best != float('inf'):
            valid_sol = valid_sol + 1

        print("res: ", full_name, s_best, f_best)
    #end for i

    parser.write_num_optimal(txt_SA3, num_optimal_sol, valid_sol)

    return num_optimal_sol


if __name__ == "__main__":

    csv_span = 'Makespan_Bounds.csv'
    csv_travel = 'Traveltime_Bounds.csv'
    
    T0 = 100
    Tmin = 0.01
    alpha = 0.9
    nbIterPerT = 5

    # uncomment THIS
    #--print(simulatedAnnealingMakespan(csv_span,T0,Tmin,alpha,nbIterPerT))
    #--print(simulatedAnnealingTraveltime(csv_travel,T0,Tmin,alpha,nbIterPerT))
