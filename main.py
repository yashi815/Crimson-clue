from flask import Flask, render_template, request
from datetime import datetime, timedelta
import os

app = Flask(__name__)

DATA_FILE = "period_data.txt"

def save_period_date(date):
    with open(DATA_FILE, "a") as f:
        f.write(date + "\n")

def read_period_dates():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return [line.strip() for line in f.readlines()]

@app.route('/')
def index():
    previous_dates = read_period_dates()
    return render_template("index.html", previous_dates=previous_dates)

@app.route('/predict', methods=['POST'])
def predict():
    start_date_str = request.form['start_date']
    cycle_length = int(request.form['cycle_length'])

    start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    next_period_date = start_date + timedelta(days=cycle_length)

    save_period_date(start_date_str)

    previous_dates = read_period_dates()

    return render_template("index.html",
                           next_date=next_period_date.strftime('%Y-%m-%d'),
                           previous_dates=previous_dates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)