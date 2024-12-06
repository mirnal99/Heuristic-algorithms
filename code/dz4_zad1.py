import random
import matplotlib.pyplot as plt
import zad1 as parser
import dz2_zad1

def randomSolution(tsp):
	cities = list(range(len(tsp)))
	random.shuffle(cities)
	return cities
#end def

#napravi shuffle gradova ako je proslijeđena veličina problema
def randomSolution_perm(size):
	cities = list(range(size))
	cities = cities[1:]
	random.shuffle(cities)
	return cities
#end def

def routeLength(tsp, solution):
	sol = solution[:]
	sol.append(solution[0])
	routeLength = 0
	for i in range(len(sol)-1):
		routeLength += tsp[sol[i]][sol[i+1]]
	return routeLength
#end def

def problemGenerator(nCities):
	tsp = []
	for i in range(nCities):
		distances = []
		for j in range(nCities):
			if j==i:
				distances.append(0)
			elif j < i:
				distances.append(tsp[j][i])
			else:
				distances.append(random.randint(10,1000))
		tsp.append(distances)
	return tsp
#end def

#početna populacija se generira tako da se koristi funkcija randomSolution_perm sve dok se ne popuni populacija
def generate_population(size, ind_size):
	population = []
	for i in range(size):
		population.append(randomSolution_perm(ind_size))
	#end for i
	return population
#end def

#selekcija proporcionalna dobroti jedinke
def roulette_wheel_selection(pop, fitness_sum,  matrix, full_name, makespan = False):
	#sortiraj populaciju
	if makespan == True:
		sorted_population = sorted(pop, key=lambda x:  parser.calc_makespan(x, matrix, full_name))
	else:
		sorted_population = sorted(pop, key=lambda x:  parser.calc_traveltime(x, matrix, full_name))

	#generiraj gdje će kotač "stati"
	wheel = random.uniform(0,1)
	
	acc = 0
	for ind in sorted_population:
		#fitness = 1 / routeLength(tsp, ind)
		if makespan == True:
			if parser.calc_makespan(ind, matrix, full_name) == float('inf'):
				fitness = 0
			else:
				fitness = 1 / parser.calc_makespan(ind, matrix, full_name)
		else:
			if parser.calc_traveltime(ind, matrix, full_name) == float('inf'):
				fitness = 0
			else:
				fitness = 1 / parser.calc_traveltime(ind, matrix, full_name)

		#normiramo da dobijemo vjerojatnost
		if fitness_sum == 0:
			prob = float('inf')
		elif fitness_sum == float('inf'):
			prob = 0
		else:
			prob = fitness / fitness_sum
		acc += prob
		
		#ako si pronašao jedinku koja je odabrana završi i vrati tu jedinku
		if wheel <= acc:
			print("ind: ", ind)
			return ind
		#end if
	#end for ind
#end def

#k-turnirska selekcija
def k_tournament_selection(pop, k, matrix, full_name, makespan = False):
	sel = random.sample(pop, k) #odaberi k jedinki iz populacije

	if makespan == True:
		best_ind = min(sel, key=lambda x: parser.calc_makespan(x, matrix, full_name))
	else:
		best_ind = min(sel, key=lambda x: parser.calc_traveltime(x, matrix, full_name))
	return best_ind
#end def

#slijedno križanje  
"""križanje u kojem se određeni broj gena (definirano početnim i završnim genom) 
   preuzima iz prvog roditelja, a ostalo iz drugog roditelja"""
def order_crossover(par1, par2):
	child = []
	#pomoćne liste
	childP1 = []
	childP2 = []
	
	#slučajno odaberi početni i završni gen koji će se preuzeti od prvog roditelja
	geneA = int(random.random() * len(par1))
	geneB = int(random.random() * len(par1))
	
	startGene = min(geneA, geneB)
	endGene = max(geneA, geneB)
	
	#odredi što se preuzima iz prvog roditelja
	for i in range(startGene, endGene):
		childP1.append(par1[i])
	#end for i
	
	#ostali geni se preuzimaju iz drugog roditelja u istom redoslijedu
	childP2 = [el for el in par2 if el not in childP1]
	print("chid1, child2: ", childP1, childP2)
	#brojač za drugog roditelja
	j = 0
	
	"""napravi jedinku tako da između početnog i završnog gena uzmeš iz prvog 
	   roditelja, a preostalo popuniš ostalim gradovima uzevši u obzir 
	   redoslijed u roditelju 2 """
	for i in range(len(par1)):
		if startGene <= i < endGene:
			child.append(par1[i])
		else:
			child.append(childP2[j])
			j += 1
		#end if
	#end for i
	
	return child
