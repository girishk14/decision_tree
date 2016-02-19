import sys
import preprocess
import classification
import decision_tree
import pruning
import random

def shuffle_order(a, b):	
	c = list(zip(a, b))
	random.shuffle(c)
	a, b = zip(*c)
	return a,b

global metadata


def classic_holdout(dataset, labels):
    no_train = int(0.70* len(dataset))
    training_X =  dataset[0:no_train]
    training_Y = labels[0:no_train]
    test_X = dataset[no_train:]
    test_Y = labels[no_train:]
     
    print(len(training_X), len(test_X))
    d_tree  = decision_tree.create_decision_tree(training_X, training_Y)
    print("Tree generated")
    count = 0
    labelled = 0
    for i in range(0, len(test_X)):
        pred = classify_tuple(training_X, training_Y, d_tree, test_X[i])
	if pred == test_Y[i]: #or pred=="Unknown Class":
		count+=1
	labelled+=1
    
    print("Accuracy  on test set = ",  count/float(labelled))

def k_fold_generator(X, y, k_fold):
    subset_size = len(X) / k_fold  # Cast to int if using Python 3
    for k in range(k_fold):
        X_train = X[:k * subset_size] + X[(k + 1) * subset_size:]
        X_valid = X[k * subset_size:][:subset_size]
        y_train = y[:k * subset_size] + y[(k + 1) * subset_size:]
        y_valid = y[k * subset_size:][:subset_size]

        yield X_train, y_train, X_valid, y_valid

def ten_fold_cross_validation(dataset, labels):
    decision_tree.set_metadata(metadata)
    print(metadata)
    fold = 1
    accuracies, pruned_accuracies= [],[]
    for X_train, Y_train, X_test, Y_test in k_fold_generator(dataset, labels, 10):
    	
	t_size = int(0.7 * len(X_train)) #Within the training set, create a 70-30 split for model training, and model tuning (pruning)
	X_model_train =  X_train[0:t_size]
	Y_model_train = Y_train[0:t_size]
	X_valid = X_train[t_size:]
	Y_valid = Y_train[t_size:]

	d_tree = decision_tree.create_decision_tree(X_train[0:t_size], Y_train[0:t_size])
        print("Tree generated. Testing on original tree")
        count = 0    
	
        accuracies.append(classification.get_classification_error(d_tree, X_model_train, Y_model_train, X_test, Y_test))
	
	pruned_tree = pruning.reduced_error_pruning(d_tree, X_model_train, Y_model_train, X_valid, Y_valid)	
	print("Now testing on pruned treee")
	pruned_accuracies.append(classification.get_classification_error(pruned_tree, X_model_train, Y_model_train, X_test, Y_test))

    for fold, (acc, pacc) in (enumerate(zip(accuracies,pruned_accuracies))):
	print("Accuracy  on fold ",  fold+1, ' = ', acc, pacc )




def main():
    global metadata
    preprocess.make_control_files()
    ctrl_file = sys.argv[1] 
    dataset, labels, md = preprocess.pre_process(ctrl_file);
    print("Preproc Complete")
    metadata = md
    classification.set_metadata(md)
    dataset, labels = shuffle_order(dataset, labels)

    ten_fold_cross_validation(dataset, labels)
   


if __name__ == "__main__":
	main()
