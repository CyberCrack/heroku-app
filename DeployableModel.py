import pickle
import time

import numpy as np


def rotate(l, n):
	return l[n:] + l[:n]


def getPredictions(gre, gpa, rank):
	allPredictions = []
	inputArray = [gre, gpa]
	rankArray = [1, 0, 0]
	ranks = [2, 3, 4]
	if rank == 1:
		rankArray = [0, 0, 0]
	else:
		for thisRank in ranks:
			if thisRank != rank:
				rankArray = rotate(rankArray, -1)
			else:
				break
	# print(rankArray)
	inputArray.extend(rankArray)
	inputArray = np.array([inputArray])
	# print(inputArray)

	pickle_in = open("Best Models with Scaler/1194728537270577555_SVM_2020-08-03_20-08-17v1.pickle", "rb")
	clf1 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/1194728537270577555_SVM_Scaler_2020-08-03_20-08-17.pickle", "rb")
	scaler1 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler1.transform(inputArray)
	allPredictions.append(clf1.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/1765715477230460282_NeuralNetwork_2020-08-03_20-27-20v2.pickle", "rb")
	clf2 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/1765715477230460282_NeuralNetwork_Scaler_2020-08-03_20-27-20.pickle", "rb")
	scaler2 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler2.transform(inputArray)
	allPredictions.append(clf2.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/2194900686905654902_NeuralNetwork_2020-08-03_21-15-00v3.pickle", "rb")
	clf3 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/2194900686905654902_NeuralNetwork_Scaler_2020-08-03_21-15-00.pickle", "rb")
	scaler3 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler3.transform(inputArray)
	allPredictions.append(clf3.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/3164770818990651256_AdaBoost_2020-08-03_20-28-03v2.pickle", "rb")
	clf4 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/3164770818990651256_AdaBoost_Scaler_2020-08-03_20-28-03.pickle", "rb")
	scaler4 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler4.transform(inputArray)
	allPredictions.append(clf4.predict(scaledArray))

	pickle_in = open("Best Models with Scaler/5433617813888004140_RandomForestClassifier_2020-08-03_20-27-09v2.pickle", "rb")
	clf5 = pickle.load(pickle_in)
	pickle_in.close()
	pickle_in = open("Best Models with Scaler/5433617813888004140_RandomForestClassifier_Scaler_2020-08-03_20-27-09.pickle", "rb")
	scaler5 = pickle.load(pickle_in)
	pickle_in.close()
	scaledArray = scaler5.transform(inputArray)
	allPredictions.append(clf5.predict(scaledArray))

	allPredictions = [int(prediction) for prediction in allPredictions]

	return 0 if allPredictions.count(0) > allPredictions.count(1) else 1

if __name__ == "__main__":
	startTime = time.time()
	print(getPredictions(0, 0, 4))
	print(time.time() - startTime)
