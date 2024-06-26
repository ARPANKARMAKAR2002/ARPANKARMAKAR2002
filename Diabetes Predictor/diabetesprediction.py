import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import accuracy_score

#loading diabetes dataset to a pandas DataFrame
<<<<<<< HEAD
diabetes_dataset = pd.read_csv("data.csv")
=======
diabetes_dataset = pd.read_csv("diabetes.csv")
>>>>>>> 8384a151922bfe95601744685b784597e952ff93

pd.read_csv

diabetes_dataset.head()

# number of rows and Columns in this dataset
diabetes_dataset.shape

# getting the statistical measures of the data
diabetes_dataset.describe()

diabetes_dataset['Outcome'].value_counts()

diabetes_dataset.groupby('Outcome').mean()
# separating the data and labels
X = diabetes_dataset.drop(columns = 'Outcome', axis=1)
Y = diabetes_dataset['Outcome']
print(X)
print(Y)

scaler=StandardScaler()
scaler.fit(X)

standardized_data = scaler.transform(X)

print(standardized_data)

X=standardized_data
Y=diabetes_dataset['Outcome']

print(X)
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify=Y, random_state=2)
print(X.shape, X_train.shape, X_test.shape)

classifier = svm.SVC(kernel='linear')
classifier.fit(X_train, Y_train)
X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)

print('Accuracy score of the training data : ', training_data_accuracy)

X_test_prediction = classifier.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)

print('Accuracy score of the test data : ', test_data_accuracy)

data = {"pregnancies":int(input("Enter number of pregnancies: ")),
        "glucose":int(input("Enter glucose level: ")),
        "bloodpressure":int(input("Enter blood pressure: ")),
        "skinthickness":int(input("Enter skin thickness: ")),
        "insulin":int(input("Enter insulin level: ")),
        "bmi":float(input("Enter BMI level: ")),
        "diabetespedegreefunction":float(input("Enter DiabetesPedegreeFunction: ")),
        "age":int(input("Enter age: "))
        }

input_data=list(data.values())
# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

# standardize the input data
std_data = scaler.transform(input_data_reshaped)
print(std_data)

prediction = classifier.predict(std_data)
print(prediction)

if (prediction[0] == 0):
  print('The person is not diabetic')
else:
  print('The person is diabetic')