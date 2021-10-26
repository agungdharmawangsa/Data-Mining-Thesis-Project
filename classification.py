# import numpy as np
from math import sqrt
from random import randrange
from operator import itemgetter
from sklearn.metrics import plot_confusion_matrix
from sklearn.metrics import confusion_matrix
from prepocessing import *

def mknn_validity(test, train, k):
	t_eucsim = t_eucsim_matrix(train)
	t_validity = t_validity_matrix(t_eucsim, k)
	return t_validity

# membuat matrix perhitungan euclidean dan similaritas antar data training
def t_eucsim_matrix(x):
	y = list(x)
	#column[] untuk menyimpan distance dan similaritas
	#column_eucsim[] untuk menyimpan baris dari data train y
	#t_eucsim[] untuk menyimpan baris dari data train x
	column = list()
	column_eucsim = list()
	t_eucsim = list()
	for i in range(len(x)):
		column_eucsim.clear()
		for j in range(len(y)):
			summing_euc=0
			for k in range(len(x[0])-1):
				summing_euc += (x[i][k] - y[j][k])**2
			column.append(sqrt(summing_euc)) # <=== Memasukan distance ke column[]
			if x[i][-1] == y[j][-1]:
				column.append(1) # <=== Memasukan similaritas ke column[] jika kelas train x dan train y sama
			else:
				column.append(0) # <=== Memasukan similaritas ke column[] jika kelas train x dan train y berbeda
			column_eucsim.append(column.copy()) # <=== Memasukan distance dan similaritas ke dalam list untuk merepresentasikan train y
			column.clear()
		t_eucsim.append(column_eucsim.copy()) # <=== Memasukan distance dan similaritas ke dalam list untuk merepresentasikan train x
		# contoh listnya menjadi seperti : [[[distance, similarity_class], [0.1, 1], [0.2, 0]], [0.2, 2], [0.1, 0], [0.3,2]]]
	return t_eucsim

def t_validity_matrix(eucsim, k):
	t_validity = list()
	temp = list()
	temp2 = list()
	shortest = list()
	for i in range(len(eucsim)):
		temp.clear()
		temp2.clear()
		shortest.clear()
		valsum=0
		validity=0
		for j in range(len(eucsim[0])):
			if i == j:
				continue
			temp.append(eucsim[i][j])
		temp2 = sorted(temp, key=itemgetter(0))
		for short in range(k):
			shortest.append(temp2[short].copy())
			valsum += shortest[short][1]
		validity = 1/k*valsum
		t_validity.append(validity)
	return t_validity

def evaluate_algorithm(algo, folds, *args):
	predicted_knn_gui = list()
	predicted_mknn_gui = list()
	accuracy_knn = list()
	precision_knn = list()
	recall_knn = list()
	accuracy_mknn = list()
	precision_mknn = list()
	recall_mknn = list()
	for fold in folds:
		train_set = list(folds)
		train_set.remove(fold)
		train_set = sum(train_set, [])
		test_set = list()
		for row in fold:
			row_copy = list(row)
			test_set.append(row_copy)
			# row_copy[-1] = None
		validity = mknn_validity(test_set, train_set, *args)
		# train_set pada parameter algo hanya memberi 1 trainset setiap perulangan for
		predicted, predicted_mknn = algo(train_set, test_set, validity, *args)
		predicted_knn_gui.append(predicted)
		predicted_mknn_gui.append(predicted_mknn)
		actual = [row[-1] for row in fold]
		# confusion matrix
		# knn
		tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()
		accuracy_knn.append((tp + tn)/(tn + tp + fn + fp))
		precision_knn.append(tp/(tp+fp))
		recall_knn.append(tp/(tp+fn))
		#mknn
		tn, fp, fn, tp = confusion_matrix(actual, predicted_mknn).ravel()
		accuracy_mknn.append((tp + tn)/(tn + tp + fn + fp))
		precision_mknn.append(tp/(tp+fp))
		recall_mknn.append(tp/(tp+fn))
	return accuracy_knn, precision_knn, recall_knn, accuracy_mknn, precision_mknn, recall_mknn,predicted_knn_gui,predicted_mknn_gui

def output(train, test, validity, num_neighbors):
	predictions = list()
	predictions_mknn = list()
	for row in test:
		output, output_mknn = predict_classification(train, row, validity, num_neighbors)
		predictions.append(output)
		predictions_mknn.append(output_mknn)
	return predictions, predictions_mknn

def predict_classification(train, test_row, validity, num_neighbors):
	neighbors, predict_mknn = get_neighbors(train, test_row, validity, num_neighbors)
	output_values = [row[-1] for row in neighbors]
	prediction = max(set(output_values), key=output_values.count)
	return prediction, predict_mknn

def get_neighbors(train, test_row, validity, num_neighbors):
	distances = list()
	distances_num_neighbors = list()
	coor= 0
	for train_row in train:
		dist = euclidean_distance(test_row, train_row)
		distances.append((train_row, dist, coor))
		coor+=1
	distances.sort(key=lambda tup: tup[1])
	neighbors = list()
	for i in range(num_neighbors):
		distances_num_neighbors.append(distances[i])
		neighbors.append(distances[i][0])
	predict_mknn = weight_vote(distances_num_neighbors, validity)
	return neighbors, predict_mknn

def weight_vote(dist, val):
	weight = dict()
	for item in dist:
		if item[0][-1] not in weight.keys():
			weight[item[0][-1]] = val[item[2]]/(item[1] + 0.5)
		else:
			weight[item[0][-1]] += val[item[2]]/(item[1] + 0.5)
	predict_mknn = max(weight.items(), key=itemgetter(1))[0]
	return predict_mknn

def euclidean_distance(row1, row2):
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return (sqrt(distance))