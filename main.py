from random import seed
# from scipy.sparse import data
from hello import *
from genetic_algo import *
#GUI Libraries
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk
a = []
b = []
c = []
d = []
e = 0
seed(12)
filename = 'ckd51.csv'
dataset = load_csv(filename)
for i in range(len(dataset[0])-1):
	str_column_to_float(dataset, i)
# convert class column to integers
str_column_to_int(dataset, len(dataset[0])-1)
# data split, menggunakan K- fold cross validation
# normalization
dataset_minmax(dataset)
# random oversampling
dataset = random_oversampling(dataset)
for i in range(len(dataset)):
	dataset_tampil = [i[:] for i in dataset]
def click(dataset):
	n_folds = int(Entry_n_folds.get())
	folds, index = cross_validation_split(dataset, n_folds)
	global a
	global b
	global c
	global d
	fold1 = list()
	train_set = list(folds)
	fold1.append(train_set.pop(0))
	train_set = sum(train_set, [])
	test_set = list()
	for row in fold1:
		row_copy = list(row)
		test_set.append(row_copy)
		row_copy[-1] = None
	a = folds
	b = train_set
	c = test_set
	d = index
	folds_tampil = list()
	for i in range(len(folds)):
		temp = [j[:] for j in folds[i]]
		folds_tampil.append(temp)
	for i in range(len(folds_tampil)):
		for j in range(len(folds_tampil[0])):
			folds_tampil[i][j].insert(0, j)
	count = 0
	for i in range(len(folds_tampil)):
		for j in range(len(folds_tampil[0])):
			my_tree.insert(parent='',index='end',iid=count,text="",values=(folds_tampil[i][j][0],folds_tampil[i][j][1],folds_tampil[i][j][2],folds_tampil[i][j][3],folds_tampil[i][j][4],folds_tampil[i][j][5],folds_tampil[i][j][6],folds_tampil[i][j][7],folds_tampil[i][j][8],folds_tampil[i][j][9],folds_tampil[i][j][10],folds_tampil[i][j][11],folds_tampil[i][j][12],folds_tampil[i][j][13],folds_tampil[i][j][14],folds_tampil[i][j][15],folds_tampil[i][j][16],folds_tampil[i][j][17],folds_tampil[i][j][18],folds_tampil[i][j][19],folds_tampil[i][j][20],folds_tampil[i][j][21],folds_tampil[i][j][22],folds_tampil[i][j][23],folds_tampil[i][j][24],folds_tampil[i][j][25]))
			count+=1
def click1():
	global b
	global c
	global e
	S_Text_Output.config(state="normal")
	pop_size = int(Entry_pop_size.get())
	crossover_rate = float(Entry_crossover_rate.get())
	mutasi_rate = float(Entry_mutasi_rate.get())
	seed()
	batas_K = round(0.1 * len(b))
	jumlah_iterasi = 15
	nilai_berhenti = 0.92
	generasi = 0
	fitness_stop = 'false'
	pop = inisialisasi_populasi(pop_size, batas_K)
	nilai_k = evaluasi_fitness(b, c, pop)
	while generasi < jumlah_iterasi and fitness_stop == 'false':
		hasil_k = seleksi(crossover_rate, nilai_k)
		pop, hasil_k = pengkodean_biner(nilai_k, hasil_k)
		child_cross = crossover(hasil_k)
		populasi = mutasi(mutasi_rate, child_cross, pop)
		pop = pengkodean_K(populasi)
		nilai_k = evaluasi_fitness(b, c, pop)
		nilai_k, fitness_stop = elitism (nilai_k, pop_size, nilai_berhenti)
		generasi+=1
	e = nilai_k[0][0]
	S_Text_Output.insert(END, str(nilai_k)+'\n')
	S_Text_Output.insert(END, str("nilai K Optimal = ")+str(nilai_k[0][0])+'\n')
	S_Text_Output.insert(END, str("nilai Fitness Optimal = ")+str(nilai_k[0][1])+'\n')
	S_Text_Output.config(state="disabled")
def clear_output():
		S_Text_Output.config(state="normal")
		S_Text_Output.delete(1.0, END)
		S_Text_Output.update()
		S_Text_Output.config(state="disabled")
