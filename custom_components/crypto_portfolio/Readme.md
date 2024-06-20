# Crypto Portfolio Integration for Home Assistant

![Logo](img/logo.png)

## Overview
This integration allows you to track and manage your cryptocurrency portfolio within Home Assistant. You can view your total investment, current value, and profit/loss for each cryptocurrency you hold.

## Installation

1. **Download the integration**:
   - Clone this repository or download the ZIP file.

2. **Add to Home Assistant**:
   - Place the `crypto_portfolio` directory in your `custom_components` directory of your Home Assistant configuration.

3. **Configure the integration**:
   - Go to Configuration > Integrations in the Home Assistant UI.
   - Click on "Add Integration" and search for "Crypto Portfolio".
   - Follow the instructions to set up the integration.

## Features

- **Total Investment**: Displays the total amount of money invested in your cryptocurrencies.
- **Total Profit/Loss**: Shows the overall profit or loss of your investments in USD and percentage.
- **Individual Crypto Sensors**: Provides detailed information for each cryptocurrency, including investment, current value, profit/loss, and profit/loss percentage.

## Usage

You can use the following services to add, update, or delete transactions:

- `crypto_portfolio.add_transaction`
- `crypto_portfolio.update_transaction`
- `crypto_portfolio.delete_transaction`

Refer to the Home Assistant documentation for more details on how to use services in your automations and scripts.

## Support

If you encounter any issues or have questions, please open an issue on the [GitHub repository](https://github.com/angelz07/crypto_portfolio).
