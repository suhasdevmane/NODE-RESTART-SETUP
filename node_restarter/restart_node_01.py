from tapo import ApiClient
import asyncio

async def main():
    client = ApiClient("suhasdevmanecardiffuni@gmail.com", "Suhas@551993")
    device = await client.p110("10.10.227.56")

    print("Turning device off...")
    await device.off()
    print("Waiting 5 seconds...")
    await asyncio.sleep(5)
    print("Turning device on...")
    await device.on()
    print("Device Restarted")

# Run the main function
asyncio.run(main())
