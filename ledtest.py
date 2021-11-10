import soundcard as sc
import asyncio
from bleak import BleakClient
import numpy as np
from audioListener import AudioListener


address = "22:74:47:27:58:7D"
writeUUID = "0000fff3-0000-1000-8000-00805f9b34fb"
bassFlag = False
red = 255
green = 0
blue = 0
freqDif = 40
listener = AudioListener()
colorList = [
    [255, 0, 0],
    [255, 150, 0],
    [255, 255, 0],
    [155, 255, 0],
    [0, 255, 0],
    [0, 255, 150],
    [0, 255, 255],
    [0, 150, 255],
    [0, 0, 255],
    [150, 0, 255],
    [255, 0, 255],
    [255, 0, 150]
]
currColorIndex = 0

def changeColor(red, green, blue):
    hexString = "7e070503" + \
        format(red, '02x') + format(green, '02x') + \
        format(blue, '02x') + "00ef"
    return bytes.fromhex(hexString)

def changeBright(bright):
    hexString = "7e0401" + format(bright, '02x') + "ffffff00ef"
    return bytes.fromhex(hexString)

async def cycleRGBColors():
    global red, green, blue
    if(red == 255):
        red = 0
        green = 255
        return
    if(green == 255):
        green = 0
        blue = 255
        return
    if(blue == 255):
        blue = 0
        red = 255
        return

async def cycleColorList():
    global currColorIndex, red, green, blue
    red = colorList[currColorIndex][0]
    green = colorList[currColorIndex][1]
    blue = colorList[currColorIndex][2]
    currColorIndex += 1
    if(currColorIndex == 12):
        currColorIndex = 0

async def fade(client):
    bright = 60
    while(bright > 10):
        await client.write_gatt_char(writeUUID, changeBright(bright))
        bright -= 3

async def colorLoop(client):
    global red, green, blue
    while(True):
        if(listener.currentFreq > freqDif):
            bassFlag == False
        if((listener.currentFreq <= freqDif) & (bassFlag == False) & (listener.currentFreq != 0)):
            await client.write_gatt_char(writeUUID, changeColor(red, green, blue))
            await fade(client)
            await cycleColorList()
            print(f"red: {red} green: {green} blue: {blue}")
            bassFlag == True
            print("color changed")
        await asyncio.sleep(0.005)


async def main(address):
    client = BleakClient(address)
    try:
        await client.connect()
        if(client.is_connected):
            await asyncio.gather(colorLoop(client), listener.startListen())
        
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()

asyncio.run(main(address))
