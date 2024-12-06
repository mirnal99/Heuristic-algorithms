import zad1 as parser
import zad2

def count_time(l,matrix, file_name):
    num_nodes, _, windows = parser.read_txt(file_name)
    counter = 0
    time = 0
    traveltime = 0
    b = False
    a = l[0]

    time = time + matrix[0][a]
    traveltime = traveltime + matrix[0][a]

    if time >= windows[a][0] and time <= windows[a][1]:
        b=True
    else:
        b=False
        counter = counter + 1

    for p in l[1:]:
        time = time + matrix[a][p]
        traveltime = traveltime + matrix[a][p]
        if time >= windows[p][0] and time <= windows[p][1]:
            b = True
            a = p
        elif time < windows[p][0]:
            wait_time = windows[p][0] - time
            time = time + wait_time
            b = True
            a = p
        elif time > windows[p][1]:
            b = False
            counter = counter + 1
            a=p

    last_elem = l[-1]
    depot = 0
    time = time + matrix[last_elem][depot]
    traveltime = traveltime + matrix[last_elem][depot]

    time = round(time, 2) #zaokruzi na 2 decimale kao sto je u best known solutions
    makespan = time
    traveltime = round(traveltime, 2)

    cost = 0
    if counter != 0:
        cost = float('inf')

    return makespan, traveltime, cost


def korak_tabu_traveltime(pocetno, full_file_name, matrix):
    pocetno_pohlepno = pocetno
    n = len(pocetno_pohlepno)

    TL = []
    dic = {}
    cost = 0
    
    full_file_name = full_file_name
    matrix = matrix

    iter = 0
    n2 = n*0.1
    for i in range(n):
        print("i= ", i)
        for j in range(i+1,n-1):
            #print("j= ", j)

            remove = []
            for k,v in dic.items():
                if v == 0:
                    r = k
                    remove.append(r)
                    TL.remove(k)

            for z in remove:
                dic.pop(z)

            for k,v in dic.items():
                dic[k] = v-1

            #uzmi dva brida s trenutnog puta
            curr1 = (pocetno_pohlepno[i], pocetno_pohlepno[i+1])
            curr2 = (pocetno_pohlepno[j], pocetno_pohlepno[(j+1)%n])
            #curr_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[i+1]] + matrix[pocetno_pohlepno[j]][ pocetno_pohlepno[(j+1)%n]]
    
            if curr1 not in TL and curr2 not in TL:

                #prespajanje, dobijemo dva nova brida i novu udaljenost
                #new1 = (pocetno_pohlepno[i], pocetno_pohlepno[j])
                #new2 = (pocetno_pohlepno[i+1], pocetno_pohlepno[j+1])
                #new_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[j]] + matrix[pocetno_pohlepno[i+1]][ pocetno_pohlepno[j+1]]

                _,curr_travel_time,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                save = pocetno_pohlepno[i+1:j+1]
                pocetno_pohlepno[i+1:j+1] = pocetno_pohlepno[i+1:j+1][::-1]
                _,new_travel_time,_ = count_time(pocetno_pohlepno, matrix, full_file_name)

                if new_travel_time < curr_travel_time:
                    #print("curr: ", curr_travel_time, " new: ", new_travel_time)
                    #print("swap edges ", curr1, curr2, " with ", new1, new2)
                    TL.append(curr1)
                    TL.append(curr2)
                    #print("append to TL= ", TL)

                    dic[TL[-1]] = 2
                    dic[TL[-2]] = 2
                    #print("dic ", dic)

                else:
                    pocetno_pohlepno[i+1:j+1] = save

            else:
                pocetno_pohlepno[i+1:j+1] = save
                #print("l se ne mijenja = ", pocetno_pohlepno )
                #print("bridovi ", curr1, curr2, "su trenutno u TABU listi")


    sol = pocetno_pohlepno
    _,travel_time,cost = count_time(sol, matrix, full_file_name)
    
    message = ""
    if cost != 0:
        message = "rješenje nije dopustivo, inf"

    else:
        cost = travel_time

    return sol, travel_time, message, cost


def odstupanja(time, file_name, csv_file):
    folder, instances, best_cost= parser.read_best_solutions(csv_file)

    k=-1
    for i in instances:
        k=k+1
        if i == file_name:
            najbolje_rj = best_cost[k]
            najbolje_rj = float(najbolje_rj)
    
    temp1 = najbolje_rj-time
    apsolutno = abs(temp1)
    #print("apsolutno: ", apsolutno)
    relativno = apsolutno/(abs(najbolje_rj))
    #print("relativno: ", relativno)

    yn = "NE"
    if time == najbolje_rj:
        yn = "DA"
    else:
        yn = "NE"

    return apsolutno, relativno, yn


