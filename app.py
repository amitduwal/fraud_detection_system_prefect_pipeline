from flask import Flask, render_template, request
import csv
import time

app = Flask(__name__, static_url_path='/static')

csv_file = 'pipeline_prefect/output.csv'

def classify_last_n_lines(file_path, n):
    classification = []

    with open(file_path, 'r') as file:
        lines = file.readlines()

    last_n_lines = lines[-n:]
    csv_reader = csv.reader(last_n_lines, delimiter=',')

    for row in csv_reader:
        first_column = row[0]
        last_two_columns = row[-2:]
        if last_two_columns == ['0', '0.0']:
            classification.append(f"{first_column},True Negative")
        elif last_two_columns == ['1', '1.0']:
            classification.append(f"{first_column},True Positive")
        elif last_two_columns == ['0', '1.0']:
            classification.append(f"{first_column},False Positive")
        elif last_two_columns == ['1', '0.0']:
            classification.append(f"{first_column},False Negative")

    return classification


@app.route('/get_data')
def get_data():
    n = 8
    result = classify_last_n_lines(csv_file, n)
    return result

def search_csv_file(filename, search_value):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == search_value:
                return row
    return None

@app.route('/transaction_details', methods=['POST'])
def transaction_details():
    transaction_id = request.form['transaction_id']
    details = search_csv_file(csv_file,transaction_id)
    
    return render_template('transaction.html', details=details)

@app.route('/')
def display_csv():
    # return render_template('home.html', rows=rows)
    n = 8
    result = classify_last_n_lines(csv_file, n)
    return render_template('home.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)

