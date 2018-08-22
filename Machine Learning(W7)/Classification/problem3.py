# Artifical Intelligence @ edX
# Week7 Project Problem 3
# Classification
# Renjie Li, rl2932@columbia.edu
import sys
import numpy
from sklearn.model_selection import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

class CL(object):

    def __init__(self):
        self.ori_data = numpy.genfromtxt(sys.argv[1], delimiter=",")  # data from input
        self.output_name = sys.argv[2]  # desired output name, in this case is output2.csv
        self.plot()
        self.x = self.ori_data[:, :-1]
        self.y = self.ori_data[:, -1]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.4, random_state=42,stratify=self.y)

        fo = open(self.output_name, 'w')
        print('start')

        params = {
            'C': [0.1, 0.5, 1, 5, 10, 50, 100],
            'kernel': ['linear']
        }

        grid_thing = GridSearchCV(SVC(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('svm_linear', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))

        print('linear finished')

        params = {
            'C': [0.1,1,3],
            'degree': [4, 5, 6],
            'gamma': [0.1, 0.5],
            'kernel': ['linear']
        }

        grid_thing = GridSearchCV(SVC(kernel='poly'), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('svm_polynomial', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))

        print('poly finished')
        params = {
            'C': [0.1,0.5,1,5,10,50,100],
            'gamma': [0.1, 0.5,1,3,6,10],
            'kernel': ['rbf']
        }

        grid_thing = GridSearchCV(SVC(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('svm_rbf', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))
        print('rbf finished')

        params = {
            'C': [0.1, 0.5, 1, 5, 10, 50, 100],
            'solver': ['liblinear']
        }
        grid_thing = GridSearchCV(LogisticRegression(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('logistic', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))
        print('logistic finished')
        params = {
            'n_neighbors': range(1, 51),
            'leaf_size': range(5, 65, 5),
            'algorithm': ['auto']
        }
        grid_thing = GridSearchCV(KNeighborsClassifier(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('knn', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))
        print('knn finished')
        params = {
            'max_depth': range(1, 51),
            'min_samples_split': range(2, 11)
        }
        grid_thing = GridSearchCV(DecisionTreeClassifier(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('decision_tree', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))
        print('decision finished')
        params = {
            'max_depth': range(1, 51),
            'min_samples_split': range(2, 11)
        }
        grid_thing = GridSearchCV(RandomForestClassifier(), params, n_jobs=1)
        grid_thing.fit(self.x_train, self.y_train)
        fo.write("%s, %0.2f, %0.2f\n" % ('random_forest', grid_thing.best_score_, grid_thing.score(self.x_test, self.y_test)))
        print('random finished')
        fo.close()
        print('end')

    def plot(self):
        plt.figure()
        plt.plot(self.ori_data[self.ori_data[:,2] == 1.0, 0], self.ori_data[self.ori_data[:,2] == 1.0, 1], 'ro')
        plt.plot(self.ori_data[self.ori_data[:, 2] == 0.0, 0], self.ori_data[self.ori_data[:, 2] == 0.0, 1], 'bo')
        plt.show()


if __name__ == "__main__":
    Classification = CL()