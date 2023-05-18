import pandas as pd
from datetime import timedelta
from prefect import task, flow
import pickle
import time
# from prefect.schedules import IntervalSchedule

# Define the task to read data from a CSV file
@task
def read_csv_file(file_path):
    df = pd.read_csv(file_path, header=None)
    return df

# Define the schedule for pipeline execution (e.g., every 5 minutes)
# schedule = IntervalSchedule(interval=timedelta(minutes=5))

# Define the task to load the model
@task
def load_model(model_file):
    with open(model_file, 'rb') as file:
        model = pickle.load(file)
    return model

# Define the task to process data DataFrame
@task
def preprocess_data(data):
    processed_data = data.iloc[:, 1:29]
    actual = data.iloc[:, 30:31]
    id = data.iloc[:,0:1]
    return processed_data, actual,id

# Define the task to predict fraud
@task
def predict_data(data,model):

    
    prediction = model.predict(data)
    return prediction


# Define the task to write data to a CSV file
@task
def write_csv_file(file_path,data):
    
    data.to_csv('output.csv',mode='a', header=False, index=False)

# Define the task to combine data
@task
def combine_data(df1,df2,df3,df4):
    df4 = pd.DataFrame(df4, columns=['Prediction'])
    
    df5 = pd.concat([df1, df2, df3, df4], axis=1)
    return df5
    

# Define the flow
@flow
def process_data():
    file_path_1 = "../data_generation/source1.csv"
    file_path_2 = "../data_generation/source2.csv"
    file_path_3 = "output.csv"
    
    data_1 = read_csv_file(file_path_1)
    data_2 = read_csv_file(file_path_2)

    processed_data_1, actual_1, id_1= preprocess_data(data_1)
    processed_data_2, actual_2, id_2= preprocess_data(data_2)

    model_file = "../analysis/pipeline.pkl"
    model = load_model(model_file)

    prediction_1 = predict_data(processed_data_1,model)
    prediction_2 = predict_data(processed_data_2,model)
    
    finaldata_1 = combine_data(id_1,processed_data_1,actual_1,prediction_1)
    finaldata_2 = combine_data(id_2,processed_data_2,actual_2,prediction_2)

    write_csv_file(file_path_3, finaldata_1)
    write_csv_file(file_path_3, finaldata_2)
    

# Run the flow
if __name__ == "__main__":
    for i in range(2000):
        process_data()
        time.sleep(5)
