import csv
import random
import time

def randomly_select_row(input_file, output_file):
    while True:
        with open(input_file, 'r') as file:
            reader = csv.reader(file)
            rows = list(reader)
            selected_row = random.choice(rows)

        with open(output_file, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(selected_row)

        print(f"Randomly selected row has been written to '{output_file}'.")
        time.sleep(5)  # Delay for 5 seconds


input_file = 'creditcard.csv'  #  input CSV file path
output_file = 'source1.csv'  #  desired output CSV file path

randomly_select_row(input_file, output_file)