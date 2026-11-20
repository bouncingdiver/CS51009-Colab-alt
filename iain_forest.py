import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
import random

# iris = load_iris()
# df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
# df['target'] = iris.target

# X = df.iloc[:, :-1].values
# y = df.iloc[:, -1].values
print("I am running")
##Forest factory##
def forestFactory(max_estimators,storage,split_list, X, y, random_state = 42):
    
    for test in split_list:
        #the 1, is so we don't run a forest with 0 trees and the +1 is to remove 0 counting
        for num_estimators in range(1,max_estimators+1): 
            print("test "+str(test))
            print("estimators "+str(num_estimators))
            
            #max_depth=random.randint(1,max_random_state)
   
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test, random_state=random_state)
            ###X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
            scaler = StandardScaler()
            X_train = scaler.fit_transform(X_train)
            X_test = scaler.transform(X_test)

            classifier = RandomForestClassifier(n_estimators=num_estimators, random_state=random_state)
            classifier.fit(X_train, y_train.values.ravel())

            y_pred = classifier.predict(X_test)

            accuracy = accuracy_score(y_test, y_pred)
            #print(f'Accuracy: {accuracy * 100:.2f}% with the training split of {round((1-test)*100)}% and num_estimators: {num_estimators}')
            
            
            data_test = str(round((1-test)*100)) +"%"
            data = (accuracy, data_test, num_estimators)
            print(data)
            storage.append(data)


            conf_matrix = confusion_matrix(y_test, y_pred)

            # plt.figure(figsize=(8, 6))
            # sns.heatmap(conf_matrix, annot=True, fmt='g', cmap='Blues', cbar=False, 
            #             xticklabels=iris.target_names, yticklabels=iris.target_names)

            # plt.title('Confusion Matrix Heatmap')
            # plt.xlabel('Predicted Labels')
            # plt.ylabel('True Labels')
            feature_importances = classifier.feature_importances_
    #plt.show()
            #print(feature_importances)
    return storage


labels = pd.read_csv('labels.csv')      #cleaned_minute.csv's labels
labels = pd.read_csv('labels_big.csv')  #timeseries.csv's labels

data = pd.read_csv('cleaned_minutes.csv', parse_dates=['timestamp'])
data = pd.read_csv('timeseries.csv', parse_dates=['timestamp'])

#Temporary fix
data = data.drop('timestamp', axis=1)

#Only use when running with timeseries.csv
data = data.drop('time', axis=1)



X = data
y = labels

accuracy_array = []
randomstate_number = 42
split_list = [0.01,0.05,0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60,0.65,0.70,0.75,0.80,0.85,0.90,0.95]
#split_list = [0.95,0.90,0.85,0.80,0.75,0.70,0.65,0.60,0.55,0.50,0.45,0.40,0.35,0.30,0.25,0.20,0.15,0.10,0.05,0.01]
forestFactory(max_estimators=5, storage=accuracy_array, split_list=split_list,random_state=randomstate_number, X=X, y=y)
print(accuracy_array)
print("I am done")