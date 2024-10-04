import pandas as pd

# Loads the dataset to data frame using pandas
df=pd.read_csv("synthetic_parking_occupancy_data.csv", parse_dates=["timestamp"])
print(df.head())

#sorting the values
df.sort_values(by=["parking_space_id","timestamp"], inplace=True) 

# Normalize and Scaling the features
from sklearn.preprocessing import MinMaxScaler
scaler= MinMaxScaler()
df[["day_of_week","hour_of_day"]] = scaler.fit_transform(df[["day_of_week", "hour_of_day"]])

# Creating the sequences for the LSTM model
seq_length=24

import numpy as np 
def create_sequences(data, seq_length):
    sequences=[]
    labels=[]
    for i in range(len(data)-seq_length):
        seq=data[i:i+seq_length]
        label=data[i+seq_length][2] #the occupancy is the third column
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences), np.array(labels)

X,y = [], []
for space_id in df['parking_space_id'].unique():
    space_data = df[df['parking_space_id']=='space_id'][['day_of_week','hour_of_day','occupancy_status']].values
    space_X, space_y = create_sequences(space_data, seq_length)
    X.append(space_X)
    y.append(space_y)

X=np.concatenate(X, axis=0)
y=np.concatenate(y, axis=0)

print(f"Shape of X: {X.shape}")
print(f"Shape of y: {y.shape}")

#splitting the data into training and testing sets
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Shape of X_train: {X_train.shape}")
print(f"Shape of X_test: {X_test.shape}")

# Model training
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout

# Define the LSTM model
model = Sequential()
model.add(LSTM(units=50, activation='relu', input_shape=(seq_length, X_train.shape[2]), return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50, activation='relu', return_sequences=False))
model.add(Dropout(0.2))
model.add(Dense(units=1))

# Compile the model
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2)

# Evaluate the model on the test set
loss = model.evaluate(X_test, y_test)
print(f"Test Loss: {loss}")


