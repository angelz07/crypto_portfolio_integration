import requests
from homeassistant.helpers.entity import Entity

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensor platform."""
    # You can add more sensors if needed
    async_add_entities([CryptoTransactionsSensor(), CryptoProfitLossSensor()])

class CryptoTransactionsSensor(Entity):
    def __init__(self):
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return 'Crypto Transactions'

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        response = requests.get('http://localhost:5000/transactions')
        if response.status_code == 200:
            transactions = response.json()
            self._state = len(transactions)
            self._attributes['transactions'] = transactions

class CryptoProfitLossSensor(Entity):
    def __init__(self):
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return 'Crypto Profit Loss'

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    async def async_update(self):
        response = requests.get('http://localhost:5000/profit_loss')
        if response.status_code == 200:
            result = response.json()
            self._state = result['summary']['total_profit_loss']
            self._attributes['details'] = result['details']
