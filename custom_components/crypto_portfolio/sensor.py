import requests
from homeassistant.helpers.entity import Entity

def setup_platform(hass, config, add_entities, discovery_info=None):
    add_entities([CryptoTransactionsSensor(), CryptoProfitLossSensor()])

class CryptoTransactionsSensor(Entity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return 'Crypto Transactions'

    @property
    def state(self):
        return self._state

    def update(self):
        response = requests.get('http://localhost:5000/transactions')
        if response.status_code == 200:
            self._state = len(response.json())

class CryptoProfitLossSensor(Entity):
    def __init__(self):
        self._state = None

    @property
    def name(self):
        return 'Crypto Profit Loss'

    @property
    def state(self):
        return self._state

    def update(self):
        response = requests.get('http://localhost:5000/profit_loss')
        if response.status_code == 200:
            self._state = response.json()['summary']['total_profit_loss']