def tabu_traveltime(csv_file):
    folder, instances, permutation, time,l1, l2, l3 = zad2.pohlepno_traveltime(csv_file)
    list2 = []
    txt_name = 'dz2_tabu_traveltime.txt'
    txt_name2 = 'dz2_tabu_traveltime_solutions.txt'

    file_names = []
    solutions = []
    times = []
    messages = []
    costs = []

    for i in range(len(l1)):
        pocetno = l2[i]
        full_file_name = l1[i]
        matrix = l3[i]
        file_name = instances[i]

        sol, travel_time, message, cost = korak_tabu_traveltime(pocetno, full_file_name, matrix)
        file_names.append(file_name)
        solutions.append(sol)
        times.append(travel_time)
        messages.append(message)
        costs.append(cost)

        apsolutno, relativno, yn = odstupanja(travel_time, file_name, csv_file)
        print(apsolutno, relativno, yn)
        parser.write1(txt_name, file_name, apsolutno, relativno, yn)
        parser.write2(txt_name2, file_name, sol, cost)

    return file_names, solutions, times, messages, costs 

#-------------------------------makespan-----------------------------------------
def korak_tabu_makespan(pocetno, full_file_name, matrix):
    pocetno_pohlepno = pocetno
    n = len(pocetno_pohlepno)

    TL = []
    dic = {}
    cost = 0

    full_file_name = full_file_name
    matrix = matrix
   
    for i in range(n):
        print("i= ", i)
        for j in range(i+1,n-1):
            #print("j= ", j)
            remove = []
            for k,v in dic.items():
                if v == 0:
                    r = k
                    remove.append(r)
                    TL.remove(k)

            for z in remove:
                dic.pop(z)

            for k,v in dic.items():
                dic[k] = v-1

            #uzmi dva brida s trenutnog puta
            curr1 = (pocetno_pohlepno[i], pocetno_pohlepno[i+1])
            curr2 = (pocetno_pohlepno[j], pocetno_pohlepno[(j+1)%n])
            #curr_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[i+1]] + matrix[pocetno_pohlepno[j]][ pocetno_pohlepno[(j+1)%n]]

            if curr1 not in TL and curr2 not in TL:

                #prespajanje, dobijemo dva nova brida i novu udaljenost
                #new1 = (pocetno_pohlepno[i], pocetno_pohlepno[j])
                #new2 = (pocetno_pohlepno[i+1], pocetno_pohlepno[j+1])
                #new_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[j]] + matrix[pocetno_pohlepno[i+1]][ pocetno_pohlepno[j+1]]

                curr_makespan,_,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                save = pocetno_pohlepno[i+1:j+1]
                pocetno_pohlepno[i+1:j+1] = pocetno_pohlepno[i+1:j+1][::-1]
                new_makespan,_,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                #print("curr: ", curr_travel_time, " new: ", new_travel_time)

                if new_makespan < curr_makespan:
                    TL.append(curr1)
                    TL.append(curr2)

                    dic[TL[-1]] = 2
                    dic[TL[-2]] = 2

                else:
                    pocetno_pohlepno[i+1:j+1] = save

            else:
                pocetno_pohlepno[i+1:j+1] = save
                #print("l se ne mijenja = ", pocetno_pohlepno )
                #print("bridovi ", curr1, curr2, "su trenutno u TABU listi")

    sol = pocetno_pohlepno
    makespan,_,cost = count_time(sol, matrix, full_file_name)
    
    message = ""
    if cost != 0:
        message = "rješenje nije dopustivo, inf"

    else:
        cost = makespan
    
    return sol, makespan, message, cost


def tabu_makespan(csv_file):
    folder, instances, permutation, time,l1, l2, l3 = zad2.pohlepno_makespan(csv_file)
    list2 = []
    txt_name3 = 'dz2_tabu_makespan.txt'
    txt_name4 = 'dz2_tabu_makespan_solutions.txt'

    file_names = []
    solutions = []
    times = []
    messages = []
    costs = []

    for i in range(len(l1)):
        pocetno = l2[i]
        full_file_name = l1[i]
        matrix = l3[i]
        file_name = instances[i]

        sol, makespan, message, cost = korak_tabu_makespan(pocetno, full_file_name, matrix)
        file_names.append(file_name)
        solutions.append(sol)
        times.append(makespan)
        messages.append(message)
        costs.append(cost)

        apsolutno, relativno, yn = odstupanja(makespan, file_name, csv_file)
        print(apsolutno, relativno, yn)
        parser.write1(txt_name3, file_name, apsolutno, relativno, yn)
        parser.write2(txt_name4, file_name, sol, cost)

    return file_names, solutions, times, messages, costs 

