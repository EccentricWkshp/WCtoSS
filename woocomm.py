import json
from woocommerce import API

# Load the configuration file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Retrieve configuration values
store_url = config['woocommerce']['store_url']
consumer_key = config['woocommerce']['consumer_key']
consumer_secret = config['woocommerce']['consumer_secret']
WC_Debug = config['WC_Debug']

# Initialize the WooCommerce API client
wcapi = API(
    url=store_url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    version="wc/v3"
)

# Define the WooCommerce Address class
class WooCommerce_Address:
    def __init__(self, first_name, last_name, address_1, address_2, city, state, postcode, country, phone, email):
        self.first_name = first_name
        self.last_name = last_name
        self.address_1 = address_1
        self.address_2 = address_2
        self.city = city
        self.state = state
        self.postcode = postcode
        self.country = country
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.address_1}, {self.address_2}, {self.city}, {self.state}, {self.postcode}, {self.country}, {self.phone}, {self.email}"

# Define the WooCommerce Item class
class WooCommerce_Item:
    def __init__(self, product_id, sku, name, quantity, price):
        self.product_id = product_id
        self.sku = sku
        self.name = name
        self.quantity = quantity
        self.price = price

    def __str__(self):
        return f"Product ID: {self.product_id}, SKU: {self.sku}, Name: {self.name}, Quantity: {self.quantity}, Price: {self.price}"

# Define the WooCommerce Order class
class WooCommerce_Order:
    def __init__(self, order_id, order_number, order_date, status, billing_address, shipping_address, items, total, shipping_amount, tax_amount, customer_notes=None, internal_notes=None, gift=None, gift_message=None, payment_method=None, requested_shipping_service=None, carrier_code=None, service_code=None, package_code=None, confirmation=None, advanced_options=None):
        self.order_id = order_id
        self.order_number = order_number
        self.order_date = order_date
        self.status = status
        self.billing_address = billing_address
        self.shipping_address = shipping_address
        self.items = items
        self.total = total
        self.shipping_amount = shipping_amount
        self.tax_amount = tax_amount
        self.customer_notes = customer_notes
        self.internal_notes = internal_notes
        self.gift = gift
        self.gift_message = gift_message
        self.payment_method = payment_method
        self.requested_shipping_service = requested_shipping_service
        self.carrier_code = carrier_code
        self.service_code = service_code
        self.package_code = package_code
        self.confirmation = confirmation
        self.advanced_options = advanced_options

    def __str__(self):
        return f"Order ID: {self.order_id}, Order Number: {self.order_number}, Order Date: {self.order_date}, Status: {self.status}, Total: {self.total}, Shipping Amount: {self.shipping_amount}, Tax Amount: {self.tax_amount}"

# Helper function to extract custom fields from meta data
def get_custom_field(meta_data, key):
    for meta in meta_data:
        if meta['key'] == key:
            return meta['value']
    return None

# Function to get orders from WooCommerce
def get_woocommerce_orders():
    if WC_Debug:
        print("Fetching orders from WooCommerce...")
    
    response = wcapi.get("orders", params={"status": "processing"})
    
    if WC_Debug:
        print(f"WooCommerce API Response Status: {response.status_code}")
    
    if response.status_code == 200:
        orders = response.json()
        
        if WC_Debug:
            print(f"Retrieved {len(orders)} orders from WooCommerce")
        
        woocommerce_order_objects = []
        for order in orders:
            if WC_Debug:
                print(f"Processing order {order['id']}...")
            
            billing_address = WooCommerce_Address(
                first_name=order['billing']['first_name'],
                last_name=order['billing']['last_name'],
                address_1=order['billing']['address_1'],
                address_2=order['billing']['address_2'],
                city=order['billing']['city'],
                state=order['billing']['state'],
                postcode=order['billing']['postcode'],
                country=order['billing']['country'],
                phone=order['billing']['phone'],
                email=order['billing']['email']
            )
            shipping_address = WooCommerce_Address(
                first_name=order['shipping']['first_name'],
                last_name=order['shipping']['last_name'],
                address_1=order['shipping']['address_1'],
                address_2=order['shipping']['address_2'],
                city=order['shipping']['city'],
                state=order['shipping']['state'],
                postcode=order['shipping']['postcode'],
                country=order['shipping']['country'],
                phone=None,  # Assuming phone is not part of shipping address in WooCommerce
                email=None   # Assuming email is not part of shipping address in WooCommerce
            )
            items = [
                WooCommerce_Item(
                    product_id=item['product_id'],
                    sku=item.get('sku', ''),
                    name=item['name'],
                    quantity=item['quantity'],
                    price=item['price']
                ) for item in order['line_items']
            ]
            advanced_options = {
                'custom_field1': get_custom_field(order['meta_data'], '_custom_field1'),
                'custom_field2': get_custom_field(order['meta_data'], '_custom_field2'),
                'custom_field3': get_custom_field(order['meta_data'], '_custom_field3')
            }
            woocommerce_order = WooCommerce_Order(
                order_id=order['id'],
                order_number=order['number'],
                order_date=order['date_created'],
                status=order['status'],
                billing_address=billing_address,
                shipping_address=shipping_address,
                items=items,
                total=order['total'],
                shipping_amount=order['shipping_total'],
                tax_amount=order['total_tax'],
                customer_notes=order['customer_note'],
                internal_notes=None,
                gift=None,
                gift_message=None,
                payment_method=order['payment_method'],
                requested_shipping_service=None,
                carrier_code=None,
                service_code=None,
                package_code=None,
                confirmation=None,
                advanced_options=advanced_options
            )
            woocommerce_order_objects.append(woocommerce_order)
            
            if WC_Debug:
                print(f"Processed order {order['id']}")
        
        if WC_Debug:
            print(f"Finished processing {len(woocommerce_order_objects)} orders")
        
        return woocommerce_order_objects
    else:
        print(f"Failed to retrieve orders from WooCommerce. Status code: {response.status_code}, Error: {response.text}")
        return None

if __name__ == "__main__":
    # This will only run if the script is executed directly, not when imported
    woocommerce_orders = get_woocommerce_orders()
    if woocommerce_orders:
        for order in woocommerce_orders:
            print(order)
            if WC_Debug:
                print(f"Billing Address: {order.billing_address}")
                print(f"Shipping Address: {order.shipping_address}")
                for item in order.items:
                    print(f"Item: {item}")
                print(f"Advanced Options: {order.advanced_options}")
                print("---")