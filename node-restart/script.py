# script.py

import requests
import time
import json
import subprocess
import logging
import os
from flask import Flask, render_template_string, render_template

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # This will print logs to the console (terminal)
        logging.FileHandler("curl_logs.txt")  # This will save logs to the file
    ]
)
# logging.info("This is an info log")
# logging.error("This is an error log")

app = Flask(__name__)

@app.route('/')
def serve_logs():
    # Read logs from curl_logs.txt file
    with open("curl_logs.txt", "r") as f:
        logs = f.readlines()

    # Display the latest 50 logs
    logs = logs[-50:][::-1]
    return render_template("logs.html", logs=logs)
    

def main():
    
    # print("Current timestamp (Unix format with milliseconds):", current_timestamp)
    device_ids = {
        "70ad22a0-b82c-11ed-b196-bb47e24272bc":"10.10.129.71",	
        "75d29440-b82c-11ed-b196-bb47e24272bc":"10.10.129.72",
        "a673eb80-b82c-11ed-b196-bb47e24272bc":"10.10.129.74",
        "83456b70-b82c-11ed-b196-bb47e24272bc":"10.10.129.75",
        "b96d6720-b82c-11ed-b196-bb47e24272bc":"10.10.129.76",	
        "be98a520-b82c-11ed-b196-bb47e24272bc":"10.10.129.77",
        "c3110de0-b82c-11ed-b196-bb47e24272bc":"10.10.129.78",	
        "c950f030-b82c-11ed-b196-bb47e24272bc":"10.10.129.79",
        "cfddba00-b82c-11ed-b196-bb47e24272bc":"10.10.129.80",
        "278505c0-0f7a-11ee-bf90-a16a1a9e1e0a":"10.10.129.73",
        "d9576a90-b82c-11ed-b196-bb47e24272bc":"10.10.129.81",
        "de18ea40-b82c-11ed-b196-bb47e24272bc":"10.10.129.82",
        "f57a1560-7cf3-11ee-94bc-d389020903a3":"10.10.129.83",
        "508d1b60-57eb-11ee-8714-19d56ba0c4fd":"10.10.129.84",
        "86c63bd0-57f0-11ee-8714-19d56ba0c4fd":"10.10.129.85",
        "3efd82d0-7cf4-11ee-94bc-d389020903a3":"10.10.129.86",
        "f583bc50-57e6-11ee-8714-19d56ba0c4fd":"10.10.129.87",
        "9458c560-0f75-11ee-bf90-a16a1a9e1e0a":"10.10.129.88",
        "2ae959b0-53c6-11ee-8714-19d56ba0c4fd":"10.10.129.89",	                        
        # # "351b0eb0-57ef-11ee-8714-19d56ba0c4fd":"10.10.129.90",   
        "0f96bed0-b82d-11ed-b196-bb47e24272bc":"10.10.129.91",
        "13e642d0-b82d-11ed-b196-bb47e24272bc":"10.10.129.92",
        "18a159e0-b82d-11ed-b196-bb47e24272bc":"10.10.129.93",
        "fef50770-57f1-11ee-8714-19d56ba0c4fd":"10.10.129.94",
        "2a5d9a90-b82d-11ed-b196-bb47e24272bc":"10.10.129.95",
        "99c6a3b0-b82b-11ed-b196-bb47e24272bc":"10.10.129.96",
        "51f2d170-57e1-11ee-8714-19d56ba0c4fd":"10.10.129.97",
        "9c563630-0f75-11ee-bf90-a16a1a9e1e0a":"10.10.129.100",
        "391303e0-b82d-11ed-b196-bb47e24272bc":"10.10.129.98",
        "3d3a3f60-b82d-11ed-b196-bb47e24272bc":"10.10.129.99",
        "4665a8e0-b82d-11ed-b196-bb47e24272bc":"10.10.129.101",
        "b9cb09a0-11ec-11ef-b56b-a96a8be1c6f5":"10.10.129.102"
    }


    
    while True:
        url = "https://thingsboard.cs.cf.ac.uk/api/auth/login"
        headers = {"Content-Type": "application/json"}

        payload = {
            "username": "SuhasAbacwsLivingLab@cardiff.ac.uk",
            "password": "SuhasDevmane",
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            token = response.json().get("token")
            print("token received successfully: ", token)
            if not token:
                logging.error("Authentication failed: No token returned.")
                print("error fetching the token.")
                return
        else:
            logging.error(f"Authentication failed. Status Code: {response.status_code}")
            print("Authentication failed.")
            logging.error(f"Response: {response.text}")
            return

        # Get current timestamp in Unix format with milliseconds
        current_timestamp = int(time.time() * 1000)

        access_token = token
        key_to_fetch = ["ip_address"]
        print("key_to_fetch", key_to_fetch)
        base_url = "https://thingsboard.cs.cf.ac.uk/api/plugins/telemetry/DEVICE"
        for device_id, ip in device_ids.items():
            url2 = f"{base_url}/{device_id}/values/timeseries?keys={','.join(key_to_fetch)}"
            headers = {
                "Content-Type": "application/json",
                "X-Authorization": f"Bearer {access_token}",
            }
            response = requests.get(url2, headers=headers)
            print("response: ", response)
            if response.status_code == 200:
                data = response.json()
                print("data: ", data)
            else:
                print("Failed to get data for device data")
                logging.error(
                    f"Failed to get data for device {device_id}. Status Code: {response.status_code}"
                )
                logging.error(response.text)
                continue
            current_timestamp = int(
                time.time() * 1000
            )  # Get current timestamp in milliseconds
            results = []
            # Iterate over the list associated with the key "ip_address"
            for ip_info in data.get("ip_address", []):
                # Access the 'ts' and 'value' keys for each dictionary in the list
                ts = ip_info.get("ts", 0)
                print("received ts:", ts)
                value = ip_info.get("value")
                print("received value: ", value)
                # print("Timestamp:", ts)
                # print("Value:", value)
                time_diff = (
                    current_timestamp - ts
                ) / 1000  # Convert milliseconds to seconds

                status = "inactive" if time_diff > 300 else "no"
                print("status: ", status)
                if value is None:
                    status = "active"

                result = {
                    "value": value,
                    "ts": ts,
                    "current-ts": current_timestamp,
                    "status": status,
                    "ip_address" : ip
                }
                results.append(result)
                print(results)
            for result in results:
                if result["status"] == "inactive":
                    ip_address = result["ip_address"]
                    print( "ip_address value", ip_address)
                    url3 = "http://node_restarter:6000/device_activity"
                    # url = "http://localhost:6000/device_activity"
                    payload = {
                           "ip_address": ip_address,
                            "device_id" : device_id,
                            "device_status" : status

                        }  # Removed unnecessary curly braces around ip_address
                    print("Sending data to endpoint:", payload) 
                    headers = {
                            "Content-Type": "application/json"
                        }  # Assuming you have headers defined somewhere
                    response = requests.post(url3, json=payload, headers=headers)
                    print("Response from server:", response.text)
                    time.sleep(20)
                    print(f"Sensor node was offline with {ip_address} and restarted")
                    logging.info(f"Device {device_id}with IP address {ip_address} is restarted")
        time.sleep(21600)            

def run_flask():
    # Start the Flask application with Gunicorn
    subprocess.run([
        "gunicorn",
        "-b", "0.0.0.0:6001",
        "script:app",
        "--timeout", "240",
        "--workers", "3"
    ])


if __name__ == "__main__":
    # Create a thread to run the Flask application
    import threading
    
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
    
    # Schedule the main task to run every 6 hours
    # schedule_task()
    
    # Keep the script running
    while True:
        main()
