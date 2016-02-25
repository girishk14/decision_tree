CSCE 633 : Machine Learning (Spring 2016)
Project 1 : Decision Tree Induction


Author : Girish Kasiviswanathan (UIN : 425000392)


Installation
------------
This code has been written using Python 2.7 on Ubuntu, using VI Editor. It has bene tested on Windows, as well as on the Linux box at compute.cs.tamu.edu

The Windows version used can be found at https://www.python.org/downloads/release/python-2710/. Please ensure that C:\Python27 is added to the environment variable named 'Path', so that the Python 2.7 interpreter can be invoked at command prompt.

Python 2.7 comes preinstalled on most Linux distributions. 


Files and Directories Included
------------------------------
1. data : Contains all the datasets and their control files
2. Tree_Images : Contains images of the already generated trees for Iris, Car, Mushroom, Pima Indians, Phising and Breast Cancer datasets. These are the same trees as those referred to in the Results document.

PS: Due to CSNET space restrictions, only one pair of trees are shown for some of the datasets.

For the complete set of images for all the datasets, refer to:
https://github.com/girishk14/decision_tree.git



3. TreeViz : Contains images for the trees generated in the current run
4. classification.py, pruning.py, driver.py, decision_tree.py and preprocess.py  : Core Python modules for decision tree
5. Decision_Tree_Report.pdf : Design documentation
6. Decision_Tree_results.pdf : Results for sample runs 


Control Files
-------------

The control files for the 6 specified datasets have already been generated. You may need to make a new control file for testing on new datasets. JSON format is used so that we can define additional parsing parameters in future. 


This is the sample control file for the Iris Dataset: 

NOTE: ALL THE FOLLOWING ARE MANDATORY METADATA INFORMATION REQUIRED

{
 "attr_types": [   //The sequence of attributes is assumed to be same as that in the raw input
  "c", 
  "c", 
  "c", 
  "c"
 ], 
 "class_name": "Class",  //Holds the position of the class column in the raw data
 "class_position": 4, 
 "location": [
  "data/Iris/iris.data" //Location of the data. We can specify multiple locations by using a comma separator.
 ], 
 "attr_names": [
  "Sepal Length", 
  "Sepal Width", 
  "Petal Length", 
  "Petal Width"
 ], 
}



Running the Decision Tree:
---------------------------
To execute the decision tree on some program, use the following command : 

python driver.py control_file_path

For example, for the selected datasets,
python driver.py data/Iris/control.json
python driver.py data/BreastCancer/control.json
python driver.py data/Mushroom/control.json
python driver.py data/Pima/control.json
python driver.py data/Phising/control.json
python driver.py data/Car/control.json

This executes the classic holdout method, i.e trains on 70% of the data, and reports accuracy on the remaining 30%


Switches
---------
1. 10 fold cross validation:  To enable 10-fold cross validation, add the switch --kfold 
eg.  python driver.py data/Iris/control.json --kfold

2. Visualization : For building an image of the generated trees, use the switch --viz. It writes to the folder ./TreeViz/

However, for doing this, the pydot library must be installed. If not, the program throws an error. 
To install pydot library, use the following command:
sudo apt-get install python-pydot

eg. python driver.py data/BreastCancer/control.json --kfold --viz
eg. python driver.py data/Mushroom/control.json ---viz


For classic holdout, it writes only a single tree named 'OriginalTree.png'.  For 10 fold validation, it prints a total of 20 trees, i.e unpruned and pruned tree for each fold.


Output
-------
The program writes the trees, and finally report the accuracies


Sample Output
-------------
Fold : 9
Decision Tree generated
Petal Length < 2.45---> Iris-setosa : 32, 
Petal Length > 2.45---> Iris-virginica : 27, Iris-versicolor : 31, 
   Petal Width < 1.7---> Iris-virginica : 3, Iris-versicolor : 30, 
      Sepal Length < 5.95---> Iris-versicolor : 16, 
      Sepal Length > 5.95---> Iris-virginica : 3, Iris-versicolor : 14, 
         Sepal Width < 2.85---> Iris-virginica : 3, Iris-versicolor : 7, 
         Sepal Width > 2.85---> Iris-versicolor : 7, 
   Petal Width > 1.7---> Iris-virginica : 24, Iris-versicolor : 1, 
      Sepal Length < 5.95---> Iris-virginica : 3, Iris-versicolor : 1, 
         Sepal Width < 3.0---> Iris-virginica : 3, 
         Sepal Width > 3.0---> Iris-versicolor : 1, 
      Sepal Length > 5.95---> Iris-virginica : 21, 
