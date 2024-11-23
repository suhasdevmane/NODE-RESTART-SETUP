from tapo import ApiClient
import asyncio

async def restart_device(ip_address):
    client = ApiClient("suhasdevmanecardiffuni@gmail.com", "Suhas@551993")
    device = await client.p110(ip_address)

    print(f"Restarting device at IP address {ip_address}...")
    await device.off()
    await asyncio.sleep(10)
    await device.on()
    print(f"Device at IP address {ip_address} restarted")

# You can call this function with the IP address of the device that sent the inactivity status
async def main(ip_address):
    await restart_device(ip_address)

# Example usage
asyncio.run(main("10.10.129.71"))  # Replace with the appropriate IP address
