import sys
import math
import csv


#Calculate Euclidean distance
def euclideanDistance (existingRecord, newRecord):
	dist = 0.0
	for i in range (3):
		dist += (existingRecord[i] - newRecord[i])**2
	return [math.sqrt(dist),existingRecord[3], existingRecord[4], existingRecord[5], existingRecord[6],
	existingRecord[7], existingRecord[8], existingRecord[9], existingRecord[10], existingRecord[11],
	existingRecord[12], existingRecord[13], existingRecord[14], existingRecord[15]]


#Find K-Nearest Neighbors
def kNearestNeighbors(dataset, newRecord, k):
	distances = []
	for row in dataset:
		distance = euclideanDistance(row, newRecord)
		distances.append(distance)
	distances.sort(key=lambda x: x[0])
	return distances[0:k]


#Predict Classification
def predict(dataset, newRecord, k):
	nearestNeighbors = kNearestNeighbors(dataset,newRecord,k)
	return nearestNeighbors


#Read CSV
def readCSV(filename):
	dataSet = list()
	with open(filename, 'r', encoding="utf8", errors='ignore') as file:
		csvReader = csv.reader(file)
		for row in csvReader:
			if not row:
				continue
			dataSet.append(row)
	#Convert String Data to Float
	for i in range(3):
		stringToFloatColumn(dataSet, i)
	return dataSet


#Convert Strings to Float in a Single Column
def stringToFloatColumn(dataSet, column):
	for row in dataSet:
		row[column] = float(row[column].strip())


#Filter Function
def filterByColumnContent(dataSet, column, value):
	filteredDataSet = []
	for row in dataSet:
		if (row[column] == value):
			filteredDataSet.append(row)
	return filteredDataSet


#Normalize Input Variables
def normalize(value, min, max):
	return (value-min)/(max-min)


#Get Match Percentage (Min approx: 0, Max approx: 5)
def matchPercent(euclideanDistance):
	return "{:.2f}".format((5 - euclideanDistance)/5 * 100)


#Print Predictions
def printPredictions(predictions):
	#Print Nearest Neighbors
	print("-----Predictions--------------------------------------------------------------------")
	for individual in predictions:
		print("Match: ", matchPercent(individual[0]), "%\nName: ", individual[3], "\nSport: ", individual[12], "\nEvent: ", individual[13], "\nAge: ", individual[5], "\nHeight: " , individual[6], "\nWeight: ", individual[7], "\nPlace of Birth: ", individual[2], "\nCountry Represented: ", individual[4])
		print("------------------------------------------------------------------------------------")
	#Print most common classification
	nearestSports = []
	for neighbor in predictions:
		nearestSports.append(neighbor[12])
	mostCommonClass = max(set(nearestSports), key=nearestSports.count)
	print("Ideal Sport: ", mostCommonClass)




def main():
	#Inputs----------------------------------------------------------
	filename = "data-sets/2012Olympics.csv"
	sex = "M" #M,F or Blank (column: 3)
	birthCountry = "GER" #Any abbreviated country code (column: 4)
	age = 21
	height = 200
	weight = 97
	k = 3
	#---------------------------------------------------------------
	#Read CSV
	dataSet = readCSV(filename)
	#Normalize Input Variables
	normalizedAge = normalize(age, 13, 65)
	normalizedHeight = normalize(height, 132, 221)
	normalizedWeight = normalize(weight, 36, 218)
	#STEP 1 - Filter by Sex and Birth Country (If applicable)
	if (sex != ""):
		dataSet = filterByColumnContent(dataSet, 3, sex)
	if (birthCountry != ""):
		dataSet = filterByColumnContent(dataSet, 4, birthCountry)
	#STEP 2 - Return the K-Nearest individuals from the filtered dataset using normalized age, height & weight
	prediction = predict(dataSet, [normalizedAge, normalizedHeight, normalizedWeight], k)
	#STEP 3 - Print out k closest matches and predicted classification
	if (len(prediction) == 0):
		print("No athlete matches found.")
	else:
		printPredictions(prediction)



if __name__ == "__main__":
	main()