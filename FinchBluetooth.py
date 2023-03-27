from time import sleep
from finch_bt_connector import FinchBluetooth

def move_forward(finch, distance):
    speed = 30
    # 30% motor speed corresponds to ~20 cm/s, adjust this value for your specific robot
    time_to_move = distance / 20
    finch.set_motors(speed, speed)
    sleep(time_to_move)
    finch.set_motors(0, 0)

def main():
    # Connect to the Finch robot over Bluetooth
    finch = FinchBluetooth()

    # Set LED color to red
    finch.set_led(100, 0, 0)

    # Move the robot forward by 10 cm
    move_forward(finch, 10)

    # Disconnect the Finch robot
    finch.disconnect()

if __name__ == "__main__":
    main()