def click2 (dataset_tampil):
	global a
	global d
	global e
	top = Toplevel()
	top.title("klasifikasi")
	top.configure(background="gray")
	#creating table frame
	tree_frame = Frame(top)
	#treeview scrollbar
	tree_scroll = Scrollbar(tree_frame,orient="vertical")
	tree_scroll1 = Scrollbar(tree_frame,orient="horizontal")
	#creating treeview
	my_tree = ttk.Treeview(tree_frame)
	my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set)
	tree_frame.pack()
	my_tree['columns'] = ("Nomor","Age","Blood Pressure", "Specific Gravity", "Albumin","Sugar","Red Blood Cells","Pus Cells","Pus Cells Pump","Bacteria","Blood Glucose Random","Blood Urea","Serum Creatinine","Sodium","Potassium","Hemoglobin","Packed Cell Volume","White Blood Cell Count","Red Blood Cell Count","Hypertension","Diabetes Mellitus","Coronary Artery Disease","Apetite","Pedal Edema","Anemia","Kelas","predicted_knn","predicted_mknn")
	#configure the scollbar
	tree_scroll.configure(command=my_tree.yview)
	my_tree.configure(yscrollcommand=tree_scroll.set)
	tree_scroll.pack(side=RIGHT, fill=Y)
	tree_scroll1.config(command=my_tree.xview)
	my_tree.configure(xscrollcommand=tree_scroll1.set)
	tree_scroll1.pack(side=BOTTOM,fill=X)
	#formatting table
	my_tree.column("#0",width=0, stretch=NO)
	my_tree.column("Nomor", anchor=CENTER, width=120)
	my_tree.column("Age", anchor=W, width=120)
	my_tree.column("Blood Pressure", anchor=W, width=120)
	my_tree.column("Specific Gravity", anchor=W, width=120)
	my_tree.column("Albumin", anchor=W, width=120)
	my_tree.column("Sugar", anchor=W, width=120)
	my_tree.column("Red Blood Cells", anchor=W, width=120)
	my_tree.column("Pus Cells", anchor=W, width=120)
	my_tree.column("Pus Cells Pump", anchor=W, width=120)
	my_tree.column("Bacteria", anchor=W, width=120)
	my_tree.column("Blood Glucose Random", anchor=W, width=120)
	my_tree.column("Blood Urea", anchor=W, width=120)
	my_tree.column("Serum Creatinine", anchor=W, width=120)
	my_tree.column("Sodium", anchor=W, width=120)
	my_tree.column("Potassium", anchor=W, width=120)
	my_tree.column("Hemoglobin", anchor=W, width=120)
	my_tree.column("Packed Cell Volume", anchor=W, width=120)
	my_tree.column("White Blood Cell Count", anchor=W, width=120)
	my_tree.column("Red Blood Cell Count", anchor=W, width=120)
	my_tree.column("Diabetes Mellitus", anchor=W, width=120)
	my_tree.column("Coronary Artery Disease", anchor=W, width=120)
	my_tree.column("Apetite", anchor=W, width=120)
	my_tree.column("Pedal Edema", anchor=W, width=120)
	my_tree.column("Anemia", anchor=W, width=120)
	my_tree.column("Kelas", anchor=W, width=120)
	my_tree.column("predicted_knn", anchor=W, width=120)
	my_tree.column("predicted_mknn", anchor=W, width=120)
	#heading tabel
	my_tree.heading("#0",text="",anchor=W)
	my_tree.heading("Nomor",text="Nomor",anchor=CENTER)
	my_tree.heading("Age",text="Age",anchor=W)
	my_tree.heading("Blood Pressure", text="Blood Pressure",anchor=W)
	my_tree.heading("Specific Gravity", text="Specific Gravity",anchor=W)
	my_tree.heading("Albumin",text="Albumin",anchor=W)
	my_tree.heading("Sugar",text="Sugar",anchor=W)
	my_tree.heading("Red Blood Cells",text="Red Blood Cells",anchor=W)
	my_tree.heading("Pus Cells",text="Pus Cells",anchor=W)
	my_tree.heading("Pus Cells Pump",text="Pus Cells Pump",anchor=W)
	my_tree.heading("Bacteria",text="Bacteria",anchor=W)
	my_tree.heading("Blood Glucose Random",text="Blood Glucose Random",anchor=W)
	my_tree.heading("Blood Urea",text="Blood Urea",anchor=W)
	my_tree.heading("Serum Creatinine",text="Serum Creatinine",anchor=W)
	my_tree.heading("Sodium",text="Sodium",anchor=W)
	my_tree.heading("Potassium",text="Potassium",anchor=W)
	my_tree.heading("Hemoglobin",text="Hemoglobin",anchor=W)
	my_tree.heading("Packed Cell Volume",text="Packed Cell Volume",anchor=W)
	my_tree.heading("White Blood Cell Count",text="White Blood Cells Count",anchor=W)
	my_tree.heading("Red Blood Cell Count",text="Red Blood Cells Count",anchor=W)
	my_tree.heading("Hypertension",text="Hypertension",anchor=W)
	my_tree.heading("Diabetes Mellitus",text="Diabetes Mellitus",anchor=W)
	my_tree.heading("Coronary Artery Disease",text="Coronary Artery Disease",anchor=W)
	my_tree.heading("Apetite",text="Apetite",anchor=W)
	my_tree.heading("Pedal Edema",text="Pedal Edema",anchor=W)
	my_tree.heading("Anemia",text="Anemia",anchor=W)
	my_tree.heading("Kelas",text="kelas",anchor=W)
	my_tree.heading("predicted_knn",text="KNN",anchor=W)
	my_tree.heading("predicted_mknn",text="MKNN",anchor=W)
	my_tree.pack(padx=30,pady=20)
	#frame
	framew = Frame(top)
	output2_frame = LabelFrame(framew, text="Output hasil klasifikasi", bg="#bbdefb", padx=10, pady=10)
	output2_frame.grid(row=0, column=0, padx=10, pady=10)
	#output box 2
	S_Text_Output2 = ScrolledText(output2_frame, height=15)
	S_Text_Output2.grid(row=0, column=0)
	S_Text_Output2.config(state="normal")
	num_neighbors = e
	accuracy_knn, precision_knn, recall_knn, accuracy_mknn, precision_mknn, recall_mknn,predicted_knn_gui,predicted_mknn_gui = evaluate_algorithm(output, a, num_neighbors)
	n = 1
	count = 0
	for i in range(len(d)):
		for j in range(len(d[0])):
			temp = dataset_tampil[d[i][j]]
			my_tree.insert(parent='',index='end',iid=count,text="",values=(n,temp[0],temp[1],temp[2],temp[3],temp[4],temp[5],temp[6],temp[7],temp[8],temp[9],temp[10],temp[11],temp[12],temp[13],temp[14],temp[15],temp[16],temp[17],temp[18],temp[19],temp[20],temp[21],temp[22],temp[23],temp[24],predicted_knn_gui[i][j],predicted_mknn_gui[i][j]))
			count+=1
			n+=1
	S_Text_Output2.insert(END, str("untuk nilai K = ")+str(num_neighbors)+'\n'+'\n')
	S_Text_Output2.insert(END, str("akurasi knn setiap fold = ")+str(accuracy_knn)+'\n')
	S_Text_Output2.insert(END, str("akurasi knn rata-rata = ")+str(round((sum(accuracy_knn)*100/float(len(accuracy_knn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str("presisi knn setiap fold = ")+str(precision_knn)+'\n')
	S_Text_Output2.insert(END, str("presisi knn rata-rata = ")+str(round((sum(precision_knn)*100/float(len(precision_knn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str("recall knn setiap fold = ")+str(recall_knn)+'\n')
	S_Text_Output2.insert(END, str("recall knn rata-rata = ")+str(round((sum(recall_knn)*100/float(len(recall_knn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str('\n'))
	S_Text_Output2.insert(END, str("akurasi mknn setiap fold = ")+str(accuracy_mknn)+'\n')
	S_Text_Output2.insert(END, str("akurasi mknn rata-rata = ")+str(round((sum(accuracy_mknn)*100/float(len(accuracy_mknn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str("presisi mknn setiap fold = ")+str(precision_knn)+'\n')
	S_Text_Output2.insert(END, str("presisi mknn rata-rata = ")+str(round((sum(precision_mknn)*100/float(len(precision_mknn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str("recall mknn setiap fold = ")+str(recall_mknn)+'\n')
	S_Text_Output2.insert(END, str("recall mknn rata-rata = ")+str(round((sum(recall_mknn)*100/float(len(recall_mknn))),2))+str("%")+'\n')
	S_Text_Output2.insert(END, str('\n'))
	S_Text_Output2.configure(state = "disabled")
	framew.pack(pady=20)
def clear_table():
	for item in my_tree.get_children():
		my_tree.delete(item)
def about():
	about = Toplevel()
	about.title("cara penggunaan program")
	text = Text(about, height=10, width=50)
	text.config(state="normal")
	text.insert(END, str("step by step penggunaan program")+'\n')
	text.insert(END, str("1. masukkan nilai fold terlebih dahulu, contoh = 2,5,10")+'\n')
	text.insert(END, str("2. klik simpan untuk menyimpan fold atau pembagian data training dan testingnya")+'\n')
	text.insert(END, str("3. masukkan size populasi, contoh = 8,9,10")+'\n')
	text.insert(END, str("4. masukkan crossover rate, contoh = 0.8, 0.2")+'\n')
	text.insert(END, str("5. masukkan mutasi rate , contoh = 0.3, 0.5")+'\n')
	text.insert(END, str("6. masukkan size populasi, contoh = 8,9,10")+'\n')
	text.insert(END, str("7. klik optimasi")+'\n')
	text.insert(END, str("8. tunggu kemudian klik klasifikasi"))
	text.pack(padx=30,pady=20)
window = Tk()
window.title("Klasifikasi ginjal")
window.configure(background="gray")
#creating table frame
tree_frame = Frame(window)
#treeview scrollbar
tree_scroll = Scrollbar(tree_frame,orient="vertical")
tree_scroll1 = Scrollbar(tree_frame,orient="horizontal")
#creating treeview
my_tree = ttk.Treeview(tree_frame)
tree_frame.pack(padx=20, pady=20)
my_tree['columns'] = ("Nomor","Age","Blood Pressure", "Specific Gravity", "Albumin","Sugar","Red Blood Cells","Pus Cells","Pus Cells Pump","Bacteria","Blood Glucose Random","Blood Urea","Serum Creatinine","Sodium","Potassium","Hemoglobin","Packed Cell Volume","White Blood Cell Count","Red Blood Cell Count","Hypertension","Diabetes Mellitus","Coronary Artery Disease","Apetite","Pedal Edema","Anemia","Kelas")
#configure the scollbar
tree_scroll.configure(command=my_tree.yview)
my_tree.configure(yscrollcommand=tree_scroll.set)
tree_scroll.pack(side=RIGHT, fill=Y)
tree_scroll1.config(command=my_tree.xview)
my_tree.configure(xscrollcommand=tree_scroll1.set)
tree_scroll1.pack(side=BOTTOM,fill=X)
#formatting table
my_tree.column("#0",width=0, stretch=NO)
my_tree.column("Nomor", anchor=CENTER, width=120)
my_tree.column("Age", anchor=W, width=120)
my_tree.column("Blood Pressure", anchor=W, width=120)
my_tree.column("Specific Gravity", anchor=W, width=120)
my_tree.column("Albumin", anchor=W, width=120)
my_tree.column("Sugar", anchor=W, width=120)
my_tree.column("Red Blood Cells", anchor=W, width=120)
my_tree.column("Pus Cells", anchor=W, width=120)
my_tree.column("Pus Cells Pump", anchor=W, width=120)
my_tree.column("Bacteria", anchor=W, width=120)
my_tree.column("Blood Glucose Random", anchor=W, width=120)
my_tree.column("Blood Urea", anchor=W, width=120)
my_tree.column("Serum Creatinine", anchor=W, width=120)
my_tree.column("Sodium", anchor=W, width=120)
my_tree.column("Potassium", anchor=W, width=120)
my_tree.column("Hemoglobin", anchor=W, width=120)
my_tree.column("Packed Cell Volume", anchor=W, width=120)
my_tree.column("White Blood Cell Count", anchor=W, width=120)
my_tree.column("Red Blood Cell Count", anchor=W, width=120)
my_tree.column("Diabetes Mellitus", anchor=W, width=120)
my_tree.column("Coronary Artery Disease", anchor=W, width=120)
my_tree.column("Apetite", anchor=W, width=120)
my_tree.column("Pedal Edema", anchor=W, width=120)
my_tree.column("Anemia", anchor=W, width=120)
my_tree.column("Kelas", anchor=W, width=120)
#heading tabel
my_tree.heading("#0",text="",anchor=W)
my_tree.heading("Nomor",text="Nomor",anchor=CENTER)
my_tree.heading("Age",text="Age",anchor=W)
my_tree.heading("Blood Pressure", text="Blood Pressure",anchor=W)
my_tree.heading("Specific Gravity", text="Specific Gravity",anchor=W)
my_tree.heading("Albumin",text="Albumin",anchor=W)
my_tree.heading("Sugar",text="Sugar",anchor=W)
my_tree.heading("Red Blood Cells",text="Red Blood Cells",anchor=W)
my_tree.heading("Pus Cells",text="Pus Cells",anchor=W)
my_tree.heading("Pus Cells Pump",text="Pus Cells Pump",anchor=W)
my_tree.heading("Bacteria",text="Bacteria",anchor=W)
my_tree.heading("Blood Glucose Random",text="Blood Glucose Random",anchor=W)
my_tree.heading("Blood Urea",text="Blood Urea",anchor=W)
my_tree.heading("Serum Creatinine",text="Serum Creatinine",anchor=W)
my_tree.heading("Sodium",text="Sodium",anchor=W)
my_tree.heading("Potassium",text="Potassium",anchor=W)
my_tree.heading("Hemoglobin",text="Hemoglobin",anchor=W)
my_tree.heading("Packed Cell Volume",text="Packed Cell Volume",anchor=W)
my_tree.heading("White Blood Cell Count",text="White Blood Cells Count",anchor=W)
my_tree.heading("Red Blood Cell Count",text="Red Blood Cells Count",anchor=W)
my_tree.heading("Hypertension",text="Hypertension",anchor=W)
my_tree.heading("Diabetes Mellitus",text="Diabetes Mellitus",anchor=W)
my_tree.heading("Coronary Artery Disease",text="Coronary Artery Disease",anchor=W)
my_tree.heading("Apetite",text="Apetite",anchor=W)
my_tree.heading("Pedal Edema",text="Pedal Edema",anchor=W)
my_tree.heading("Anemia",text="Anemia",anchor=W)
my_tree.heading("Kelas",text="kelas",anchor=W)
#frame
framew = Frame(window)
frame = LabelFrame(framew, text="input", bg="#bbdefb", padx=20, pady=20)
frame1 = LabelFrame(framew, text="Pengujian Optimasi", bg="#bbdefb", padx=20, pady=20)
frame.grid(row=0, column=0, padx=20, pady=20)
frame1.grid(row=0, column=1, padx=20, pady=20)
#Pembuatan Label
Label (frame, text="Masukkan Nilai Fold", bg="#bbdefb", fg="black", font="none 12 bold").grid(row=0, column=0)
Label (frame1, text="Masukkan size populasi", bg="#bbdefb", fg="black", font="none 12 bold").grid(row=0, column=0)
Label (frame1, text="Masukkan crossover rate", bg="#bbdefb", fg="black", font="none 12 bold").grid(row=2, column=0)
Label (frame1, text="Masukkan mutasi rate", bg="#bbdefb", fg="black", font="none 12 bold").grid(row=4, column=0)
#field box
Entry_n_folds = Entry(frame, width=20, bg="#64b5f6", fg="black", font="none 12 bold")
Entry_pop_size = Entry(frame1, width=20, bg="#64b5f6", fg="black", font="none 12 bold")
Entry_crossover_rate = Entry(frame1, width=20, bg="#64b5f6", fg="black", font="none 12 bold")
Entry_mutasi_rate = Entry(frame1, width=20, bg="#64b5f6", fg="black", font="none 12 bold")
Entry_n_folds.grid(row=1, column=0)
Entry_pop_size.grid(row=1, column=0)
Entry_crossover_rate.grid(row=3, column=0)
Entry_mutasi_rate.grid(row=5, column=0)
#submit button
Button_Click1 = Button(frame, text="Simpan", width=15, bg="#1565c0", fg="white", command=lambda: click(dataset))
Button_Click2 = Button(frame, text="clear_table", width=15, bg="#1565c0", fg="white", command=clear_table)
Button_Click3 = Button(frame1, text="Optimasi", width=15, bg="#1565c0", fg="white", command=click1)
Button_Click4 = Button(frame1, text="klasifikasi", width=15, bg="#1565c0", fg="white", command=lambda: click2(dataset_tampil))
about_click = Button(frame, text="about", width=15, bg="#1565c0", fg="white", command=about)
Button_Click1.grid(row=2, column=0)
Button_Click2.grid(row=3, column=0)
Button_Click3.grid(row=6, column=0)
Button_Click4.grid(row=7, column=0)
about_click.grid(row=4, column=0)
output_frame = LabelFrame(framew, text="Output", bg="#bbdefb", padx=20, pady=20)
output_frame.grid(row=0, column=2, padx=20, pady=20)
Button_Click5 = Button(output_frame, text="clear_output", width=15, bg="#1565c0", fg="white", command=clear_output)
Button_Click5.grid(row=1, column=0, padx=20, pady=10)
#output box 2
S_Text_Output = ScrolledText(output_frame, width=60, height=10)
S_Text_Output.grid(row=0, column=0)
S_Text_Output.config(state="normal")
S_Text_Output.config(state="disabled")
#pack
my_tree.pack(padx=30,pady=20)
framew.pack(padx=50,pady=20)
#run tkinter GUI
window.mainloop()