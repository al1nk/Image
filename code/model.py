'''
    Sample predictive model.
    You must supply at least 4 methods:
    - fit: trains the model.
    - predict: uses the model to perform predictions.
    - save: saves the model.
    - load: reloads the model.
    '''
import pickle
import numpy as np   # We recommend to use numpy arrays
from os.path import isfile
import sklearn

from sklearn import pipeline as ppl
from sklearn import preprocessing as pp
from sklearn import decomposition as dc
from sklearn import feature_selection as fs
from sklearn import cluster as cls

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.cluster import  KMeans
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV

from preprocessing import Preprocessing as CustPp

from time import time

datapath = "../public_data/"

class model:
    def __init__(self):
        '''
            This constructor is supposed to initialize data members.
            Use triple quotes for function documentation.
            '''
        self.num_train_samples=0
        self.num_feat=1
        self.num_labels=1
        self.vt = 0.87
        self.is_trained=False
        self.mod = RandomForestClassifier(n_estimators = 100)
        '''
        The HP of this predictor were found with the ./HyperParameter/model.py GS implementation
        '''
        self.ppl = ppl.Pipeline([('prepro', CustPp()),
                                 ('mod', self.mod)])
    
    def fit(self, X, Y):
        '''
            This function should train the model parameters.
            Here we do nothing in this example...
            Args:
            X: Training data matrix of dim num_train_samples * num_feat.
            y: Training label matrix of dim num_train_samples * num_labels.
            Both inputs are numpy arrays.
            For classification, labels could be either numbers 0, 1, ... c-1 for c classe
            or one-hot encoded vector of zeros, with a 1 at the kth position for class k.
            The AutoML format support on-hot encoding, which also works for multi-labels problems.
            Use data_converter.convert_to_num() to convert to the category number format.
            For regression, labels are continuous values.
            '''
        # For multi-class problems, convert target to be scikit-learn compatible
        # into one column of a categorical variable
        y=self.convert_to_num(Y, verbose=False)
        
        self.num_train_samples = X.shape[0]
        if X.ndim>1: self.num_feat = X.shape[1] # Does not work for sparse matrices
        print("FIT: dim(X)= [{:d}, {:d}]".format(self.num_train_samples, self.num_feat))
        num_train_samples = y.shape[0]
        if y.ndim>1: self.num_labels = y.shape[1]
        print("FIT: dim(y)= [{:d}, {:d}]".format(num_train_samples, self.num_labels))
        if (self.num_train_samples != num_train_samples):
            print("ARRGH: number of samples in X and y do not match!")
        
        self.ppl.fit(X, y)
        self.is_trained=True
        print("Done fitting !")
    
    def predict(self, X):
        '''
            This function should provide predictions of labels on (test) data.
            Here we just return zeros...
            Make sure that the predicted values are in the correct format for the scoring
            metric. For example, binary classification problems often expect predictions
            in the form of a discriminant value (if the area under the ROC curve it the metric)
            rather that predictions of the class labels themselves. For multi-class or multi-labels
            problems, class probabilities are often expected if the metric is cross-entropy.
            Scikit-learn also has a function predict-proba, we do not require it.
            The function predict eventually can return probabilities.
            '''
        num_test_samples = X.shape[0]
        if X.ndim>1: num_feat = X.shape[1]
        print("PREDICT: dim(X)= [{:d}, {:d}]".format(num_test_samples, num_feat))
        if (self.num_feat != num_feat):
            print("ARRGH: number of features in X does not match training data!")
        print("PREDICT: dim(y)= [{:d}, {:d}]".format(num_test_samples, self.num_labels))
        
        # Return predictions as class probabilities
        y = self.ppl.predict_proba(X)
        return y
    
    def save(self, path="./"):
        with open(path + '_model.pickle', 'wb') as f:
            print('modele name : ', path + '_model.pickle')
            pickle.dump(self , f)

    def load(self, path="./"):
        modelfile = path + '_model.pickle'
        if isfile(modelfile):
            with open(modelfile, 'rb') as f:
                self = pickle.load(f)
            print("Model reloaded from: " + modelfile)
        return self

    def convert_to_num(self, Ybin, verbose=True):
        ''' Convert binary targets to numeric vector (typically classification target values)'''
        if verbose: print("Converting to numeric vector")
        Ybin = np.array(Ybin)
        if len(Ybin.shape) ==1: return Ybin
        classid=range(Ybin.shape[1])
        Ycont = np.dot(Ybin, classid)
        if verbose: print(Ycont)
        return Ycont

def parseFile(path):
    
    with open(path, "r") as f:
        data = []
        for line in f:
            bits = []
            for bit in line.split(" "):
                bits.append(float(bit))
            data.append(bits)
        return np.array(data)


if __name__ == '__main__':
    
    traindata = parseFile(datapath+"cifar10_train.data")
    validdata = parseFile(datapath+"cifar10_valid.data")
    label = parseFile(datapath+"cifar10_train.solution")
    
    model = model()
    start = time()
    model.fit(traindata, label)
    fittime = time()
    model.predict(validdata)
    predtime = time()
    print("Fitting : {}\nPredicting : {}\nScore : {}".format(fittime-start, predtime-fittime, model.ppl.score(traindata, label.argmax(axis=1))))



