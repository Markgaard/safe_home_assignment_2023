import requests
import csv
import os

export_folder = "export"  # export the csv file into the export folder
os.makedirs(export_folder, exist_ok=True)  # creates the folder in case it is not there

s_rq = "https://safe-transaction-mainnet.safe.global/api/v1/safes/0xBbA4C8eB57DF16c4CfAbe4e9A3Ab697A3e0C65D8/multisig-transactions/"  # s_ for Safe
walletconnect_txns_count = []

try:
    response = requests.get(s_rq)
    response.raise_for_status()  # checks for https errors

    s_data = response.json()  # data format

    for transaction in s_data.get("results", []):
        origin = transaction.get("origin", "")  # fetch all transactions with WalletConnect as the origin
        if "WalletConnect" in origin:
            safe = transaction.get("safe", "")  # safe address
            to = transaction.get("to", "")  # destination address
            transaction_hash = transaction.get("transactionHash", "")  # fetch the transaction hash
            execution_date = transaction.get("executionDate", "")  # fetch the execution date
            walletconnect_txns_count.append({
                "safe": safe,
                "to": to,
                "transaction_hash": transaction_hash,
                "execution_date": execution_date
            })

    print(f"Count of transactions originating from WalletConnect: {len(walletconnect_txns_count)}")

    safe_txns_exp = os.path.join(export_folder, "safe_walletconnect_transactions.csv") # create and export csv file with the results
    with open(safe_txns_exp, "w", newline="") as csv_file:
        fieldnames = ["safe_address", "to", "transaction_hash", "execution_date"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()  # csv header

        for idx, tx in enumerate(walletconnect_txns_count, start=1):
            writer.writerow({
                "safe_address": tx["safe"],
                "to": tx["to"],
                "transaction_hash": tx["transaction_hash"],
                "execution_date": tx["execution_date"]
            })

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
except ValueError as e:
    print(f"Error parsing JSON response: {e}")