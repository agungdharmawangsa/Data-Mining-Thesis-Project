from random import randrange
from random import uniform
from hello import mknn_validity

def inisialisasi_populasi(pop_size, batas_K):
    populasi = list()
    for x in range(pop_size):
        populasi.append(randrange(1, batas_K))
    return populasi

def evaluasi_fitness(train_set, test_set, populasi):
    pop_size = len(populasi)
    fitness = list()
    nilai_k = list()
    for i in range(pop_size):
        fitness.append(sum(mknn_validity(test_set, train_set, populasi[i]))/len(train_set))
    for i in range(pop_size):
        temp = list()
        temp.append(populasi[i])
        temp.append(fitness[i])
        nilai_k.append(temp)
    return nilai_k

def seleksi(crossover_rate, nilai_k):
    roulletecopy = [i[:] for i in nilai_k]
    roullete = [i[:] for i in nilai_k]
    hasil_k = list()
    cross_num = int(crossover_rate*len(nilai_k))
    total_fitness = 0
    for i in range(len(roullete)):
        total_fitness = total_fitness+roullete[i][1]
    probabilitas = list()
    for i in range(len(roullete)):
        roullete[i][1] = roullete[i][1]/total_fitness
        probabilitas.append(roullete[i][1])
    for i in range(len(roullete)-1):
        roullete[i+1][1] = roullete[i][1]+probabilitas[i+1]
    for i in range(len(roullete)):
        roullete[i][1] = round(roullete[i][1], 3)
    # setelah mencari probabilitas komulatif, bangkitkan uniform random (0,1) dan seleksi berdasarkan nilai random
    parent = 0
    while parent<cross_num:
        i = 0
        r = uniform(0,1)
        for i in range(len(roullete)):
            if roullete[i][1] <= r and roullete[i+1][1] > r:
                if roullete[i+1][0] != 'null': 
                    hasil_k.append(roulletecopy[i+1][0])
                    parent += 1
                    roullete[i+1][0] = 'null'
                break
            elif roullete[i][1] > r:
                if roullete[i][0] != 'null':
                    hasil_k.append(roulletecopy[i][0])
                    parent += 1
                    roullete[i][0] = 'null'
                break
    return hasil_k

def pengkodean_biner(nilai_k, hasil_k):
    biner_pop = list()
    biner_seleksi = list()
    for i in range(len(nilai_k)):
        temp = list()
        biner = list()
        biner = [f'{nilai_k[i][0]:06b}']
        for item in biner:
            for karakter in item:
                temp.append(int(karakter))
        biner_pop.append(temp)
    for i in range(len(hasil_k)):
        temp = list()
        biner = list()
        biner = [f'{hasil_k[i]:06b}']
        for item in biner:
            for karakter in item:
                temp.append(int(karakter))
            biner_seleksi.append(temp)
    return biner_pop, biner_seleksi

def crossover(hasil_k):
    # mencari pasangannya
    kawin = list()
    if len(hasil_k) % 2 == 0:
        for row in range(int(len(hasil_k)/2)):
            temp = list()
            mating = 0
            while mating<2:
                index = randrange(len(hasil_k))
                if hasil_k[index] != 'null':
                    temp.append(hasil_k[index])
                    hasil_k[index] = 'null'
                    mating+=1
            kawin.append(temp)
    else:
        temp3 = list()
        temp1 = hasil_k.pop(randrange(len(hasil_k)))
        temp2 = hasil_k[randrange(len(hasil_k))]
        temp3.append(temp1)
        temp3.append(temp2)
        kawin.append(temp3)
        for row in range(int(len(hasil_k)/2)):
            temp = list()
            mating = 0
            while mating<2:
                index = randrange(len(hasil_k))
                if hasil_k[index] != 'null':
                    temp.append(hasil_k[index])
                    hasil_k[index] = 'null'
                    mating+=1
            kawin.append(temp) 
    # one cut point crossover
    child = list()
    for i in range(len(kawin)):
        temp3 = list()
        index = randrange(1, len(kawin[i][0])-1)
        for j in range(len(kawin[0])):
            temp1 = list()
            temp2 = list()
            temp1 = kawin[i][j][:index]
            temp2 = kawin[i][j][index:]
            temp3.append(temp1)
            temp3.append(temp2)
        child.append(temp3[2]+temp3[1])
        child.append(temp3[0]+temp3[3])
    return child

def mutasi(mutasi_rate, child_cross, biner_pop):
    # menetukan jumlah yang akan dimutasi
    populasi_total = biner_pop + child_cross
    populasi = [i[:] for i in populasi_total]
    populasi_mut = [i[:] for i in populasi_total]
    mutasi_num = int(mutasi_rate*len(populasi))
    child_mutasi = list()
    index = list()
    mutasi = 0
    while mutasi < mutasi_num:
        random = randrange(len(populasi)*len(populasi[0]))
        temp = 0
        for i in range(len(populasi)):
            for j in range(len(populasi[0])):
                if temp == random and populasi[i][j] != 'null':
                    if populasi_mut[i][j]==0:
                        populasi_mut[i][j] = 1
                    else:
                        populasi_mut[i][j] = 0
                    index.append(i)
                    populasi[i][j] = 'null'
                    mutasi += 1
                temp += 1
    index_mutasi = list(dict.fromkeys(index))
    for i in range(len(index_mutasi)):
        child_mutasi.append(populasi_mut[index_mutasi[i]])
    populasi_total = biner_pop + child_cross + child_mutasi
    # memutasi individu yang semua gennnya 0
    for i in range(len(populasi_total)):
        if sum(populasi_total[i]) == 0:
            random = randrange(len(populasi_total[i]))
            populasi_total[i][random] = 1
    return populasi_total

def pengkodean_K(populasi_total):
    nilai_k = list()
    biner = list()
    # untuk mendapatkan pangkat biner
    for jumlah, item in enumerate(populasi_total[0]):
        biner.append(jumlah)
    biner.reverse()
    for i in range(len(populasi_total)):
        temp = list()
        for j in range(len(populasi_total[0])):
            temp.append(populasi_total[i][j]*2**biner[j])
        nilai_k.append(sum(temp))
    return nilai_k

def elitism (nilai_k, pop_size, nilai_berhenti):
    # sorting fitness
    hasil_k = list()
    true = 0
    while true < len(nilai_k)-1:
        for i in range(len(nilai_k)-1):
            if nilai_k[i][1]<nilai_k[i+1][1]:
                temp = nilai_k[i+1]
                nilai_k[i+1] = nilai_k[i]
                nilai_k[i] = temp
                temp = 0
        true = 0
        for i in range(len(nilai_k)-1):
            if nilai_k[i][1]>nilai_k[i+1][1] or nilai_k[i][1]==nilai_k[i+1][1]:
                true += 1
    for i in range(pop_size):
        hasil_k.append(nilai_k[i])
    if hasil_k[0][1] >= nilai_berhenti:
        fitness_stop = 'true'
    else:
        fitness_stop = 'false'
    return hasil_k, fitness_stop