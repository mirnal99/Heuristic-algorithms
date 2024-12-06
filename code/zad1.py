import numpy as np

def calc_traveltime(l,matrix, file_name): #koristeno/popravljano za 3.dz
    num_nodes, _, windows = read_txt(file_name)
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
        #---print("not ok")

    for p in l[1:]:
        time = time + matrix[a][p]
        traveltime = traveltime + matrix[a][p]
        if time >= windows[p][0] and time <= windows[p][1]:
            b = True
            a = p
        elif time < windows[p][0]:
            wait_time = windows[p][0] - time
            #print("wait_time: ", wait_time)
            time = time + wait_time
            #print("time after waiting: ", time)
            b = True
            a = p
            #print("novi a: ", a)
        elif time > windows[p][1]:
            b = False
            #---print("nije dopustivo")
            counter = counter + 1
            a=p

    last_elem = l[-1]
    depot = 0
    traveltime = traveltime + matrix[last_elem][depot]

    traveltime = round(traveltime, 2)
    #---print("traveltime = ", traveltime)

    cost = traveltime
    if counter != 0:
        #---print("rjesnje nije dopustivo")
        cost = float('inf')

    return cost


def calc_makespan(l,matrix, file_name): #koristeno u 3.dz
    num_nodes, _, windows = read_txt(file_name)
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
            #print(time, " window: ", windows[p][0], windows[p][1])
            b = True
            a = p
        elif time < windows[p][0]:
            wait_time = windows[p][0] - time
            #print("wait_time: ", wait_time)
            time = time + wait_time
            #print("time after waiting: ", time)
            b = True
            a = p
            #print("novi a: ", a)
        elif time > windows[p][1]:
            b = False
            #---print("nije dopustivo")
            counter = counter + 1
            #return -1
            a=p

    last_elem = l[-1]
    depot = 0
    time = time + matrix[last_elem][depot]

    time = round(time, 2) #zaokruzi na 2 decimale kao sto je u best known solutions
    makespan = time

    cost = makespan
    if counter != 0:
        cost = float('inf')

    return cost

def write1(txt_name, file_name, aps_odstupanje, rel_odstupanje, yn): #koristeno u 3.dz
    file = open(txt_name, "a")
    #file.write("naziv instance  relativno odstupanje    apsolutno odstupanje    DA/NE")
    file.write(file_name)
    file.write("    ")
    file.write(str(aps_odstupanje))
    file.write("    ")
    file.write(str(rel_odstupanje))
    file.write("    ")
    file.write(str(yn))
    file.write("\n"+"\n")
    file.close

def write2(txt_name, file_name, sol, time): #koristeno u 3.dz
    file = open(txt_name, "a")
    file.write("instanca: ")
    file.write(file_name)
    file.write("\n"+"rjesenje: ")
    file.write(str(sol))
    file.write("\n"+"time: ")
    file.write(str(time))
    file.write("\n"+"\n")
    file.close

def write_num_optimal(txt_name, num_optimal, num_valid):
    file = open(txt_name, "a")
    file.write("Number of optimal solutions: ")
    file.write(str(num_optimal))
    file.write("\n"+"Number of valid solutions: ")
    file.write(str(num_valid))
    file.close

#--------------------------------------------------------------

"""implementirati parser kojim ce se moci u program ucitavati
    instance problema koje ce se zatim rjesavati odredenim pristupom"""
