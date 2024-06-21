import logging
import requests
from homeassistant.helpers.entity import Entity

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup sensor platform."""
    async_add_entities([
        CryptoTransactionsSensor(hass, config_entry.entry_id),
        TotalInvestmentSensor(hass, config_entry.entry_id),
        TotalValueSensor(hass, config_entry.entry_id),
        TotalProfitLossSensor(hass, config_entry.entry_id),
        TotalProfitLossPercentSensor(hass, config_entry.entry_id)
    ])

    # Add individual crypto sensors
    response = await hass.async_add_executor_job(
        requests.get, 'http://localhost:5000/profit_loss'
    )
    if response.status_code == 200:
        data = response.json()
        for detail in data['details']:
            async_add_entities([
                CryptoInvestmentSensor(hass, config_entry.entry_id, detail),
                CryptoCurrentValueSensor(hass, config_entry.entry_id, detail),
                CryptoProfitLossDetailSensor(hass, config_entry.entry_id, detail),
                CryptoProfitLossPercentDetailSensor(hass, config_entry.entry_id, detail)
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



# Define additional sensor classes
class TotalInvestmentSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Total Investment'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_total_investment"

    async def async_update(self):
        _LOGGER.debug("Updating Total Investment Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/profit_loss'
            )
            if response.status_code == 200:
                data = response.json()
                self._state = data['summary']['total_investment']
                _LOGGER.debug(f"Total Investment Sensor updated: {self._state}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in TotalInvestmentSensor: {e}")

class TotalValueSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Total Value'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_total_value"

    async def async_update(self):
        _LOGGER.debug("Updating Total Value Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/profit_loss'
            )
            if response.status_code == 200:
                data = response.json()
                self._state = data['summary']['total_value']
                _LOGGER.debug(f"Total Value Sensor updated: {self._state}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in TotalValueSensor: {e}")

class TotalProfitLossSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Total Profit Loss'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_total_profit_loss"

    async def async_update(self):
        _LOGGER.debug("Updating Total Profit Loss Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/profit_loss'
            )
            if response.status_code == 200:
                data = response.json()
                self._state = data['summary']['total_profit_loss']
                _LOGGER.debug(f"Total Profit Loss Sensor updated: {self._state}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in TotalProfitLossSensor: {e}")

class TotalProfitLossPercentSensor(Entity):
    def __init__(self, hass, entry_id):
        self._state = None
        self.hass = hass
        self._entry_id = entry_id

    @property
    def name(self):
        return 'Total Profit Loss Percent'

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_total_profit_loss_percent"

    async def async_update(self):
        _LOGGER.debug("Updating Total Profit Loss Percent Sensor")
        try:
            response = await self.hass.async_add_executor_job(
                requests.get, 'http://localhost:5000/profit_loss'
            )
            if response.status_code == 200:
                data = response.json()
                self._state = data['summary']['total_profit_loss_percent']
                _LOGGER.debug(f"Total Profit Loss Percent Sensor updated: {self._state}")
            else:
                _LOGGER.error(f"Error fetching data: {response.status_code}")
        except Exception as e:
            _LOGGER.error(f"Exception in TotalProfitLossPercentSensor: {e}")

# Individual Crypto Sensors
class CryptoInvestmentSensor(Entity):
    def __init__(self, hass, entry_id, detail):
        self._state = detail['investment']
        self._attributes = detail
        self.hass = hass
        self._entry_id = entry_id
        self._crypto_id = detail['crypto_id']

    @property
    def name(self):
        return f"Investment {self._crypto_id}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_{self._crypto_id}_investment"

    @property
    def extra_state_attributes(self):
        return self._attributes

class CryptoCurrentValueSensor(Entity):
    def __init__(self, hass, entry_id, detail):
        self._state = detail['current_value']
        self._attributes = detail
        self.hass = hass
        self._entry_id = entry_id
        self._crypto_id = detail['crypto_id']

    @property
    def name(self):
        return f"Current Value {self._crypto_id}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_{self._crypto_id}_current_value"

    @property
    def extra_state_attributes(self):
        return self._attributes

class CryptoProfitLossDetailSensor(Entity):
    def __init__(self, hass, entry_id, detail):
        self._state = detail['profit_loss']
        self._attributes = detail
        self.hass = hass
        self._entry_id = entry_id
        self._crypto_id = detail['crypto_id']

    @property
    def name(self):
        return f"Profit Loss {self._crypto_id}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_{self._crypto_id}_profit_loss"

    @property
    def extra_state_attributes(self):
        return self._attributes

class CryptoProfitLossPercentDetailSensor(Entity):
    def __init__(self, hass, entry_id, detail):
        self._state = detail['profit_loss_percent']
        self._attributes = detail
        self.hass = hass
        self._entry_id = entry_id
        self._crypto_id = detail['crypto_id']

    @property
    def name(self):
        return f"Profit Loss Percent {self._crypto_id}"

    @property
    def state(self):
        return self._state

    @property
    def unique_id(self):
        return f"{self._entry_id}_{self._crypto_id}_profit_loss_percent"

    @property
    def extra_state_attributes(self):
        return self._attributes
