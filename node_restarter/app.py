from flask import Flask, request, jsonify
from tapo import ApiClient
import asyncio

app = Flask(__name__)

async def restart_device(ip_address):
    client = ApiClient("suhasdevmanecardiffuni@gmail.com", "Suhas@551993")
    device = await client.p110(ip_address)

    print(f"Restarting device at IP address {ip_address}...")
    await device.off()
    await asyncio.sleep(10)
    await device.on()
    print(f"Device at IP address {ip_address} restarted")

@app.route('/device_activity', methods=['POST'])
def device_activity():
    data = request.json
    print("Received data:", data)
    
    # Extract relevant information from the request data
    device_id = data.get('device_id')
    device_status = data.get('device_status')
    ip_address = data.get('ip_address')
    
    if device_status == 'inactive':
        # If device is inactive, restart the device
        asyncio.run(restart_device(ip_address))
        
        # Respond with a success message
        return jsonify({'message': f'Device {device_id} restarted at {ip_address}'}), 200
    else:
        # If device is active, respond with a success message
        return jsonify({'message': f'Device {device_id} is active'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
