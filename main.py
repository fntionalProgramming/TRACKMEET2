from flask import Flask, render_template, jsonify
from run_scrappers import run_all_scrapper
from pathlib import Path

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/load_data', methods=['POST'])
def load_data():
    print("loading data button triggered")
    # running all the scrappers
    # alos we have to run the scrapper everytime becasue the information
    # from trackie and sssad can change in real time
    # data should be stored in the rolling_schedule director
    run_all_scrapper()
    # load the data from the rolling_schedule directory
    # and return it as a json response because javascript browser are sandobx so you cannot access files from ther 
    rolling_schedule_dir = Path("rolling_schedule")
    meets_info = []
    for file_path in rolling_schedule_dir.iterdir():
        if file_path.is_file() and file_path.suffix == '.csv':
            with open(file_path, 'r') as file:
                data = file.read()
            meets_info.append([
                file_path.stem,  # get the file name without extension
                data.splitlines()  # split the contents into lines
            ])
    # return a success response with the meets info
    return jsonify({"status": "success", "meets_info": meets_info})

'''
same function as above but this one is use to load the initial data
'''
@app.route('/load_initial_data', methods=['POST'])
def load_initial_data():
    print("loading initial data")
    rolling_schedule_dir = Path("rolling_schedule")
    if not rolling_schedule_dir.exists():
        return jsonify({"status": "unsuccessful", "error_message": "Please press load_data_button inorder to get data of athletes!<br>The data from sssad and trackie website will be updating constantly so i recommend you always fetch new data when you use it"})
    meets_info = []
    for file_path in rolling_schedule_dir.iterdir():
        if file_path.is_file() and file_path.suffix == '.csv':
            with open(file_path, 'r') as file:
                data = file.read()
            meets_info.append([
                file_path.stem,  # get the file name without extension
                data.splitlines()  # split the contents into lines
            ])
    # return a success response with the meets info
    return jsonify({"status": "success", "meets_info": meets_info})

            
if __name__ == "__main__":
    app.run(debug=True)
