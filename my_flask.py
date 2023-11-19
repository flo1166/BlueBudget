from flask import Flask, render_template, jsonify
from flask import request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('blue_budget_website.html')

@app.route('/get-groundwater-data')
def get_groundwater_data():
    data = [
        {'date': '2023-11-30', 'level': 7.8, 'type': 'Predicted'},
        {'date': '2023-11-30', 'level': 7.8, 'type': 'Predicted'},
        {'date': '2023-11-30', 'level': 7.8, 'type': 'Predicted'},
        {'date': '2023-11-30', 'level': 7.8, 'type': 'Predicted'},
        {'date': '2023-11-30', 'level': 7.8, 'type': 'Predicted'},
    ]
    return jsonify(data)


@app.route('/get-water-budget')
def get_water_budget():
    return jsonify({'waterBudget': 125})



@app.route('/get-data-for-postal-code')
def get_data_for_postal_code():
    postal_code = request.args.get('postalCode')
    # Assuming `data_source` is your data list or database query
    relevant_data = [entry for entry in data_source if entry['postalCode'] == postal_code]  # data source ist der datensatz wo die postleitzahl... gespeichert ist
    return jsonify(relevant_data)

if __name__ == '__main__':
    app.run(debug=True)


