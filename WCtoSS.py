import json
from woocomm import get_woocommerce_orders
from ShipStation import ShipStation, ShipStationOrder, ShipStationAddress, ShipStationItem, ShipStationWeight, ShipStationContainer, ShipStationAdvancedOptions
import pycountry_convert as pcc
import pycountry
import sys

# Load the configuration file
try:
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
except json.JSONDecodeError as e:
    print(f"Error parsing config.json: {e}")
    print("Please check the format of your config.json file.")
    sys.exit(1)
except FileNotFoundError:
    print("config.json file not found. Please make sure it exists in the current directory.")
    sys.exit(1)

# Initialize ShipStation client
ss = ShipStation(key=config['shipstation']['api_key'], secret=config['shipstation']['api_secret'])
SS_Submit_Orders = config['SS_Submit_Orders']
ss.debug = config['SS_Debug']

def get_woocommerce_store_id():
    if config['shipstation']['WCstoreID']:
        return config['shipstation']['WCstoreID']
    else:
        # Fetch stores from ShipStation
        ss_stores = ss.fetch_stores().json()
        for store in ss_stores:
            if store['storeName'] == 'WooCommerce':
                return store['storeId']
        print("Error: WooCommerce store not found in ShipStation.")
        return None

# Get WooCommerce store ID
WC_store_id = get_woocommerce_store_id()
if WC_store_id is None:
    print("Cannot proceed without a valid WooCommerce store ID.")
    exit(1)

def convert_country_name_to_code(country):
    if len(country) == 2 and country.isalpha():
        return country.upper()  # It's already a country code
    try:
        country_obj = pycountry.countries.search_fuzzy(country)
        return country_obj[0].alpha_2
    except LookupError:
        print(f"Warning: Could not convert country '{country}' to country code.")
        return country

def wc_address_to_ss_address(wc_address):
    return ShipStationAddress(
        name=f"{wc_address.first_name} {wc_address.last_name}",
        company=None,  # WooCommerce address doesn't have a company field
        street1=wc_address.address_1,
        street2=wc_address.address_2,
        city=wc_address.city,
        state=wc_address.state,
        postal_code=wc_address.postcode,
        country=convert_country_name_to_code(wc_address.country),
        phone=wc_address.phone,
        residential=None
    )

def wc_item_to_ss_item(wc_item):
    ss_item = ShipStationItem(
        sku=wc_item.sku,
        name=wc_item.name,
        quantity=wc_item.quantity,
        unit_price=wc_item.price
    )
    ss_item.set_weight(ShipStationWeight(units='ounces', value='3'))  # Default weight, adjust as needed
    return ss_item

def wc_order_to_ss_order(wc_order):
    ss_order = ShipStationOrder(order_number=wc_order.order_number)
    ss_order.order_date = wc_order.order_date
    ss_order.payment_date = wc_order.order_date  # Assuming payment date is the same as order date
    ss_order.order_status = 'awaiting_shipment'
    ss_order.customer_username = f"{wc_order.billing_address.first_name} {wc_order.billing_address.last_name}"
    ss_order.customer_email = wc_order.billing_address.email
    ss_order.amount_paid = wc_order.total
    ss_order.tax_amount = wc_order.tax_amount
    ss_order.shipping_amount = wc_order.shipping_amount
    ss_order.customer_notes = wc_order.customer_notes
    ss_order.payment_method = wc_order.payment_method

    ss_order.set_billing_address(wc_address_to_ss_address(wc_order.billing_address))
    ss_order.set_shipping_address(wc_address_to_ss_address(wc_order.shipping_address))

    for wc_item in wc_order.items:
        ss_order.add_item(wc_item_to_ss_item(wc_item))

    ss_order.set_dimensions(ShipStationContainer(units='inches', length='12', width='12', height='12'))

    advanced_options = ShipStationAdvancedOptions(
        billToAccount='',
        billToCountryCode='',
        billToMyOtherAccount='',
        billToParty='',
        billToPostalCode='',
        containsAlcohol='False',
        customField1=wc_order.advanced_options.get('custom_field1', ''),
        customField2=wc_order.advanced_options.get('custom_field2', ''),
        customField3=wc_order.advanced_options.get('custom_field3', ''),
        mergedIds='',
        mergedOrSplit='False',
        nonMachinable='False',
        parentID='',
        saturdayDelivery='False',
        source='WooCommerce',
        storeID=WC_store_id,
        warehouseId=''
    )
    ss_order.set_advanced_options(advanced_options)

    return ss_order

def main():
    wc_orders = get_woocommerce_orders()
    if wc_orders is None:
        print("Failed to retrieve orders from WooCommerce.")
        return

    for wc_order in wc_orders:
        ss_order = wc_order_to_ss_order(wc_order)
        ss.add_order(ss_order)

    if SS_Submit_Orders:
        print("Submitting orders to ShipStation...")
        ss.submit_orders()
        print(f"Submitted {len(wc_orders)} orders to ShipStation.")
    else:
        print(f"Configured to not submit orders. {len(wc_orders)} orders processed but not submitted.")

if __name__ == "__main__":
    main()