from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol
from .const import DOMAIN

class CryptoPortfolioConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Crypto Portfolio."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            return self.async_create_entry(title=user_input["name"], data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("name"): str,
            })
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return CryptoPortfolioOptionsFlowHandler(config_entry)

class CryptoPortfolioOptionsFlowHandler(config_entries.OptionsFlow):
    """Handle an options flow for Crypto Portfolio."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional("option1", default=self.config_entry.options.get("option1", False)): bool,
            })
        )
