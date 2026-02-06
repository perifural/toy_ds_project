import asyncio
import time
from bleak import BleakScanner, BleakClient

TARGET_NAME = "JEU-Lush139-XT"
OPEN_CTRL = "SECRET"

def uuid_add32(uuid_str: str, offset: int) -> str:
    head, rest = uuid_str.split("-", 1)
    new_head = (int(head, 16) + offset) & 0xFFFFFFFF
    return f"{new_head:08x}-{rest}"

async def main():
    print("Searching...")
    devices = await BleakScanner.discover()

    target = None
    for d in devices:
        if d.name == TARGET_NAME:
            target = d
            break

    if not target:
        print("device not found\n")
        return

    print("device found\n")
    print("Connecting...")

    async with BleakClient(target.address) as client:
        print("success\n")

        services = client.services
        service = list(services)[0]

        uuid1 = service.uuid
        uuid3 = uuid_add32(uuid1, 2)

        print("Opening...")

        data = OPEN_CTRL.encode("utf-8")
        await client.write_gatt_char(
            uuid3,
            data,
            response=False
        )

        print("success\n")
        time.sleep(3)

    print("Disconnected\n")

asyncio.run(main())
input("")
