import logging
import requests
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensor platform."""
    async_add_entities([
        CryptoTransactionsSensor(hass, config_entry.entry_id),
        CryptoProfitLossSensor(hass, config_entry.entry_id)
    ])

class CryptoTransactionsSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self._attributes = {}
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Crypto Transactions'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_crypto_transactions"

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
                data = response.json()
                self._state = len(data)
                self._attributes = {"transactions": data}
                _LOGGER.debug(f"Crypto Transactions Sensor updated: {data}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in CryptoTransactionsSensor: {e}")

class CryptoProfitLossSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self._attributes = {}
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Crypto Profit Loss'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_crypto_profit_loss"

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
                data = response.json()
                self._state = data['summary']['total_profit_loss']
                self._attributes = data
                _LOGGER.debug(f"Crypto Profit Loss Sensor updated: {data}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in CryptoProfitLossSensor: {e}")
