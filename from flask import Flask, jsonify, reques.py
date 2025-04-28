from flask import Flask, jsonify, request
from datetime import datetime, date
from typing import Dict, List

app = Flask(__name__)


metal_data: Dict[str, List[Dict[str, any]]] = {
    "gold": [
        {"date": date(2023, 1, 1), "price": 1800.0},
        {"date": date(2023, 1, 2), "price": 1810.0},
        {"date": date(2023, 1, 3), "price": 1820.0},
        {"date": date(2023, 1, 4), "price": 1815.0},
        {"date": date(2023, 1, 5), "price": 1825.0},
        {"date": date(2024, 1, 20), "price": 2024.0},
    ],
    "silver": [
        {"date": date(2023, 1, 1), "price": 22.0},
        {"date": date(2023, 1, 2), "price": 22.5},
        {"date": date(2023, 1, 3), "price": 23.0},
        {"date": date(2023, 1, 4), "price": 22.8},
        {"date": date(2023, 1, 5), "price": 23.2},
        {"date": date(2024, 1, 20), "price": 25.5}
    ],
    "platinum": [
        {"date": date(2023, 1, 1), "price": 1000.0},
        {"date": date(2023, 1, 2), "price": 1010.0},
        {"date": date(2023, 1, 3), "price": 1020.0},
        {"date": date(2023, 1, 4), "price": 1015.0},
        {"date": date(2023, 1, 5), "price": 1025.0},
        {"date": date(2024, 1, 20), "price": 1100.0},
    ]
}


@app.route('/metals/current', methods=['GET'])
def get_current_prices():
    
    current_prices = {}
    for metal, prices in metal_data.items():
        if prices:  # Check if the list is not empty
            # Find the most recent date
            latest_date = max(price['date'] for price in prices)
            # Get the price for the most recent date
            latest_price = next(price['price'] for price in prices if price['date'] == latest_date)

            current_prices[metal] = {"price": latest_price, "date": latest_date.strftime("%Y-%m-%d")}
    return jsonify(current_prices)


@app.route('/metals/history', methods=['GET'])
def get_historical_prices():

    metal = request.args.get('metal')
    date_from_str = request.args.get('date_from')
    date_to_str = request.args.get('date_to')

    if not metal or not date_from_str or not date_to_str:
        return jsonify({"error": "Missing required parameters (metal, date_from, date_to)"}), 400

    try:
        date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date()
        date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    if metal not in metal_data:
        return jsonify({"error": "Metal not found"}), 404

    historical_data = []
    for item in metal_data[metal]:
        if date_from <= item['date'] <= date_to:
            historical_data.append({"date": item['date'].strftime("%Y-%m-%d"), "price": item['price']})

    return jsonify(historical_data)


if __name__ == '__main__':
    app.run(debug=True)
