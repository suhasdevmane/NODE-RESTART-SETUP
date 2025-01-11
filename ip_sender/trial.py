import requests
import time
import json
import subprocess
import logging

logging.basicConfig(filename='curl_logs.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

def main():
    url = "https://thingsboard.cs.cf.ac.uk/api/auth/login"
    headers = {"Content-Type": "application/json"}

    payload = {"username": "SuhasAbacwsLivingLab@cardiff.ac.uk", "password": "SuhasDevmane"}

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        # Authentication successful
        token = response.json().get("token")
        # print("JWT_Token:", token)
    else:
        logging.error("Authentication failed. Status Code:", response.status_code)
        logging.error("Response:", response.text)

    # Get current timestamp in Unix format with milliseconds
    current_timestamp = int(time.time() * 1000)
    # print("Current timestamp (Unix format with milliseconds):", current_timestamp)
    device_ids = [
        "70ad22a0-b82c-11ed-b196-bb47e24272bc",
        "75d29440-b82c-11ed-b196-bb47e24272bc",
        "7b717ba0-b82c-11ed-b196-bb47e24272bc",
        "a673eb80-b82c-11ed-b196-bb47e24272bc",
        "83456b70-b82c-11ed-b196-bb47e24272bc",
        "b96d6720-b82c-11ed-b196-bb47e24272bc",
        "be98a520-b82c-11ed-b196-bb47e24272bc",
        "c3110de0-b82c-11ed-b196-bb47e24272bc",
        "c950f030-b82c-11ed-b196-bb47e24272bc",
        "cfddba00-b82c-11ed-b196-bb47e24272bc",
        "278505c0-0f7a-11ee-bf90-a16a1a9e1e0a",
        "d9576a90-b82c-11ed-b196-bb47e24272bc",
        "de18ea40-b82c-11ed-b196-bb47e24272bc",
        "f57a1560-7cf3-11ee-94bc-d389020903a3",
        "508d1b60-57eb-11ee-8714-19d56ba0c4fd",
        "86c63bd0-57f0-11ee-8714-19d56ba0c4fd",
        "3efd82d0-7cf4-11ee-94bc-d389020903a3",
        "f583bc50-57e6-11ee-8714-19d56ba0c4fd",
        "9458c560-0f75-11ee-bf90-a16a1a9e1e0a",
        "cbc851c0-57ee-11ee-8714-19d56ba0c4fd",
        "2ae959b0-53c6-11ee-8714-19d56ba0c4fd",
        "351b0eb0-57ef-11ee-8714-19d56ba0c4fd",
        "0f96bed0-b82d-11ed-b196-bb47e24272bc",
        "13e642d0-b82d-11ed-b196-bb47e24272bc",
        "18a159e0-b82d-11ed-b196-bb47e24272bc",
        "fef50770-57f1-11ee-8714-19d56ba0c4fd",
        "2a5d9a90-b82d-11ed-b196-bb47e24272bc",
        "99c6a3b0-b82b-11ed-b196-bb47e24272bc",
        "51f2d170-57e1-11ee-8714-19d56ba0c4fd",
        "9c563630-0f75-11ee-bf90-a16a1a9e1e0a",
        "391303e0-b82d-11ed-b196-bb47e24272bc",
        "3d3a3f60-b82d-11ed-b196-bb47e24272bc",
        "a83a46c0-7cf4-11ee-94bc-d389020903a3",
        "4665a8e0-b82d-11ed-b196-bb47e24272bc",
    ]
    access_token = token

    key_to_fetch = ["ip_address"]
    base_url = "https://thingsboard.cs.cf.ac.uk/api/plugins/telemetry/DEVICE"

    # List to store responses for each device
    all_responses = []

    for device_id in device_ids:
        url = f"{base_url}/{device_id}/values/timeseries?keys={','.join(key_to_fetch)}"
        headers = {
            "Content-Type": "application/json",
            "X-Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            all_responses.append(data)
        else:
            logging.error(
                f"Failed to get data for device {device_id}. Status Code: {response.status_code}"
            )
            logging.error(response.text)

    def analyze_timestamps(data):
        current_timestamp = (
            int(time.time() * 1000)
        )  # Get current timestamp in milliseconds
        results = []

        for device_data in data:
            ip_address_info = device_data.get("ip_address", [])
            for info in ip_address_info:
                ts = info.get("ts", 0)
                value = info.get("value")

                time_diff = (
                    current_timestamp - ts
                ) / 1000  # Convert milliseconds to seconds

                status = "yes" if time_diff > 60 else "no"
                if value is None:
                    status = "no"

                result = {
                    "value": value,
                    "ts": ts,
                    "current-ts": current_timestamp,
                    "status": status,
                }
                results.append(result)

                if status == "yes":
                    ip_address = result["value"]
                    # Log message before executing curl command
                    logging.info(f"Curl command executed for IP address: {ip_address}")
                    subprocess.run(
                        [
                            "curl",
                            "-X",
                            "POST",
                            "-H",
                            "Content-Type: application/json",
                            "-d",
                            f'{{"ip_address":"{ip_address}"}}',
                            "http://localhost:5000/device_activity",
                        ]
                    )

        return results

    results = analyze_timestamps(all_responses)
    for result in results:
        print(result)

if __name__ == "__main__":
    while True:
        main()
        time.sleep(15)
