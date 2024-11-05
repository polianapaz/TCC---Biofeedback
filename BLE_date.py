import asyncio
from bleak import BleakScanner

async def main():
    target_name = "ESP32 - Poliana - BLE"
    target_address = None

    devices = await BleakScanner.discover()
    for d in devices:
        print(d)
        if target_name == d.name:
            target_address = d.address
            print("found target {} bluetooth device with address {} ".format(target_name,target_address))
            break
asyncio.run(main())