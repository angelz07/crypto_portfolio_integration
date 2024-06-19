import json
import requests
from datetime import datetime
import logging
from flask import Flask, jsonify, request
from .db import add_transaction, get_transactions, delete_transaction, update_transaction, get_crypto_transactions

# Configure logging
logging.basicConfig(level=logging.INFO)

# Flag to enable/disable test transactions
ENABLE_TEST_TRANSACTIONS = True

app = Flask(__name__)

def get_crypto_id(name):
    url = f"https://api.coingecko.com/api/v3/search?query={name}"
    response = requests.get(url)
    data = response.json()
    for coin in data['coins']:
        if coin['name'].lower() == name.lower():
            return coin['id']
    return None

def get_crypto_price(crypto_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={crypto_id}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[crypto_id]['usd']

def get_historical_price(crypto_id, date):
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/history?date={date}"
    response = requests.get(url)
    data = response.json()
    try:
        return data['market_data']['current_price']['usd']
    except KeyError:
        return None

def add_test_transactions():
    test_transactions = [
        ('Polygon', 'matic-network', 244.862, 130.346, 'buy', 'Bitget', '2023-09-18', 0.5323243296223996),
        ('Polygon', 'matic-network', 227.913, 127.461, 'buy', 'Bitget', '2023-10-01', 0.5592528728067289),
        ('Ethereum', 'ethereum', 0.0188939, 30.77, 'buy', 'Kucoin', '2023-10-21', 1628.567950502543),
        ('Ethereum', 'ethereum', 0.01, 18.17, 'sell', 'Kucoin', '2023-10-25', 1817),
        ('Ethereum', 'ethereum', 0.0199527, 41.47, 'buy', 'Bitget', '2023-11-25', 2078.41545254527)
    ]
    for tx in test_transactions:
        add_transaction(*tx)
        logging.info(f"Added test transaction: {tx}")

def calculate_profit_loss():
    transactions = get_transactions()
    crypto_groups = {}
    for transaction in transactions:
        crypto_id = transaction[2]
        if crypto_id not in crypto_groups:
            crypto_groups[crypto_id] = []
        crypto_groups[crypto_id].append(transaction)

    total_investment = 0
    total_value = 0

    results = []
    for crypto_id, transactions in crypto_groups.items():
        current_price = get_crypto_price(crypto_id)
        investment = 0
        quantity_held = 0
        for transaction in transactions:
            if transaction[5] == 'buy':
                investment += transaction[4]
                quantity_held += transaction[3]
            elif transaction[5] == 'sell':
                investment -= transaction[4]
                quantity_held -= transaction[3]

        current_value = quantity_held * current_price
        total_investment += investment
        total_value += current_value
        profit_loss = current_value - investment
        profit_loss_percent = (profit_loss / investment) * 100 if investment != 0 else 0
        results.append({
            "crypto_id": crypto_id,
            "investment": investment,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percent": profit_loss_percent
        })

    total_profit_loss = total_value - total_investment
    total_profit_loss_percent = (total_profit_loss / total_investment) * 100 if total_investment != 0 else 0
    summary = {
        "total_investment": total_investment,
        "total_value": total_value,
        "total_profit_loss": total_profit_loss,
        "total_profit_loss_percent": total_profit_loss_percent
    }

    return {"details": results, "summary": summary}

@app.route('/transactions', methods=['GET'])
def transactions():
    transactions = get_transactions()
    return jsonify(transactions)

@app.route('/profit_loss', methods=['GET'])
def profit_loss():
    result = calculate_profit_loss()
    return jsonify(result)

@app.route('/transaction', methods=['POST'])
def add_transaction_endpoint():
    data = request.json
    crypto_name = data['crypto_name']
    crypto_id = get_crypto_id(crypto_name)
    if not crypto_id:
        return jsonify({"error": "Cryptocurrency not found"}), 404
    quantity = data['quantity']
    price_usd = data['price_usd']
    transaction_type = data['transaction_type']
    location = data['location']
    date = data['date']
    historical_price = get_historical_price(crypto_id, datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y"))
    if not historical_price:
        historical_price = price_usd / quantity

    add_transaction(crypto_name, crypto_id, quantity, price_usd, transaction_type, location, date, historical_price)
    return jsonify({"message": "Transaction added"}), 201

@app.route('/transaction/<int:transaction_id>', methods=['DELETE'])
def delete_transaction_endpoint(transaction_id):
    delete_transaction(transaction_id)
    return jsonify({"message": "Transaction deleted"}), 200

@app.route('/transaction/<int:transaction_id>', methods=['PUT'])
def update_transaction_endpoint(transaction_id):
    data = request.json
    crypto_name = data['crypto_name']
    crypto_id = get_crypto_id(crypto_name)
    if not crypto_id:
        return jsonify({"error": "Cryptocurrency not found"}), 404
    quantity = data['quantity']
    price_usd = data['price_usd']
    transaction_type = data['transaction_type']
    location = data['location']
    date = data['date']
    historical_price = get_historical_price(crypto_id, datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y"))
    if not historical_price:
        historical_price = price_usd / quantity

    update_transaction(transaction_id, crypto_name, crypto_id, quantity, price_usd, transaction_type, location, date, historical_price)
    return jsonify({"message": "Transaction updated"}), 200

def run_flask_app():
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    if ENABLE_TEST_TRANSACTIONS:
        add_test_transactions()
    run_flask_app()
