import logging
from flask import Flask, jsonify, request
import threading
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType
from .db import create_table, add_transaction, get_transactions, delete_transaction, update_transaction, get_crypto_transactions
from .crypto_portfolio import get_crypto_id, get_crypto_price, get_historical_price, calculate_profit_loss
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

app = Flask(__name__)

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

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    create_table()
    thread = threading.Thread(target=run_flask_app)
    thread.start()
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "sensor")
    )
    return await async_setup(hass, entry.data)
