# WCtoSS (WooCommerce to ShipStation)

WCtoSS is a Python-based tool that automates the process of fetching orders from WooCommerce and submitting them to ShipStation. This integration streamlines the order fulfillment process for e-commerce businesses using WooCommerce as their platform and ShipStation for shipping management.

## Features

- Fetches processing orders from WooCommerce
- Converts WooCommerce orders to ShipStation format
- Submits orders to ShipStation
- Supports custom fields and advanced options
- Debug mode for both WooCommerce and ShipStation operations

## Prerequisites

- Python 3.7+
- WooCommerce store with API access
- ShipStation account with API access

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/EccentricWkshp/WCtoSS.git
   cd WCtoSS
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

1. Copy the `config.json.example` file to `config.json`:
   ```
   cp config.json.example config.json
   ```

2. Edit `config.json` and fill in your WooCommerce and ShipStation API credentials:
   ```json
   {
     "woocommerce": {
       "store_url": "https://your-store-url.com",
       "consumer_key": "your_consumer_key",
       "consumer_secret": "your_consumer_secret"
     },
     "shipstation": {
       "api_key": "your_api_key",
       "api_secret": "your_api_secret",
       "WCstoreID": "your_woocommerce_store_id_in_shipstation"
     },
     "SS_Submit_Orders": false,
     "SS_Debug": false,
     "WC_Debug": false
   }
   ```

   Note: Set `SS_Submit_Orders` to `true` when you're ready to actually submit orders to ShipStation.

## Usage

Run the main script:

```
python WCtoSS.py
```

This will fetch processing orders from WooCommerce, convert them to ShipStation format, and either submit them to ShipStation (if `SS_Submit_Orders` is `true`) or simulate the submission (if `false`).

## Debugging

To enable debug output:

1. Set `"SS_Debug": true` in `config.json` for ShipStation debugging.
2. Set `"WC_Debug": true` in `config.json` for WooCommerce debugging.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

## Disclaimer

This tool is not officially affiliated with or endorsed by WooCommerce or ShipStation. Use at your own risk.

## Support

If you encounter any problems or have any questions, please open an issue in this repository.
