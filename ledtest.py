import asyncio
from bleak import BleakClient

address = "22:74:47:27:58:7D"
writeUUID = "0000fff3-0000-1000-8000-00805f9b34fb"


def changeColor(red, green, blue):
	hexString = "7e070503" + format(red, '02x') + format(green, '02x') + format(blue, '02x') + "00ef"
	return bytes.fromhex(hexString)


async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        red = 0
        green = 0
        blue = 0
        while(red < 255):
            await client.write_gatt_char(writeUUID, changeColor(red, green, blue))
            await asyncio.sleep(0.01)
            red += 1
        
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(main(address))
