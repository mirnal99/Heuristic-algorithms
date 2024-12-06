import random
import numpy as np
from itertools import combinations
from matplotlib import pyplot
import zad1 as parser
import dz2_zad1 

def randomSolution(tsp): 
    cities = list(range(len(tsp)))
    random.shuffle(cities)
    return cities

def PSO_traveltime(csv_file, n=10, no_it=500, w=0.8, alpha = 0.3, beta = 0.3):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)

    txt_PSO1 = './DZ3/PSO/PSO_traveltime.txt'
    txt_PSO2 = './DZ3/PSO/PSO_traveltime_solutions.txt'
    txt_PSO3 = './DZ3/PSO/PSO_optimal_sol_traveltime.txt'

    num_optimal_sol = 0
    valid_sol = 0
    
    for i in range(len(instances)):
        
        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        print("instanca: ", name)

        cities = [x for x in range(num_nodes)]
        cities = cities[1:]
        print("cities: ", cities)

        #initalize particles
        particles = []

        #početne čestice su nasumično generirane, permutacija gradova
        for i in range(n):
            particles.append(randomSolution(cities))
        #end for i
        print("PARTICLES = ", particles)

        particles_obj = [] #lista za spremanje funkcije cilja radi ubrzanja
        for particle in particles:
            #particles_obj.append(routeLength(tsp,particle))
            print("particle= ", particle)
            particles_obj.append(parser.calc_traveltime(particle, matrix, full_name))
        #end for particles

        #postavi početna rješenja kao ujedno i najbolje za svaku česticu
        pbest = particles.copy() 
        pbest_obj = particles_obj.copy() #spremi i vrijednosti funkcije cilja
        gbest = particles[np.argmin(particles_obj)].copy() #pronađi najbolju česticu
        gbest_obj = min(particles_obj) #i njezinu dobrotu
        print('random solution objective (particles):')
        print(pbest_obj)

        v = [] #velocity
        #za svaku česticu izračunaj velocity
        for particle in particles:
            so = [] #pravimo listu s mogućim zamjenama
            for swap in combinations([x for x in range(len(cities))],2):
                so.append(swap)
            #end for swap

            ss = [] #niz so, svaki velocity će biti sastavljen od 2 nasumična
            #vjerojatnost zamjene postavi na inerciju
            ss.append((random.choice(so),w))
            ss.append((random.choice(so),w))
            v.append(ss)
        #end for particle

        c = 0
        d = 0
        #ponavljaj no_it iteracija
        for it in range(no_it):
            print("it: ", it)
            #za svaku česticu
            for i in range(len(particles)):
                #za svaki njezin indeks tj grad
                for j in range(len(cities)):
                    """provjeri odgovara li onome što se nalazi u najboljem
                       pronađenom rješenju s tom česticom"""
                    if particles[i][j] != pbest[i][j]:
                        """ako ne, spremi u niz promjena (ss) uređeni par indeks u
                           trenutnoj čestici gdje se nalazi taj grad i u pbest
                           vjerojatnost s kojom će se napraviit taj pomak je alpha"""
                        v[i].append(((j, pbest[i].index(particles[i][j])),alpha))
                    #end if
                #end for j

                #za svaki njezin indeks tj grad
                for j in range(len(cities)):
                    #provjeri odgovara li onome što se nalazi u najboljem globalno pronađenom rješenju 
                    if particles[i][j] != gbest[j]:
                        """ako ne, spremi u niz promjena (ss) uređeni par indeks
                            u trenutnoj čestici gdje se nalazi taj grad i u gbest
                            vjerojatnost s kojom će se napraviit taj pomak je beta"""
                        v[i].append(((j, gbest.index(particles[i][j])),beta))
                    #end if
                #end for j

                #prođi svakim korakom, i ako je vjerojatnost manja od vjerojatnosti pridružene tom pomaku napravi pomak
                for (swap,prob) in v[i]:
                    if random.random() <= prob:
                       particles[i][swap[0]],particles[i][swap[1]] = \
                            particles[i][swap[1]],particles[i][swap[0]]
                    #end if
                #end for (swap,prob)

                #izračunaj dobrotu dobivene čestice
                particles_obj[i] = parser.calc_traveltime(particles[i], matrix, full_name)

                #po potrebi ažuriraj pbest
                if particles_obj[i] < pbest_obj[i]:
                    pbest_obj[i] = particles_obj[i]
                    pbest[i] = particles[i].copy()
                #end if

                #velocity se sastoji od zadnja dva pomaka
                v[i] = [(v[i][-2][0], w), (v[i][-1][0], w)]
            #end for i

            #nakon što su napravljene sve nove čestice, provjeri je li potrebno ažurirati globalno najbolje rješenje
                
            
            #POBOLJŠANJE ALGORITMA?
            print(gbest_obj, min(particles_obj))
            if gbest_obj == min(particles_obj):
                c = c+1
                if c == 10:
                    gbest = particles[np.argmin(particles_obj)].copy()
                    print("BREAK")
                    break
            else:
                c = 0

            if gbest_obj < min(particles_obj):
                d = d+1
                if d == 10:
                    gbest = particles[np.argmin(particles_obj)].copy()
                    print("BREAK kod d")
                    break
            else:
                d = 0
                     
            
            if gbest_obj > min(particles_obj): 
                gbest_obj = min(particles_obj)
                gbest = particles[np.argmin(particles_obj)].copy()
                #print(gbest, gbest_obj)
            #end if
                
        print(gbest, gbest_obj)
        instanca = name
		#print("INSTANCA=", instanca)

        apsolutno, relativno, yn = dz2_zad1.odstupanja(gbest_obj, instanca, csv_file)
        print("writing 1st file traveltime")
        parser.write1(txt_PSO1, instanca, apsolutno, relativno, yn)
        if yn == 'DA':
            num_optimal_sol = num_optimal_sol + 1
        print("writing 2nd traveltime")
        parser.write2(txt_PSO2, instanca, gbest, gbest_obj)
        if gbest_obj != float('inf'):
            valid_sol = valid_sol + 1


    #end for it
    parser.write_num_optimal(txt_PSO3, num_optimal_sol, valid_sol)
    return num_optimal_sol