Now pruning . . .
Petal Length < 2.45---> Iris-setosa : 32, 
Petal Length > 2.45---> Iris-virginica : 27, Iris-versicolor : 31, 
   Petal Width < 1.7---> Iris-virginica : 3, Iris-versicolor : 30, 
      Sepal Length < 5.95---> Iris-versicolor : 16, 
      Sepal Length > 5.95---> Iris-virginica : 3, Iris-versicolor : 14, 
         Sepal Width < 2.85---> Iris-virginica : 3, Iris-versicolor : 7, 
         Sepal Width > 2.85---> Iris-versicolor : 7, 
   Petal Width > 1.7---> Iris-virginica : 24, Iris-versicolor : 1, 
Pruned. Now testing on pruned tree. . .


Fold : 10
Decision Tree generated
Petal Length < 2.45---> Iris-setosa : 32, 
Petal Length > 2.45---> Iris-virginica : 27, Iris-versicolor : 31, 
   Petal Width < 1.7---> Iris-virginica : 3, Iris-versicolor : 30, 
      Sepal Length < 5.95---> Iris-versicolor : 16, 
      Sepal Length > 5.95---> Iris-virginica : 3, Iris-versicolor : 14, 
         Sepal Width < 2.85---> Iris-virginica : 3, Iris-versicolor : 7, 
         Sepal Width > 2.85---> Iris-versicolor : 7, 
   Petal Width > 1.7---> Iris-virginica : 24, Iris-versicolor : 1, 
      Sepal Length < 5.95---> Iris-virginica : 3, Iris-versicolor : 1, 
         Sepal Width < 3.0---> Iris-virginica : 3, 
         Sepal Width > 3.0---> Iris-versicolor : 1, 
      Sepal Length > 5.95---> Iris-virginica : 21, 
Now pruning . . .
Petal Length < 2.45---> Iris-setosa : 32, 
Petal Length > 2.45---> Iris-virginica : 27, Iris-versicolor : 31, 
   Petal Width < 1.7---> Iris-virginica : 3, Iris-versicolor : 30, 
      Sepal Length < 5.95---> Iris-versicolor : 16, 
      Sepal Length > 5.95---> Iris-virginica : 3, Iris-versicolor : 14, 
         Sepal Width < 2.85---> Iris-virginica : 3, Iris-versicolor : 7, 
         Sepal Width > 2.85---> Iris-versicolor : 7, 
   Petal Width > 1.7---> Iris-virginica : 24, Iris-versicolor : 1, 
      Sepal Length < 5.95---> Iris-virginica : 3, Iris-versicolor : 1, 
         Sepal Width < 3.0---> Iris-virginica : 3, 
         Sepal Width > 3.0---> Iris-versicolor : 1, 
      Sepal Length > 5.95---> Iris-virginica : 21, 
Pruned. Now testing on pruned tree. . .


Results : (Majority Classifier Accuracy, Unpruned Accuracy, Pruned Accuracy)


('Accuracy  on fold 1', ' =   0.20                  1.00    13 nodes                1.00    9 nodes ')
('Accuracy  on fold 2', ' =   0.27                  0.87    13 nodes                0.87    9 nodes ')
('Accuracy  on fold 3', ' =   0.27                  0.93    13 nodes                1.00    5 nodes ')
('Accuracy  on fold 4', ' =   0.33                  1.00    13 nodes                1.00    9 nodes ')
('Accuracy  on fold 5', ' =   0.13                  0.87    13 nodes                0.93    5 nodes ')
('Accuracy  on fold 6', ' =   0.20                  0.93    9 nodes                0.93    9 nodes ')
('Accuracy  on fold 7', ' =   0.27                  1.00    13 nodes                1.00    9 nodes ')
('Accuracy  on fold 8', ' =   0.40                  0.93    13 nodes                0.93    9 nodes ')
('Accuracy  on fold 9', ' =   0.20                  0.93    13 nodes                0.93    9 nodes ')
('Accuracy  on fold 10', ' =   0.33                  0.93    13 nodes                0.93    13 nodes ')