#----------------------fix-----------------
def fixed_korak_tabu_makespan(pocetno, full_file_name, matrix):
    pocetno_pohlepno = pocetno
    n = len(pocetno_pohlepno)

    TL = []
    dic = {}
    cost = 0

    full_file_name = full_file_name
    matrix = matrix
    n2 = int(n*0.05)
    for i in range(n):
        print("i= ", i)
        for j in range(i+1,n2):
            #print("j= ", j)
            remove = []
            for k,v in dic.items():
                if v == 0:
                    r = k
                    remove.append(r)
                    TL.remove(k)

            for z in remove:
                dic.pop(z)

            for k,v in dic.items():
                dic[k] = v-1

            #uzmi dva brida s trenutnog puta
            curr1 = (pocetno_pohlepno[i], pocetno_pohlepno[i+1])
            curr2 = (pocetno_pohlepno[j], pocetno_pohlepno[(j+1)%n])
            #curr_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[i+1]] + matrix[pocetno_pohlepno[j]][ pocetno_pohlepno[(j+1)%n]]
            #print()

            if curr1 not in TL and curr2 not in TL:

                #prespajanje, dobijemo dva nova brida i novu udaljenost
                #new1 = (pocetno_pohlepno[i], pocetno_pohlepno[j])
                #new2 = (pocetno_pohlepno[i+1], pocetno_pohlepno[j+1])
                #new_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[j]] + matrix[pocetno_pohlepno[i+1]][ pocetno_pohlepno[j+1]]

                curr_makespan,_,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                save = pocetno_pohlepno[i+1:j+1]
                pocetno_pohlepno[i+1:j+1] = pocetno_pohlepno[i+1:j+1][::-1]
                new_makespan,_,_ = count_time(pocetno_pohlepno, matrix, full_file_name)

                if new_makespan < curr_makespan:
                    TL.append(curr1)
                    TL.append(curr2)

                    dic[TL[-1]] = 2
                    dic[TL[-2]] = 2

                else:
                    pocetno_pohlepno[i+1:j+1] = save

            else:
                pocetno_pohlepno[i+1:j+1] = save
                #print("l se ne mijenja = ", pocetno_pohlepno )
                #print("bridovi ", curr1, curr2, "su trenutno u TABU listi")

    sol = pocetno_pohlepno
    #makespan,_,cost = count_time(sol, matrix, full_file_name)
    cost = parser.calc_traveltime(sol, matrix, full_file_name)
    
    return sol, cost


def fixed_tabu_makespan(csv_file):
    folder, instances, permutation, time,l1, l2, l3 = zad2.pohlepno_makespan(csv_file)
    list2 = []

    file_names = []
    solutions = []
    times = []
    messages = []
    costs = []

    #txt_tabu1 = './DZ2/Tabu/TABU_makespan.txt'
    #txt_tabu2 = './DZ2/Tabu/TABU_makespan_solutions.txt'
    txt_tabu3 = './DZ2/Tabu/TABU_optimal_sol_makespan.txt'
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(len(l1)):
        #list1 = []
        pocetno = l2[i]
        full_file_name = l1[i]
        matrix = l3[i]
        file_name = instances[i]

        sol, makespan, message, _ = fixed_korak_tabu_makespan(pocetno, full_file_name, matrix)
        cost = parser.calc_makespan(sol, matrix, full_file_name)
        file_names.append(file_name)
        solutions.append(sol)
        times.append(makespan)
        messages.append(message)
        costs.append(cost)

        apsolutno, relativno, yn = odstupanja(makespan, file_name, csv_file)
        print(apsolutno, relativno, yn)

        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1
        if cost != float('inf'):
            valid_sol = valid_sol + 1
        print("res: ", full_file_name, permutation, cost)


    print(parser.write_num_optimal(txt_tabu3, num_optimal_sol, valid_sol))

    return file_names, solutions, times, messages, costs 



