# -*- coding: utf-8 -*-

import random
from matplotlib import pyplot
import zad1 as parser
import zad2 as greedy
import dz2_zad1 


def hybrid_ACO_TABU_makespan(csv_file, m, ro, max_it, br_azur, alpha=1):
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_hybrid1 = './DZ3/Hybrid/hybrid_makespan.txt'
	txt_hybrid2 = './DZ3/Hybrid/hybrid_makespan_solutions.txt'
	txt_hybrid3 = './DZ3/Hybrid/hybrid_optimal_sol_makespan.txt'
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
		best = cities.copy()
		
		best_eval = parser.calc_makespan(best, matrix, full_name)
		trails = [[1.0/5000]*(len(cities)+1)]*(len(cities)+1)
	
		it = 0
		ants = [] #lista u koju spremamo putanju svakog od m mravi
		scores = []

		tsp = cities 
		c = 0
		d = 0

		while it < max_it:
			it += 1
			print("it= ", it)
			# za svakog mrava pozovi doWalk funkciju koja "gradi" rješenje
			for i in range(m):
				ants.append(doWalk(tsp, trails))


			# sortiraj mrave po dobroti (kraći put = bolji mrav)
			ants = sorted(ants, key=lambda x: parser.calc_makespan(x, matrix, full_name))

			# samo najboljih br_azur mrava ostavlja feromonski trag
			updateTrails(ants[:br_azur], tsp, trails, matrix, full_name, True)

			# ispari feromonski trag
			evaporateTrails(trails, ro)
			
            # pronađi najbolje rješenje
			current_best = ants[0]
			print("current best: ", current_best)
			if it%5 == 0:
				print("djeljiv s 5")
				sol, cost = dz2_zad1.fixed_korak_tabu_makespan(current_best, full_name, matrix)
				current_best = sol
				print("new best: ", current_best)
				current_best_eval = cost
			else:
				current_best_eval = parser.calc_makespan(current_best, matrix, full_name)


			#POBOLJŠANJE ALGORITMA
			print(current_best_eval, best_eval)
			if current_best_eval == best_eval:
				c = c+1
				if c == 5:
					ants = ants[:br_azur]
					break
			else:
				c = 0

			if best_eval < current_best_eval:
				d = d+1
				if d == 5:
					ants = ants[:br_azur]
					break
			else:
				d = 0

			#ako je trenutno najbolje rješenje bolje od globalno najboljeg
			if current_best_eval < best_eval:
				best, best_eval = current_best, current_best_eval
				scores.append(best_eval)
			#end if

			ants = ants[:br_azur] #uzmi samo najboljih br_azur mrava

		instanca = name

		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_eval, instanca, csv_file)
		#print(apsolutno, relativno, yn)
		print("writing 1st file makespan")
		parser.write1(txt_hybrid1, instanca, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
		
		print("writing 2nd file makespan")
		parser.write2(txt_hybrid2, instanca, best, best_eval)
		if best_eval != float('inf'):
			valid_sol = valid_sol + 1

		print("res: ", full_name, best, best_eval, scores)
	
	print(parser.write_num_optimal(txt_hybrid3, num_optimal_sol, valid_sol))
	return num_optimal_sol
	
def hybrid_ACO_TABU_traveltime(csv_file, m, ro, max_it, br_azur, alpha=1):
	folder, instances, best_cost= parser.read_best_solutions(csv_file)
	txt_hybrid1 = './DZ3/Hybrid/hybrid_traveltime.txt'
	txt_hybrid2 = './DZ3/Hybrid/hybrid_traveltime_solutions.txt'
	txt_hybrid3 = './DZ3/Hybrid/hybrid_optimal_sol_traveltime.txt'
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
		best = cities.copy()
		

		best_eval = parser.calc_traveltime(best, matrix, full_name)
		trails = [[1.0/5000]*(len(cities)+1)]*(len(cities)+1)
		
		it = 0
		ants = [] #lista u koju spremamo putanju svakog od m mravi
		scores = []

		tsp = cities 
		c = 0
		d = 0

		while it < max_it:
			it += 1
			print("it= ", it)

			# za svakog mrava pozovi doWalk funkciju koja "gradi" rješenje
			for i in range(m):
				#print("DO WALK")
				ants.append(doWalk(tsp, trails))

			# sortiraj mrave po dobroti (kraći put = bolji mrav)
			ants = sorted(ants, key=lambda x: parser.calc_traveltime(x, matrix, full_name))

			# samo najboljih br_azur mrava ostavlja feromonski trag
			#print("UPDATE TRAILS")
			updateTrails(ants[:br_azur], tsp, trails, matrix, full_name, True)
			
			# ispari feromonski trag
			#print("EVAPORATE TRAILS")
			evaporateTrails(trails, ro)
			
            # pronađi najbolje rješenje
			current_best = ants[0]
			print("current best: ", current_best)
			if it%10 == 0:
				print("djeljiv s 10")
				sol, cost = dz2_zad1.fixed_korak_tabu_traveltime(current_best, full_name, matrix)
				current_best = sol
				print("new best: ", current_best)
				current_best_eval = cost
			else:
				current_best_eval = parser.calc_traveltime(current_best, matrix, full_name)

			#POBOLJŠANJE ALGORITMA
			print(current_best_eval, best_eval)
			if current_best_eval == best_eval:
				c = c+1
				if c == 5:
					ants = ants[:br_azur]
					break
			else:
				c = 0

			if best_eval < current_best_eval:
				d = d+1
				if d == 5:
					ants = ants[:br_azur]
					break
			else:
				d = 0

			#ako je trenutno najbolje rješenje bolje od globalno najboljeg
			if current_best_eval < best_eval:
				best, best_eval = current_best, current_best_eval
				scores.append(best_eval)
			#end if
			
			ants = ants[:br_azur] #uzmi samo najboljih br_azur mrava

		instanca = name

		apsolutno, relativno, yn = dz2_zad1.odstupanja(best_eval, instanca, csv_file)
		print("writing 1st file makespan")
		parser.write1(txt_hybrid1, instanca, apsolutno, relativno, yn)
		if yn == "DA":
			num_optimal_sol = num_optimal_sol + 1
		
		parser.write2(txt_hybrid2, instanca, best, best_eval)
		if best_eval != float('inf'):
			valid_sol = valid_sol + 1
		print("writing 2nd file makespan")

		print("res: ", full_name, best, best_eval, scores)

	print(parser.write_num_optimal(txt_hybrid3, num_optimal_sol, valid_sol))
	return num_optimal_sol
	

#end def

def doWalk(tsp, trails, alpha=1):
	cities = tsp
	random.shuffle(cities) #svaki grad NE može biti početni
	
	sol = [cities[0]]
	
	# kamo dalje?
	while len(sol) != len(cities):
		prev = sol[-1] #zadnji grad stavljen u rješenje
		prob = {} #izračunaj vjerojatnost prelaska u preostale gradove
		
		for city in cities:
			if city not in sol:
				prob[(prev, city)] = trails[prev][city] ** alpha
			#end if
		#end for city
		
		# normalizacija - da dobiješ vjerojatnost
		norm = sum(prob.values())
		for item in prob:
			prob[item] /= norm
		#end for item
		
		# odaberi grad koji ima maksimalnu vjerojatnost prelaska
		sol.append(max(prob, key=prob.get)[1])
	#end while
	return sol
#end def

def updateTrails(ants, tsp, trails, matrix, full_name, makespan = False):
	for ant in ants:
		#delta = 1 / routeLength(tsp, ant) #izračunaj dobrotu rješenja mrava
		if makespan == True:
			delta = 1 / parser.calc_makespan(ant, matrix, full_name)
		else:
			delta = 1 / parser.calc_traveltime(ant, matrix, full_name)
		# ažuriraj trag feromona s obzirom na dobrotu
		for i in range(1, len(ant)):
			prev, curr = ant[i-1], ant[i]
			trails[prev][curr] += delta

			#trgovački putnik -> simetrična matrica
			trails[curr][prev] = trails[prev][curr]
		#end for i
	#end for ant
#end def

def evaporateTrails(trails, ro):
	for i in range(len(trails)):
		for j in range(len(trails[i])):
			trails[i][j] *= (1-ro)
		#end for j
	#end for i
#end def

if __name__ == "__main__":
	
	csv_travel = 'Traveltime_Bounds.csv'
	csv_span = 'Makespan_Bounds.csv'

	#m = 40
	#ro =  0.2 
	#max_it = 500
	#br_azur = 20
	#alpha=1
	#best, score, scores = simpleACOtraveltime(csv_travel, m, ro, max_it, br_azur, alpha=1)

	m = 10
	ro =  0.2 
	max_it = 50
	br_azur = 5 #10
	alpha=1

	#--uncomment THIS
	print(hybrid_ACO_TABU_makespan(csv_span, m, ro, max_it, br_azur, alpha=1))
	#print(hybrid_ACO_TABU_traveltime(csv_travel, m, ro, max_it, br_azur, alpha=1))
	#-----------------
	

	# line plot of best scores
	#pyplot.plot(scores, ".-")
	#pyplot.xlabel("Broj poboljšanja")
	#pyplot.ylabel("Evaluacija f(x)")
	#pyplot.show()

	
#end main
