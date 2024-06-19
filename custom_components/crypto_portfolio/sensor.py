import logging
import requests
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensor platform."""
    async_add_entities([CryptoTransactionsSensor(hass), CryptoProfitLossSensor(hass)])

class CryptoTransactionsSensor(Entity):
    def __init__(self, hass):
        self._state = None
        self._attributes = {}
        self.hass = hass

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
        _LOGGER.debug("Updating Crypto Transactions Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/transactions'
            )
            if response.status_code == 200:
                transactions = response.json()
                self._state = len(transactions)
                self._attributes['transactions'] = transactions
                _LOGGER.debug(f"Transactions: {transactions}")
            else:
                _LOGGER.error(f"Error fetching transactions: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in CryptoTransactionsSensor: {e}")

class CryptoProfitLossSensor(Entity):
    def __init__(self, hass):
        self._state = None
        self._attributes = {}
        self.hass = hass

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
        _LOGGER.debug("Updating Crypto Profit Loss Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/profit_loss'
            )
            if response.status_code == 200:
                result = response.json()
                self._state = result['summary']['total_profit_loss']
                self._attributes['details'] = result['details']
                _LOGGER.debug(f"Profit/Loss Summary: {result['summary']}")
                _LOGGER.debug(f"Profit/Loss Details: {result['details']}")
            else:
                _LOGGER.error(f"Error fetching profit/loss: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in CryptoProfitLossSensor: {e}")