def fixed_korak_tabu_traveltime(pocetno, full_file_name, matrix):
    pocetno_pohlepno = pocetno
    n = len(pocetno_pohlepno)

    TL = []
    dic = {}
    cost = 0

    full_file_name = full_file_name
    matrix = matrix

    iter = 0
    n2 = int(n*0.2)
    for i in range(n):
        print("i= ", i)
        for j in range(i+1,n2):

            remove = []
            for k,v in dic.items():
                if v == 0:
                    r = k
                    remove.append(r)
                    TL.remove(k)

            for z in remove:
                dic.pop(z)

            for k,v in dic.items():
                dic[k] = v-1


            #uzmi dva brida s trenutnog puta
            curr1 = (pocetno_pohlepno[i], pocetno_pohlepno[i+1])
            curr2 = (pocetno_pohlepno[j], pocetno_pohlepno[(j+1)%n])
            #curr_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[i+1]] + matrix[pocetno_pohlepno[j]][ pocetno_pohlepno[(j+1)%n]]


            if curr1 not in TL and curr2 not in TL:

                #prespajanje, dobijemo dva nova brida i novu udaljenost
                #new1 = (pocetno_pohlepno[i], pocetno_pohlepno[j])
                #new2 = (pocetno_pohlepno[i+1], pocetno_pohlepno[j+1])
                #new_dist = matrix[pocetno_pohlepno[i]][pocetno_pohlepno[j]] + matrix[pocetno_pohlepno[i+1]][ pocetno_pohlepno[j+1]]

                #_,curr_travel_time,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                curr_travel_time = parser.calc_traveltime(pocetno_pohlepno, matrix, full_file_name)
                save = pocetno_pohlepno[i+1:j+1]
                pocetno_pohlepno[i+1:j+1] = pocetno_pohlepno[i+1:j+1][::-1]
                #_,new_travel_time,_ = count_time(pocetno_pohlepno, matrix, full_file_name)
                new_travel_time = parser.calc_traveltime(pocetno_pohlepno, matrix, full_file_name)

                if new_travel_time < curr_travel_time:
                    #print("curr: ", curr_travel_time, " new: ", new_travel_time)
                    #print("swap edges ", curr1, curr2, " with ", new1, new2)
                    TL.append(curr1)
                    TL.append(curr2)
                    #print("append to TL= ", TL)

                    dic[TL[-1]] = 2
                    dic[TL[-2]] = 2

                else:
                    pocetno_pohlepno[i+1:j+1] = save

            else:
                pocetno_pohlepno[i+1:j+1] = save
                #print("l se ne mijenja = ", pocetno_pohlepno )
                #print("bridovi ", curr1, curr2, "su trenutno u TABU listi")


    sol = pocetno_pohlepno
    cost= parser.calc_traveltime(sol, matrix, full_file_name)

    return sol, cost

def fixed_tabu_traveltime(csv_file):
    folder, instances, permutation, time,l1, l2, l3 = zad2.pohlepno_traveltime(csv_file)
    list2 = []
    #txt_name = 'dz2_fixed_tabu_traveltime.txt'
    #txt_name2 = 'dz2_fixed_tabu_traveltime_solutions.txt'

    file_names = []
    solutions = []
    times = []
    messages = []
    costs = []

    #txt_tabu1 = './DZ2/Tabu/TABU_traveltime.txt'
    #txt_tabu2 = './DZ2/Tabu/TABU_traveltime_solutions.txt'
    #txt_tabu3 = './DZ2/Tabu/TABU_optimal_sol_traveltime.txt'
    num_optimal_sol = 0
    valid_sol = 0

    for i in range(2):
        #list1 = []
        pocetno = l2[i]
        full_file_name = l1[i]
        matrix = l3[i]
        file_name = instances[i]

        sol, cost = fixed_korak_tabu_traveltime(pocetno, full_file_name, matrix)

        cost = parser.calc_traveltime(sol, matrix, full_file_name)

        file_names.append(file_name)
        solutions.append(sol)
        costs.append(cost)

        apsolutno, relativno, yn = odstupanja(cost, file_name, csv_file)

        if yn == "DA":
            num_optimal_sol = num_optimal_sol + 1
        if cost != float('inf'):
            valid_sol = valid_sol + 1


    return file_names, solutions, times, messages, costs 


if __name__ == "__main__":
    csv_travel = 'Traveltime_Bounds.csv'
    csv_span = 'Makespan_Bounds.csv'

    #print(tabu_traveltime(csv_travel))
    #print(tabu_makespan(csv_span))

    #--print(fixed_tabu_makespan(csv_span))
    #--print(fixed_tabu_traveltime(csv_travel))

