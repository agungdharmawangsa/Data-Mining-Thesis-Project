hi welcome to my thesis project, here im gonna explain what i did and how to use my code
/////
first of all, my thesis title is Implementation of Genetic Algorithms for Optimization of Modified K-Nearest Neighbor in the Classification of Chronic Kidney Disease. the idea of this, it's hard to define whether someone got a chronic kidney disease or not. The problem is, belong to the data characteristic is similar from the one who might got kidney disease compare to the healthy one. which is why machine learning will help to determine and make a good classification to seperate high risk or postive chronic kidney disease or not. the more faster we know the more life would be saved in future.
////
main classification method of this thesis is Modified K-Nearest Neighbor and K-Nearest Neighbor. Genetic Algorithm to optimize the K parameter in both of those method

that all for the introduction, it's just too long to write them all so if you have any question or want to learn more about my thesis project please feel free to contact me on
email : Dharmaagung56@gmail.com
Whatsapp : 082146062951

main.py
this is the main program, when you try to run my code be sure to run from this file

prepocessing.py
- i use min-max normalization to make the data has the same range from (0-1)
- my data has imbalance dataset, one major class and one minor class, to avoid classification method tend to one class (major class) because major class has more information, i did one more normalization method, Random Oversampling. now i have the balance dataset

genetic_algo.py
optimizing the K parameter in K-Nearest Neighbor or Modified K-Nearest Neighbor

classification.py
this is where i code all classification function and how to evaluate them

Data
secondary data from UCI.edu
https://archive.ics.uci.edu/ml/datasets/chronic_kidney_disease
or you can use data that i already upload
