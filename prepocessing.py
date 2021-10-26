from random import randrange
from operator import itemgetter
from csv import reader

# Load a CSV file
def load_csv(filename):
	dataset = list()
	with open(filename, 'r') as file:
		csv_reader = reader(file)
		for row in csv_reader:
			if not row:
				continue
			dataset.append(row)
	return dataset

# Convert string column to float
def str_column_to_float(dataset, column):
	for row in dataset:
		row[column] = float(row[column].strip())

# Convert string column to integer
def str_column_to_int(dataset, column):
	class_values = [row[column] for row in dataset]
	unique = list(dict.fromkeys(class_values)) # <== MENGHAPUS DUPLIKASI KELAS NAMUN URUTAN SESUAI CSV
	# unique = set(class_values) <== MENGHAPUS DUPLIKASI KELAS NAMUN RANDOM URUTANNYA
	lookup = dict()
	for i, value in enumerate(unique):
		lookup[value] = i
	for row in dataset:
		row[column] = lookup[row[column]]
	return lookup

def random_oversampling(dataset):
	kelas = list()
	jumlah_kelas = list()
	dataset_bagi = list()
	selisih = list()
	# nyari kelasnya apa aja
	for i in range(len(dataset)):
		kelas.append(dataset[i][-1])
	kelas = list(dict.fromkeys(kelas))
	# untuk kumpulin kelas yang sejenis dan mengetahui jumlahnya
	for i in range(len(kelas)):
		jumlah = 0
		temp = list()
		for j in range(len(dataset)):
			if kelas[i] == dataset[j][-1]:
				temp.append(dataset[j])
				jumlah +=1
		dataset_bagi.append(temp)
		jumlah_kelas.append([kelas[i], jumlah])
	# sorting jumlah kelas supaya dapet kelas yang dominan di depan 
	jumlah_kelas = sorted(jumlah_kelas,reverse=True,key=itemgetter(1))
	for x in range(len(jumlah_kelas)-1):
		temp = jumlah_kelas[0][1]-jumlah_kelas[x+1][1]
		jumlah_kelas[x+1].append(temp)
		selisih.append(jumlah_kelas[x+1])
	true = 0
	i = 0
	# dataset bagi nyimpen list setiap kelas
	while true < len(selisih):
		# pass kelas dominan 
		if dataset_bagi[i][0][-1] == jumlah_kelas[0][0]:
			i+=1
		else:
			for x in range(len(selisih)):
				# mencari identitas
				if dataset_bagi[i][0][-1] == selisih[x][0]:
					for row in range(selisih[x][-1]):
						r = randrange(len(dataset_bagi[i]))
						dataset_bagi[i].append(dataset_bagi[i][r])
					i+=1
					true+=1
					break
	dataset = list()
	for i in range(len(dataset_bagi)):
		for j in range(len(dataset_bagi[0])):
			dataset.append(dataset_bagi[i][j])
	return dataset

def dataset_minmax(dataset):
	minmax = list()
	for i in range(len(dataset[0])-1):
		col_values = [row[i] for row in dataset]
		value_min = min(col_values)
		value_max = max(col_values)
		minmax.append([value_min, value_max])
		normalize_dataset(dataset, minmax, i)
	return

def normalize_dataset(dataset, minmax, i):
	for row in dataset:
		row[i] = round((row[i] - minmax[i][0]) / (minmax[i][1] - minmax[i][0]), 2)
	return

def cross_validation_split(dataset, n_folds):
	dataset_split = list()
	dataset_copy = list(dataset)
	index = list()
	fold_size = int(len(dataset) / n_folds)
	for _ in range(n_folds):
		fold = list()
		fold_num = 0
		temp = list()
		while fold_num < fold_size:
			rand_index = randrange(len(dataset_copy))
			if dataset_copy[rand_index] != 'null':
				fold.append(dataset_copy[rand_index])
				dataset_copy[rand_index] = 'null'
				fold_num +=1
				temp.append(rand_index)
		index.append(temp)
		dataset_split.append(fold)
	return dataset_split, index