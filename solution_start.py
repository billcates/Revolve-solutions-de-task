import argparse
import csv
import json
import os
from collections import defaultdict
from typing import List, Dict
import glob


def load_customers(customers_location: str) -> List[Dict]:
    """
    Load customer data from a CSV file and return a list of dictionaries.
    Each dictionary represents a customer with 'customer_id' and 'loyalty_score' fields.
    """
    customers = []
    with open(customers_location, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            customer_id = row['customer_id']
            customers.append({
                'customer_id': customer_id,
                'loyalty_score': int(row['loyalty_score'])
            })
    return customers


def load_products(products_location: str) -> List[Dict]:
    """
    Load product data from a CSV file and return a list of dictionaries.
    Each dictionary represents a product with 'product_id' and 'product_category' fields.
    """
    products = []
    with open(products_location, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            product_id = row['product_id']
            products.append({
                'product_id': product_id,
                'product_category': row['product_category']
            })
    return products


def get_loyalty_score(customers: List[Dict], customer_id: str) -> int:
    """
    Get the loyalty score for a given customer.
    If the customer is not found, return 0.
    """
    for customer in customers:
        if customer['customer_id'] == customer_id:
            return customer.get('loyalty_score', 0)
    return 0


def get_product_category(products: List[Dict], product_id: str) -> str:
    """
    Get the product category for a given product ID.
    If the product is not found, return an empty string.
    """
    for product in products:
        if product['product_id'] == product_id:
            return product.get('product_category', '')
    return ''


def get_purchase_count(transactions: List[Dict], customer_id: str, product_id: str) -> int:
    """
    Get the purchase count for a given customer ID and product ID.
    Traverse the transactions and count the occurrences of the customer-product combination.
    """
    count = 0
    for transaction in transactions:
        if transaction.get('customer_id') == customer_id:
            basket = transaction.get('basket', [])
            for item in basket:
                if item.get('product_id') == product_id:
                    count += 1
    return count


def load_transactions(transactions_location: str) -> List[Dict]:
    """
    Load transaction data from JSON Lines files in the specified location and return a list of dictionaries.
    Each dictionary represents a transaction with 'customer_id', 'basket', and 'product_id' fields.
    """
    transactions = []
    file_paths = glob.glob(os.path.join(transactions_location, "*", "transactions.json"))
    for file_path in file_paths:
        file_path = file_path.replace('/', '\\')
        with open(file_path, 'r') as f:
            for line in f:
                try:
                    transaction = json.loads(line)
                    basket = transaction.get('basket', [])
                    product_ids = [item.get('product_id') for item in basket]
                    transaction['product_id'] = product_ids
                    transactions.append(transaction)
                except json.JSONDecodeError as e:
                    print(f"Error loading JSON in file {file_path}: {e}")
    return transactions


def process_data(customers: List[Dict], products: List[Dict], transactions: List[Dict]) -> List[Dict]:
    """
    Process the data and generate the output for each customer.
    """
    output_data = []
    for transaction in transactions:
        customer_id = transaction.get('customer_id')
        basket = transaction.get('basket', [])
        if customer_id is not None and basket:
            loyalty_score = get_loyalty_score(customers, customer_id)
            for item in basket:
                product_id = item.get('product_id')
                product_category = get_product_category(products, product_id)
                purchase_count = get_purchase_count(transactions, customer_id, product_id)
                data_entry = {
                    'customer_id': customer_id,
                    'loyalty_score': loyalty_score,
                    'product_id': product_id,
                    'product_category': product_category,
                    'purchase_count': purchase_count
                }
                output_data.append(data_entry)
    return output_data


def save_output(output_data: List[Dict], output_location: str):
    """
    Save the output data as JSON to the specified location.
    """
    os.makedirs(output_location, exist_ok=True)
    output_file = os.path.join(output_location, 'output.json')
    with open(output_file, 'w') as file:
        for data in output_data:
            json_data = json.dumps(data)
            file.write(json_data)
            file.write('\n')


def get_params() -> dict:
    """
    Get the command line arguments as parameters.
    """
    parser = argparse.ArgumentParser(description='DataTest')
    parser.add_argument('--customers_location', required=False, default="./input_data/starter/customers.csv")
    parser.add_argument('--products_location', required=False, default="./input_data/starter/products.csv")
    parser.add_argument('--transactions_location', required=False, default="./input_data/starter/transactions/")
    parser.add_argument('--output_location', required=False, default="./output_data/outputs/")
    return vars(parser.parse_args())


def main():
    params = get_params()

    customers = load_customers(params['customers_location'])
    products = load_products(params['products_location'])
    transactions = load_transactions(params['transactions_location'])
    output_data = process_data(customers, products, transactions)
    save_output(output_data, params['output_location'])


if __name__ == "__main__":
    main()

