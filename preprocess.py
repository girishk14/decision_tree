__author__ = 'Girish'
import json

#This module contains routines to pre_process the 5 selected datasets, and obtain the metadata, features and lebels in the form that the decsion tree expects

'''
Format Description:


1. Dataset:  An array of tuples, where each tuple represents the feature vectors, i.e the n features of the examples
2. Labels: The classes corresponding to the examples in the dataset
3. Metadata ;This contains information about the data, i.e types, domains and statistical features of attributes
4. Missing Data: Replace missing data with the value having the highest probability, or the average of all values

'''
def mean(lst):
	sum = 0
#        print(lst)
	for val in lst:
		#print(val)
		if val.strip()!='?':
			sum = sum + float(val)
	return (sum/float(len(lst)))	

def most_common(lst):
    return max(set(lst), key=lst.count)

def pre_process(control_file):
	dataset = []
	#The control file is to instruct the pre_processer on how to view the data
	labels = [] 
	with open(control_file) as data_file:    
		   metadata  = json.load(data_file)
	sep = metadata['sep'] if 'sep' in metadata.keys() else ','
	for f in  metadata['location']:
		with open(f, 'r') as ifile:
			for line in ifile:
				attrs = line.strip().split(sep)
				dataset.append([attr for i, attr in enumerate(attrs) if i!=metadata['class_position']])
				labels.append(attrs[metadata['class_position']])	
					
	#To compute means, and replace missing data with thse values		
	metadata['attr_mean'] = []
	for i, atype in enumerate(metadata['attr_types']):
		print(i, atype)
		if atype=='c':
			metadata['attr_mean'].append(mean([instance[i] for instance in dataset]))
  
		else:
			metadata['attr_mean'].append(most_common([instance[i] for instance in dataset]))
	print(metadata['attr_mean'])
	for example in dataset:
		for attr in range(0, len(metadata['attr_types'])):
		 	if example[attr].strip() == '?':
				example[attr] = metadata['attr_mean'][attr]	
				
			if metadata['attr_types'][attr] == 'c':
				example[attr] = float(example[attr])
	return (dataset, labels, metadata)
	
		


def make_control_file_HAPT():
	cf = open('data/HAPT/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/HAPT/Train/train.txt' , 'data/HAPT/Test/test.txt']
	metadata['attr_names'] = []
	metadata['attr_types'] = []	
	with open('data/HAPT/features.txt', 'r') as ffile:
		for line in ffile:
			metadata['attr_names'].append(line.strip())
			metadata['attr_types'].append('c')
	metadata['class_position'] = len(metadata['attr_names'])
	metadata['class_name'] = "Action/Movement Made" 
	metadata['sep'] = ' '
	cf.write(json.dumps(metadata, indent=1))
	metadata['c_split_limit'] = 5
	

def make_control_file_Mushroom():
	cf = open('data/Mushroom/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Mushroom/agaricus-lepiota.data']
	metadata['attr_names'] = []
	metadata['attr_types']  = []
	metadata['class_name']="Poisonous/Edible"
	
	with open('data/Mushroom/features.txt', 'r') as ffile:
		for line in ffile:
			metadata['attr_names'].append((line.strip()).split(' ')[1])
			metadata['attr_types'].append('d')
	metadata['class_position'] = 0
	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Chess():
	cf = open('data/Chess/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Chess/krkopt.data']
	metadata['attr_names'] = ['White King File', 'White King Rank', 'White Rook File', 'White Rook Rank', 'Black King File', 'Black King Rank']
	metadata['class_name'] = 'Optimal Depth'
	metadata['attr_types'] = ['d'] * 6
	metadata['class_position'] = 6
	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Iris():
	cf = open('data/Iris/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Iris/iris.data']
	metadata['class_name'] = 'Class'
	metadata['attr_names'] = ['Sepal Length', 'Sepal Width', 'Petal Length', 'Petal Width']
	metadata['attr_types'] = ['c'] * 4 
	metadata['class_position'] = 4
	metadata['c_split_limit'] = 2
	cf.write(json.dumps(metadata, indent=1))