def read_txt(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        list=[]
        for line in lines:
            list.append(line.rstrip('\n'))

        num_nodes = int(list[0])

        matrix1 = []
        for l in list[1:num_nodes+1]:
            matrix1.append(l)

        matrix2 = []
        for m in matrix1:
            temp = m.split(" ")

            for i in temp:
                a = float(i)
                a = round(a,2) 
                #print(a)
                matrix2.append(a)

        temp_mat = np.array(matrix2)
        matrix = temp_mat.reshape((num_nodes,num_nodes))

        list3 =[]
        for l2 in list[num_nodes+1:]:
            k = l2.split(" ")
            #print("k: ", k)
            for j in k:
                if j != ' ':
                    list3.append(j)
                    #print("j ", j)

        
        list4 =[]
        for i in list3:
            if i != '':
                #print(i)
                a = int(i)
                list4.append(a)


        windows = [i for i in zip(*[iter(list4)]*2)]

        return num_nodes, matrix, windows

    
"""implementirati parser kojim ce se moci ucitati najbolja
    poznata rjesenja za sve instance za oba kriterija"""
import csv
def read_best_solutions(csv_name):
    folder = []
    instances = []
    best_cost = []
    with open(csv_name) as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            folder.append(row[0])
            instances.append(row[1])
            best_cost.append(row[2])

    del folder[0]
    del instances[0]
    del best_cost[0]

    return folder, instances, best_cost


   
"""implementirati metodu kojom ce se provjeravati je li rjesenje dopustivo"""
import random
def dopustivost(file_name): 
    num_nodes, matrix, windows = read_txt(file_name)
    l = []
    for i in range(1,num_nodes):
        l.append(i)

    random.shuffle(l)

    time = 0
    traveltime = 0
    counter = 0
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
            a = p
            counter = counter + 1

    last_elem = l[-1]
    depot = 0
    time = time + matrix[last_elem][depot]
    traveltime = traveltime + matrix[last_elem][depot]

    time = round(time, 2) #zaokruzi na 2 decimale kao sto je u best known solutions
    traveltime = round(traveltime, 2)

    cost = 0
    if counter != 0:
        #print("rjesnje nije dopustivo")
        cost = float('inf')

    """
    if time <= windows[depot][1]:
        #--print("rješenje je dopustivo s makespan vremenom završetka u {}".format(time))
        #--print("rješenje je dopustivo s traveltime vremenom završetka u {}".format(traveltime))
        print(" ")
    else:
        print(" ")
        #--print("rješenje NIJE dopustivo")
    """

    return l, time, traveltime, cost


"""implementirati metodu kojom ce se usporediti je li proslijedeno
    rjesenje jednako najboljem poznatom"""
def compare_makespan(file_name, best_known_csv_file):
    l, my_cost, _,_ = dopustivost(file_name)

    folder, instances, best_cost= read_best_solutions(best_known_csv_file)
    k=-1
    for i in instances:
        k=k+1
        if i == file_name:

            najbolje_rj = best_cost[k]
            print("najbolje makespan rjesenje: ", najbolje_rj)

    if my_cost == najbolje_rj:
        return "DA"
    else:
        return "NE"
    
    
def compare_traveltime(file_name, best_known_file):
    l, _, my_cost,_ = dopustivost(file_name)
    folder, instances, best_cost= read_best_solutions(best_known_file)

    k=-1
    for i in instances:
        k=k+1

        if i == file_name:
            najbolje_rj = best_cost[k]

    if my_cost == najbolje_rj:
        return "DA"
    else:
        return "NE"
    
def odstupanja(time, file_name, csv_file): #FIXED function above(dz2)
    folder, instances, best_cost= read_best_solutions(csv_file)

    k=-1
    for i in instances:
        k=k+1
        if i == file_name:
            najbolje_rj = best_cost[k]
            najbolje_rj = float(najbolje_rj)
    
    temp1 = najbolje_rj-time
    apsolutno = abs(temp1)
    relativno = apsolutno/(abs(najbolje_rj))

    yn = "NE"
    if time == najbolje_rj:
        yn = "DA"
    else:
        yn = "NE"

    return apsolutno, relativno, yn


def odstupanja(full_file_name, file_name, best_known_cvs_file):
    l, _, rjesenje,_ = dopustivost(full_file_name)
    folder, instances, best_cost= read_best_solutions(best_known_cvs_file)

    k=-1
    for i in instances:
        k=k+1
        if i == file_name:
            najbolje_rj = best_cost[k]
            najbolje_rj = float(najbolje_rj)
    
    temp1 = najbolje_rj-rjesenje
    apsolutno = abs(temp1)
    #print("apsolutno: ", apsolutno)
    relativno = apsolutno/(abs(najbolje_rj))
    #print("relativno: ", relativno)

    yn = "NE"
    if rjesenje == najbolje_rj:
        yn = "DA"
    else:
        yn = "NE"

    return apsolutno, relativno, yn

def add_prefix(folder_name):
    
    if folder_name == 'AFG':
        prefix = 'AFG/'
    elif folder_name == 'Dumas':
        prefix = 'Dumas/'
    elif folder_name == 'GendreauDumas':
        prefix = 'GendreauDumasExtended/'
    elif folder_name == 'Langevin':
        prefix = 'Langevin/'
    elif folder_name == 'OhlmannThomas':
        prefix = 'OhlmannThomas/'
    elif folder_name == 'SolomonPesant':
        prefix = 'SolomonPesant/'
    elif folder_name == 'SolomonPotvinBengio':
        prefix = 'SolomonPotvinBengio/'
    else:
        print("error")

    return prefix

def writing(txt_name, best_known_csv_traveltime, best_known_csv_makespan):
    folder, instances, best_cost= read_best_solutions(best_known_csv_makespan)
    folder, instances, best_cost= read_best_solutions(best_known_csv_traveltime)

    for i in range(len(instances)):
        #print(i)
        folder_name = folder[i]
        prefix = add_prefix(folder_name)
        name = prefix+instances[i]
        l, rj_makespan, rj_traveltime,_ = dopustivost(name)
        #print(name)
        write_file(txt_name, name, l, rj_traveltime, rj_makespan)


def writing_traveltime(txt_name, best_known_traveltime):
    folder, instances, best_cost = read_best_solutions(best_known_traveltime)

    for i in range(len(instances)):
        folder_name = folder[i]
        prefix = add_prefix(folder_name)
        name = prefix+instances[i]
        #print("name", name)
        apsolutno, relativno, yn = odstupanja(name, instances[i], best_known_traveltime)
        write_file_traveltime(txt_name, name, apsolutno, relativno, yn)

def writing_makespan(txt_name, best_known_traveltime):
    folder, instances, best_cost = read_best_solutions(best_known_traveltime)

    for i in range(len(instances)):
        folder_name = folder[i]
        prefix = add_prefix(folder_name)
        name = prefix+instances[i]
        #print("name", name)
        apsolutno, relativno, yn = odstupanja(name, instances[i], best_known_traveltime)
        write_file_makespan(txt_name, name, apsolutno, relativno, yn)

def write_file(txt_name, instance, permutation, traveltime, makespan):
    file = open(txt_name, "a")
    file.write("instanca: ")
    file.write(instance)
    file.write("\n"+"rjesenje: ")
    file.write(str(permutation))
    file.write("\n"+"travel time: ")
    file.write(str(traveltime))
    file.write("\n"+ "makespan: ")
    file.write(str(makespan))
    file.write("\n"+"\n")
    file.close

def write_file_traveltime(txt_name, instance, aps_odstupanje, rel_odstupanje, yn):
    file = open(txt_name, "a")
    file.write("instanca: ")
    file.write(instance)
    file.write("\n"+"apsolutno odstupanje: ")
    file.write(str(aps_odstupanje))
    file.write("\n"+"relativno odstupanje: ")
    file.write(str(rel_odstupanje))
    file.write("\n"+ "najbolje poznato rjesenje? ")
    file.write(str(yn))
    file.write("\n"+"\n")
    file.close

def write_file_makespan(txt_name, instance, aps_odstupanje, rel_odstupanje, yn):
    file = open(txt_name, "a")
    file.write("instanca: ")
    file.write(instance)
    file.write("\n"+"apsolutno odstupanje: ")
    file.write(str(aps_odstupanje))
    file.write("\n"+"relativno odstupanje: ")
    file.write(str(rel_odstupanje))
    file.write("\n"+ "najbolje poznato rjesenje? ")
    file.write(str(yn))
    file.write("\n"+"\n")
    file.close

if __name__ == "__main__":
    
    csv_traveltime = 'Traveltime_Bounds.csv'
    csv_makespan = 'Makespan_Bounds.csv'
    
    #----uncomment for writing in results.txt
    #print(writing("results.txt", csv_traveltime, csv_makespan))

    #----uncomment for writing in traveltime_results.txt
    #print(writing_traveltime("traveltime_results.txt", csv_traveltime))

    #----uncomment for writing in makespan_results.txt
    #print(writing_makespan("makespan_results.txt", csv_makespan))




    #ignore - used for writing results into files-----------------------------------------------------
    """
    file_name1 = 'rc_201.1.txt'
    file_name2 = 'rc_206.1.txt'
    file_name3 = 'rc_205.2.txt'
    file_name4 = 'rc_207.4.txt'
    file_name5 = 'rc_202.2.txt'
    file_name6 = 'rc_201.2.txt'
    #print(read_txt(file_name))
    num_nodes, matrix, windows = read_txt(file_name1)
    #print("num_nodes: ", num_nodes)
    #print("matrix: ", matrix)
    #print("windows: ", windows)
    """
    """
    best_time_afg = 'AFG-best-known-traveltime.txt'
    best_span_afg = 'AFG-best-known-makespan.txt'

    best_time_dumas= 'Dumas-best-known-traveltime.txt'
    best_span_dumas = 'Dumas-best-known-makespan.txt'

    best_time_gendreau = 'GendreauDumasExtended-best-known-traveltime.txt'
    best_span_gendreau = 'GendreauDumasExtended-best-known-makespan.txt'

    best_time_langevin = 'Langevin-best-known-traveltime.txt'
    best_span_langevin = 'Langevin-best-known-makespan.txt'

    best_time_thomas = 'OhlmannThomas-best-known-traveltime.txt'
    best_span_thomas = 'OhlmannThomas-best-known-makespan.txt'

    best_time_pesant= 'SolomonPesant-best-known-traveltime.txt'
    best_span_pesant = 'SolomonPesant-best-known-makespan.txt'

    best_time_potvin = 'SolomonPotvinBengio-best-known-traveltime.txt'
    best_span_potvin = 'SolomonPotvinBengio-best-known-makespan.txt'

    #folder, instances, best_cost= read_best_solutions(best_span_potvin)
    """
    """
    print(writing("results.txt", best_time_afg,best_span_afg,'AFG/'))
    print(writing("results.txt", best_time_dumas,best_span_dumas,'Dumas/'))
    print(writing("results.txt", best_time_gendreau,best_span_gendreau,'GendreauDumasExtended/'))
    print(writing("results.txt", best_time_langevin,best_span_langevin,'Langevin/'))
    print(writing("results.txt", best_time_thomas,best_span_thomas,'OhlmannThomas/'))
    print(writing("results.txt", best_time_pesant,best_span_pesant,'SolomonPesant/'))
    print(writing("results.txt", best_time_potvin,best_span_potvin,'SolomonPotvinBengio/'))
    """
    
    """
    print(writing_traveltime("traveltime_results.txt", best_time_afg,'AFG/'))
    print(writing_traveltime("traveltime_results.txt", best_time_dumas,'Dumas/'))
    print(writing_traveltime("traveltime_results.txt", best_time_gendreau,'GendreauDumasExtended/'))
    print(writing_traveltime("traveltime_results.txt", best_time_langevin,'Langevin/'))
    print(writing_traveltime("traveltime_results.txt", best_time_thomas,'OhlmannThomas/'))
    print(writing_traveltime("traveltime_results.txt", best_time_pesant,'SolomonPesant/'))
    print(writing_traveltime("traveltime_results.txt", best_time_potvin,'SolomonPotvinBengio/'))
    """
    
    """
    print(writing_makespan("makespan_results.txt", best_span_afg,'AFG/'))
    print(writing_makespan("makespan_results.txt", best_span_dumas,'Dumas/'))
    print(writing_makespan("makespan_results.txt", best_span_gendreau,'GendreauDumasExtended/'))
    print(writing_makespan("makespan_results.txt", best_span_langevin,'Langevin/'))
    print(writing_makespan("makespan_results.txt", best_span_thomas,'OhlmannThomas/'))
    print(writing_makespan("makespan_results.txt", best_span_pesant,'SolomonPesant/'))
    print(writing_makespan("makespan_results.txt", best_span_potvin,'SolomonPotvinBengio/'))
    """
    #print(compare_makespan(file_name4,'Makespan_Bounds.csv'))
    #print(compare_traveltime(file_name4,'Traveltime_Bounds.csv'))
    