#end def

def PSO_makespan(csv_file, n=10, no_it=500, w=0.8, alpha = 0.3, beta = 0.3):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)

    txt_PSO1 = './DZ3/PSO/PSO_makespan.txt'
    txt_PSO2 = './DZ3/PSO/PSO_makespan_solutions.txt'
    txt_PSO3 = './DZ3/PSO/PSO_optimal_sol_makespan.txt'

    num_optimal_sol = 0
    valid_sol = 0
    
    for i in range(len(instances)):
        
        folder_name = folder[i]
        prefix = parser.add_prefix(folder_name)
        name = instances[i]
        full_name = prefix+name
        num_nodes, matrix, windows = parser.read_txt(full_name)
        print("instanca: ", name)

        cities = [x for x in range(num_nodes)]
        cities = cities[1:]
        print("cities: ", cities)

        #initalize particles
        particles = []

        #početne čestice su nasumično generirane, permutacija gradova
        for i in range(n):
            #particles.append(randomSolution(tsp))
            particles.append(randomSolution(cities))
        #end for i
        print("PARTICLES = ", particles)

        particles_obj = [] #lista za spremanje funkcije cilja radi ubrzanja
        for particle in particles:
            #particles_obj.append(routeLength(tsp,particle))
            print("particle= ", particle)
            particles_obj.append(parser.calc_makespan(particle, matrix, full_name))
        #end for particles

        #postavi početna rješenja kao ujedno i najbolje za svaku česticu
        pbest = particles.copy() 
        pbest_obj = particles_obj.copy() #spremi i vrijednosti funkcije cilja
        gbest = particles[np.argmin(particles_obj)].copy() #pronađi najbolju česticu
        gbest_obj = min(particles_obj) #i njezinu dobrotu
        print('random solution objective (particles):')
        print(pbest_obj)

        v = [] #velocity
        #za svaku česticu izračunaj velocity
        for particle in particles:
            so = [] #pravimo listu s mogućim zamjenama
            for swap in combinations([x for x in range(len(cities))],2):
                so.append(swap)
            #end for swap

            ss = [] #niz so, svaki velocity će biti sastavljen od 2 nasumična
            #vjerojatnost zamjene postavi na inerciju
            ss.append((random.choice(so),w))
            ss.append((random.choice(so),w))
            v.append(ss)
        #end for particle

        c = 0
        d = 0
        #ponavljaj no_it iteracija
        for it in range(no_it):
            print("it: ", it)
            #za svaku česticu
            for i in range(len(particles)):
                #za svaki njezin indeks tj grad
                for j in range(len(cities)):
                    #provjeri odgovara li onome što se nalazi u najboljem pronađenom rješenju s tom česticom
                    if particles[i][j] != pbest[i][j]:
                        """ako ne, spremi u niz promjena (ss) uređeni par indeks u
                            trenutnoj čestici gdje se nalazi taj grad i u pbest
                            vjerojatnost s kojom će se napraviit taj pomak je alpha"""
                        v[i].append(((j, pbest[i].index(particles[i][j])),alpha))
                    #end if
                #end for j

                #za svaki njezin indeks tj grad
                for j in range(len(cities)):
                    #provjeri odgovara li onome što se nalazi u najboljem globalno pronađenom rješenju 
                    if particles[i][j] != gbest[j]:
                        """ako ne, spremi u niz promjena (ss) uređeni par indeks
                            u trenutnoj čestici gdje se nalazi taj grad i u gbest
                            vjerojatnost s kojom će se napraviit taj pomak je beta"""
                        v[i].append(((j, gbest.index(particles[i][j])),beta))
                    #end if
                #end for j

                #prođi svakim korakom, i ako je vjerojatnost manja od vjerojatnosti pridružene tom pomaku napravi pomak
                for (swap,prob) in v[i]:
                    if random.random() <= prob:
                       particles[i][swap[0]],particles[i][swap[1]] = \
                            particles[i][swap[1]],particles[i][swap[0]]
                    #end if
                #end for (swap,prob)

                #izračunaj dobrotu dobivene čestice
                particles_obj[i] = parser.calc_makespan(particles[i], matrix, full_name)

                #po potrebi ažuriraj pbest
                if particles_obj[i] < pbest_obj[i]:
                    pbest_obj[i] = particles_obj[i]
                    pbest[i] = particles[i].copy()
                #end if

                #velocity se sastoji od zadnja dva pomaka
                v[i] = [(v[i][-2][0], w), (v[i][-1][0], w)]
            #end for i

            #nakon što su napravljene sve nove čestice, provjeri je li potrebno ažurirati globalno najbolje rješenje
            
            
            #POBOLJŠANJE ALGORITMA?
            print(gbest_obj, min(particles_obj))
            if gbest_obj == min(particles_obj):
                c = c+1
                if c == 10:
                    gbest = particles[np.argmin(particles_obj)].copy()
                    print("BREAK")
                    break
            else:
                c = 0

            if gbest_obj < min(particles_obj):
                d = d+1
                if d == 10:
                    gbest = particles[np.argmin(particles_obj)].copy()
                    print("BREAK kod d")
                    break
            else:
                d = 0
            
            
            if gbest_obj > min(particles_obj): 
                gbest_obj = min(particles_obj)
                gbest = particles[np.argmin(particles_obj)].copy()
            #end if
                
        print(gbest, gbest_obj)
        instanca = name

        apsolutno, relativno, yn = dz2_zad1.odstupanja(gbest_obj, instanca, csv_file)
        print("writing 1st file traveltime")
        parser.write1(txt_PSO1, instanca, apsolutno, relativno, yn)
        if yn == 'DA':
            num_optimal_sol = num_optimal_sol + 1
        print("writing 2nd traveltime")
        parser.write2(txt_PSO2, instanca, gbest, gbest_obj)
        if gbest_obj != float('inf'):
            valid_sol = valid_sol + 1


    #end for it
    parser.write_num_optimal(txt_PSO3, num_optimal_sol, valid_sol)
    return num_optimal_sol

#end def

if __name__ == "__main__":

    #gbest, gbest_obj = PSO(tsp, 20, 1000, 0.8, 0.5, 0.5)
    #print(f'Global best solution: {gbest}, objective: {gbest_obj}')

    csv_travel = 'Traveltime_Bounds.csv'
    csv_span = 'Makespan_Bounds.csv'

    """
    n = 20
    no_it = 1000
    w = 0.8
    alpha = 0.3
    beta = 0.3
    """
    #print(PSO_traveltime(csv_travel, n, no_it, w, alpha, beta))

    """
    n=50
    no_it=1000
    w=2
    alpha = 0.5
    beta = 0.5
    """

    n=10
    no_it=300
    w=0.8
    alpha = 0.3
    beta = 0.3

    #--uncomment THIS
    print(PSO_makespan(csv_span, n, no_it, w, alpha, beta))
    print(PSO_traveltime(csv_travel, n, no_it, w, alpha, beta))
    #--


#end main