#end def

#mutacija zamjenom - svaki element zamjeni s vjerojatnošću mutationRate
def swap_mutation(ind, mutationRate):
	for swapped in range(len(ind)):
		if random.random() < mutationRate:
			swapWith = int(random.random() * len(ind))
			ind[swapped], ind[swapWith] = ind[swapWith], ind[swapped]
		#end if
	#end for swapped
#end def

######################### eliminacijski #########################

#eliminacijski GA
def genetic_algorithm_ss_makespan(csv_file, pop_size, no_of_iterations, mutationRate):
	best_ind_fitness_list = []
	
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_GA1 = './DZ4/GA_eliminacijski/GA_elim_makespan.txt'
	txt_GA2 = './DZ4/GA_eliminacijski/GA_elim_makespan_solutions.txt'
	txt_GA3 = './DZ4/GA_eliminacijski/GA_elim_optimal_sol_makespan.txt'
	
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
		cities = [x for x in range(num_nodes)]
		cities = cities[1:]     
		random.shuffle(cities)
		print("cities: ", cities)
		ind_size = len(cities)      	
		
        #generiranje populacije
		pop = generate_population(pop_size, ind_size)
		it = 1
		c=0
		d=0
		prev_ind_value = float('inf')
		while it <= no_of_iterations:
			print("it: ", it)

        	#k-turnirska selekcija
			par1 = k_tournament_selection(pop, 3, matrix, full_name, makespan=True)
			par2 = k_tournament_selection(pop, 3, matrix, full_name, makespan=True)
			child = order_crossover(par1, par2) #slijedno križanje
			print("par1, par2, child: ", par1, par2, child)
			swap_mutation(child, mutationRate) #mutacija zamjenom    

        	#slučajno odaberi tri jedinke i najlošiju među njima zamijeni novonastalom jedinkom
			sel = random.sample(pop, 3)
			sel = sorted(sel, key=lambda x: parser.calc_makespan(x, matrix, full_name))
			print("sel= ", sel)
			pop[pop.index(sel[2])] = child      

			best_ind = min(pop, key=lambda x: parser.calc_makespan(x, matrix, full_name))
			best_ind_value = parser.calc_makespan(best_ind, matrix, full_name)
			
			#poboljšanje algoritma
			if best_ind_value == prev_ind_value:
				c = c+1
				if c == 15:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break
			if prev_ind_value < best_ind_value:
				d = d + 1
				if d == 15:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break

			prev_ind_value = best_ind_value
			print(it, ". iteration, best obj_value found: ", best_ind_value, sep="")
			best_ind_fitness_list.append(best_ind_value)        
			it += 1     
			print("res: ", name, best_ind, best_ind_value)
			
            
			
		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_ind_value, name, csv_file)
		parser.write1(txt_GA1, name, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
			
		parser.write2(txt_GA2, name, best_ind, best_ind_value)
		if best_ind_value != float('inf'):
			valid_sol = valid_sol + 1
				
	parser.write_num_optimal(txt_GA3, num_optimal_sol, valid_sol)
			
	return num_optimal_sol, valid_sol, best_ind_fitness_list
	
#eliminacijski GA
def genetic_algorithm_ss_traveltime(csv_file, pop_size, no_of_iterations, mutationRate):
	best_ind_fitness_list = []
	
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_GA1 = './DZ4/GA_eliminacijski/GA_elim_traveltime.txt'
	txt_GA2 = './DZ4/GA_eliminacijski/GA_elim_traveltime_solutions.txt'
	txt_GA3 = './DZ4/GA_eliminacijski/GA_elim_optimal_sol_traveltime.txt'
	
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
		random.shuffle(cities)
		print("cities: ", cities)
		ind_size = len(cities)      	
		
        #generiranje populacije
		pop = generate_population(pop_size, ind_size)
		it = 1
        
		c=0
		d=0
		prev_ind_value = float('inf')
		while it <= no_of_iterations:
			print("it: ", it)

        	#k-turnirska selekcija
			par1 = k_tournament_selection(pop, 3, matrix, full_name, makespan=False)
			par2 = k_tournament_selection(pop, 3, matrix, full_name, makespan=False)
			child = order_crossover(par1, par2) #slijedno križanje
			print("par1, par2, child: ", par1, par2, child)
			swap_mutation(child, mutationRate) #mutacija zamjenom    

        	#slučajno odaberi tri jedinke i najlošiju među njima zamijeni novonastalom jedinkom
			sel = random.sample(pop, 3)
			sel = sorted(sel, key=lambda x: parser.calc_traveltime(x, matrix, full_name))
			print("sel= ", sel)
			pop[pop.index(sel[2])] = child      
			best_ind = min(pop, key=lambda x: parser.calc_traveltime(x, matrix, full_name))
			best_ind_value = parser.calc_traveltime(best_ind, matrix, full_name)
			
			#poboljšanje algoritma
			if best_ind_value == prev_ind_value:
				c = c+1
				if c == 15:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break
			if prev_ind_value < best_ind_value:
				d = d + 1
				if d == 15:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break
				
			prev_ind_value = best_ind_value
			print(it, ". iteration, best obj_value found: ", best_ind_value, sep="")
			best_ind_fitness_list.append(best_ind_value)        
			it += 1     
			print("res: ", name, best_ind, best_ind_value)
			
            
		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_ind_value, name, csv_file)
		parser.write1(txt_GA1, name, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
			
		parser.write2(txt_GA2, name, best_ind, best_ind_value)
		if best_ind_value != float('inf'):
			valid_sol = valid_sol + 1
				
	parser.write_num_optimal(txt_GA3, num_optimal_sol, valid_sol)
			
	return num_optimal_sol, valid_sol, best_ind_fitness_list


######################### generacijski #########################

def genetic_algorithm_generation_makespan(csv_file, pop_size, no_of_iterations, mutationRate, elitism=False):
	best_ind_fitness_list = []
	
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_GA1 = './DZ4/GA_generacijski/GA_gen_makespan.txt'
	txt_GA2 = './DZ4/GA_generacijski/GA_gen_makespan_solutions.txt'
	txt_GA3 = './DZ4/GA_generacijski/GA_gen_optimal_sol_makespan.txt'
	
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
		random.shuffle(cities)
		print("cities: ", cities)
        #solution = cities
        #print("sol= ",solution)
		
		ind_size = len(cities)
		
		pop = generate_population(pop_size, ind_size)
		it = 1
		c=0
		d=0
		prev_ind_value = float('inf')
		while it <= no_of_iterations:
			temp_pop = []
	    	#ako je uključen elitizam
			if elitism:
				temp_pop = sorted(pop, key=lambda x: parser.calc_makespan(x, matrix, full_name))[:5]
				txt_GA1 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_makespan.txt'
				txt_GA2 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_makespan_solutions.txt'
				txt_GA3 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_optimal_sol_makespan.txt'
				
			while len(temp_pop) < pop_size:
	    			#k-turnirska selekcija
				#par1 = k_tournament_selection(pop, 3, matrix, full_name, makespan=True)
				#par2 = k_tournament_selection(pop, 3, matrix, full_name, makespan=True)
				#child = order_crossover(par1, par2)
				#swap_mutation(child, mutationRate)
				#temp_pop.append(child)
				
					#roulette wheel selekcija
				fitness_sum = 0
				for ind in pop:
					if parser.calc_makespan(ind, matrix, full_name) == float('inf'):
						fitness_sum += 0
					else:
						fitness_sum += 1 /	parser.calc_makespan(ind, matrix, full_name)
				#end for ind
				par1 = roulette_wheel_selection(pop, fitness_sum,  matrix, full_name, makespan = True)
				par2 = roulette_wheel_selection(pop, fitness_sum,  matrix, full_name, makespan = True)

				#slijedno križanje
				child = order_crossover(par1, par2)

				#mutacija zamjenom
				swap_mutation(child, mutationRate)

				#dodaj novonastalu jedinku u sljedeću generaciju
				temp_pop.append(child)
				
			pop = temp_pop
			best_ind = min(pop, key=lambda x: parser.calc_makespan(x, matrix, full_name))
			best_ind_value = parser.calc_makespan(best_ind, matrix, full_name)
			
			#poboljšanje algoritma
			if best_ind_value == prev_ind_value:
				c = c+1
				if c == 5:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break
				
			if prev_ind_value < best_ind_value:
				d = d + 1
				if d == 5:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1

					break
				
			prev_ind_value = best_ind_value
			print(it, ". iteration, best obj_value found: ", best_ind_value, sep="")
			best_ind_fitness_list.append(best_ind_value)
			it += 1
		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_ind_value, name, csv_file)
		parser.write1(txt_GA1, name, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
			
		parser.write2(txt_GA2, name, best_ind, best_ind_value)
		if best_ind_value != float('inf'):
			valid_sol = valid_sol + 1
				
	parser.write_num_optimal(txt_GA3, num_optimal_sol, valid_sol)
    
	return best_ind, best_ind_value, best_ind_fitness_list

def genetic_algorithm_generation_traveltime(csv_file, pop_size, no_of_iterations, mutationRate, elitism=False):
	best_ind_fitness_list = []
	
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_GA1 = './DZ4/GA_generacijski/GA_gen_traveltime.txt'
	txt_GA2 = './DZ4/GA_generacijski/GA_gen_traveltime_solutions.txt'
	txt_GA3 = './DZ4/GA_generacijski/GA_gen_optimal_sol_traveltime.txt'
	
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
		random.shuffle(cities)
		print("cities: ", cities)
		
		ind_size = len(cities)
		
		pop = generate_population(pop_size, ind_size)
		it = 1
		c=0
		d=0
		prev_ind_value = float('inf')
		while it <= no_of_iterations:
			temp_pop = []
			
	    	#ako je uključen elitizam
			if elitism:
				temp_pop = sorted(pop, key=lambda x: parser.calc_traveltime(x, matrix, full_name))[:5]
				
				txt_GA1 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_traveltime.txt'
				txt_GA2 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_traveltime_solutions.txt'
				txt_GA3 = './DZ4/GA_generacijski_elitizam/GA_gen_elit_optimal_sol_traveltime.txt'
				
			while len(temp_pop) < pop_size:
	    		#k-turnirska selekcija
				par1 = k_tournament_selection(pop, 3, matrix, full_name, makespan=False)
				par2 = k_tournament_selection(pop, 3, matrix, full_name, makespan=False)
				child = order_crossover(par1, par2) #slijedno križanje
				swap_mutation(child, mutationRate) #mutacija zamjenom
				temp_pop.append(child) #dodaj novonastalu jedinku u sljedeću generaciju
				
			pop = temp_pop
			best_ind = min(pop, key=lambda x: parser.calc_traveltime(x, matrix, full_name))
			best_ind_value = parser.calc_traveltime(best_ind, matrix, full_name)
			
			#poboljšanje algoritma
			if best_ind_value == prev_ind_value:
				c = c+1
				if c == 5:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1
					print("BREAK")
					break
				
			if prev_ind_value < best_ind_value:
				d = d + 1
				if d == 5:
					best_ind_fitness_list.append(best_ind_value)        
					it += 1
					print("BREAK kod d")
					break
				
			prev_ind_value = best_ind_value
			print(it, ". iteration, best obj_value found: ", best_ind_value, sep="")
			best_ind_fitness_list.append(best_ind_value)
			it += 1
			
		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_ind_value, name, csv_file)
		parser.write1(txt_GA1, name, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
			
		parser.write2(txt_GA2, name, best_ind, best_ind_value)
		if best_ind_value != float('inf'):
			valid_sol = valid_sol + 1
				
	parser.write_num_optimal(txt_GA3, num_optimal_sol, valid_sol)
    
	return best_ind, best_ind_value, best_ind_fitness_list


if __name__ == "__main__":

	csv_travel = 'Traveltime_Bounds.csv'
	csv_span = 'Makespan_Bounds.csv'
	
	pop_size = 20
	no_of_iterations = 50
	mutationRate = 0.05

	#--UNCOMMENT THIS - eliminacijski
	#print(genetic_algorithm_ss_makespan(csv_span, pop_size, no_of_iterations, mutationRate))
	#print(genetic_algorithm_ss_traveltime(csv_travel, pop_size, no_of_iterations, mutationRate))

	##pop_size = 100
	##no_of_iterations = 50
	##mutationRate = 0.1

	#--UNCOMMENT THIS - generacijski
	#print(genetic_algorithm_generation_makespan(csv_span, pop_size, no_of_iterations, mutationRate, elitism=False))
	#print(genetic_algorithm_generation_traveltime(csv_travel, pop_size, no_of_iterations, mutationRate, elitism=False))

	#generacijski s roulette 
	#//

	#--generacijski WITH ELITISM
	#print(genetic_algorithm_generation_makespan(csv_span, pop_size, no_of_iterations, mutationRate, elitism=True))
	#print(genetic_algorithm_generation_traveltime(csv_travel, pop_size, no_of_iterations, mutationRate, elitism=True))

	#best_ind, best_ind_value, best_ind_fitness_list = genetic_algorithm_ss_makespan(csv_span, pop_size, no_of_iterations, mutationRate)
	#plt.plot(range(len(best_ind_fitness_list)), best_ind_fitness_list, label="Eliminacijski GA")
	
	#plt.ylabel("Distance")
	#plt.xlabel("Generation")
	#plt.legend()
	#plt.show()
#end main
