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

def pre_process(name):
	return eval("pre_process_" + name)



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
	metadata['attr_names'].append("Action/Movement Made")
	metadata['attr_types'].append('class')
	cf.write(json.dumps(metadata, indent=1))
	
	

def make_control_file_Mushroom():
	cf = open('data/Mushroom/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Mushroom/agaricus-lepiota.data']
	metadata['attr_names'] = []
	metadata['attr_names'].append("Poisonous/Edible")
	metadata['attr_types'] = []	
	metadata['attr_types'].append('class')
	
	with open('data/Mushroom/feature.txt', 'r') as ffile:
		for line in ffile:
			metadata['attr_names'].append((line.strip()).split(' ')[1])
			metadata['attr_types'].append('d')
	metadata['class_position'] = 0
	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Chess():
	cf = open('data/Chess/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Chess/krkopt.data']
	metadata['attr_names'] = ['White King File', 'White King Rank', 'White Rook File', 'White Rook Rank', 'Black King File', 'Black King Rank', 'Optimal Depth']
	metadata['attr_types'] = ['d'] * 6
	metadata['attr_types'].append('class')
	metadata['class_position'] = 6
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
	metadata['attr_names'].append("Salary")
	metadata['attr_types'].append('class')



	cf.write(json.dumps(metadata, indent=1))


def make_control_file_Phising():
	cf = open('data/Phising/control.json' , 'w')	
	metadata = {}
	metadata['location'] = ['data/Phising/dataset.arff']
	metadata['attr_names'] = []
	metadata['attr_types'] = []	
	
	with open('data/Phising/features.txt', 'r') as ffile:
		for line in ffile:
			print(line)
			parts =(line.strip()).split(' ');
			metadata['attr_names'].append(parts[1])
			metadata['attr_types'].append('d')
	
	metadata['class_position'] = len(metadata['attr_names'])
	metadata['attr_names'].append("Result")
	metadata['attr_types'].append('class')



	cf.write(json.dumps(metadata, indent=1))


make_control_file_Phising()





def mean(lst):
	return  (sum(lst) / float(len(lst)))

def most_common(lst):
    return max(set(lst), key=lst.count)


''''

def replace_missing_data(dataset, attr_types):
	#The strategy for missing data is to choose the majority value in case of discrete values and choose the mean in case of continuous values
	for attr in range(0, len(attr_types)):
		;
'''