def make_control_file_BreastCancer():
	cf = open('data/BreastCancer/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/BreastCancer/breast_cancer.data']
	metadata['class_name'] = 'Tumor'
	metadata['attr_names'] = ['Clump Thickness', 'Uniformity of Cell Shape', 'Uniformity of Cell Size', 'Marginal Adhesion', 'Single Epithelial Cell Size', 'Bare Nuclei', 'Bland Chromatin', 'Normal Nucleoli', 'Mitoses'] 
	metadata['attr_types'] = ['c'] * 9
	metadata['class_position'] = 9
	metadata['c_split_limit'] = 2
	cf.write(json.dumps(metadata, indent=1))

def make_control_file_ILPD():
	cf = open('data/IndianLiver/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/IndianLiver/ILDP.data']
	metadata['class_name'] = 'Selector'
	metadata['attr_names'] = ['Age', 'Gender',  'TB Total Bilirubin', 'DB Direct Bilirubin','Alkphos Alkaline Phosphotase','Sgpt Alamine Aminotransferase','Sgot Aspartate Aminotransferase','TP Total Protiens','ALB Albumin','A/G Ratio Albumin and Globulin Ratio']

        metadata['attr_types'] = ['c', 'd', 'c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']
	metadata['class_position'] = 10
	metadata['c_split_limit'] = 2
	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Pima():
	cf = open('data/Pima/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Pima/diabetes.data']
	metadata['class_name'] = 'Class'	
        metadata['attr_types'] = ['c', 'c', 'c', 'c', 'c', 'c', 'c', 'c']
	metadata['class_position'] = 8
	metadata['c_split_limit'] = 2
	metadata['attr_names'] = ['Number of times pregnant','Plasma glucose concentration a 2 hours in an oral glucose tolerance test','Diastolic blood pressure (mm Hg)','Triceps skin fold thickness (mm)','2-Hour serum insulin (mu U/ml)','Body mass index (weight in kg/(height in m)^2)','Diabetes pedigree function','Age (years) ']
	cf.write(json.dumps(metadata, indent=1))

def make_control_file_Adult():
	cf = open('data/Adult/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Adult/adult.data', 'data/Adult/adult.test']
	
	metadata['attr_names'] = []
	metadata['attr_types'] = []	
	
	with open('data/Adult/features.txt', 'r') as ffile:
		for line in ffile:
			parts =(line.strip()).split(':');
			metadata['attr_names'].append(parts[0])
			metadata['attr_types'].append('c') if parts[1].strip()=='continuous.' else metadata['attr_types'].append('d')
	
	metadata['class_position'] = len(metadata['attr_names'])
	metadata['class_name'] = "Salary"
	metadata['c_split_limit'] = 3
	

	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Phising():
	cf = open('data/Phising/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Phising/dataset.arff']
	metadata['attr_names'] = []
	metadata['attr_types'] = []	
	
	with open('data/Phising/features.txt', 'r') as ffile:
		for line in ffile:
			parts =(line.strip()).split(' ');
			metadata['attr_names'].append(parts[1])
			metadata['attr_types'].append('d')
	
	metadata['class_position'] = len(metadata['attr_names'])
	metadata['class_name'] = 'Result'
	metadata['c_split_limit'] = 0

	cf.write(json.dumps(metadata, indent=1))




def make_control_files():
	make_control_file_Phising()
	make_control_file_Pima()
	make_control_file_Mushroom()
	make_control_file_BreastCancer()
	make_control_file_Chess()
	make_control_file_Iris()


#make_control_files()
#pre_process('data/Adult/control.json')



''''

def replace_missing_data(dataset, attr_types):
	#The strategy for missing data is to choose the majority value in case of discrete values and choose the mean in case of continuous values
	for attr in range(0, len(attr_types)):
		;
'''
