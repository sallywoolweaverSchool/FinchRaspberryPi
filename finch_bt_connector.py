import bluetooth
from BirdBrain import Robot

FINCH_NAME_PREFIX = "Finch"

class FinchBluetooth(Robot):
    def __init__(self):
        address = self.find_finch_bt_address()
        if address:
            super().__init__(name="Finch", address=address, bt=True)
        else:
            raise Exception("Finch robot not found. Make sure it's powered on and in range.")

    def find_finch_bt_address(self):
        print("Searching for Finch robot...")
        devices = bluetooth.discover_devices(lookup_names=True)
        for address, name in devices:
            if name.startswith(FINCH_NAME_PREFIX):
                print(f"Found Finch robot: {name} at {address}")
                return address

        return None
