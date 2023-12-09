import spidev
import time

# Initialize SPI
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI port 0, device (CS) 0
spi.max_speed_hz = 1000000  # Set SPI speed (1MHz)


def send_data(device, data1):
    spi.open(0, device)
    resp1 = spi.xfer2([ord(c) for c in data1]) # String
    # resp2 = spi.xfer2([ord(c) for c in data2])
    # resp3 = spi.xfer2([data3])
    spi.close()
    return resp1 #, resp2, resp3





# Check responses
if response1[2][0] == 1:
    print("Successful communication with STM32 #1")

if response2[2][0] == 1:
    print("Successful communication with STM32 #2")



"""
payload for stm32
funciton:
    lockernumber
    unlock / lock

"""
def lock_signal_stm32(locker_number = 1) -> str:
    """
    >>> write_to_database(locker_number = 1, 'img_database/1.jpg')
    ['img_database/1.jpg', 'img_database/2.jpg']"""
    response = send_data(locker_number, "lock")
    if response[2][0] == 1:
        return True




def unlock_signal_stm32(locker_number = 1) -> str:
    """
    >>> read_from_database(1)
    'img_database/1.jpg'"""
    response = send_data(locker_number, "unlock")
    if response[2][0] == 1:
        return True



if __name__ == "__main__":
    # Example usage
    # Send data to STM32 #1
    response1 = send_data(0, "unlock")  # Device 0
    # Send data to STM32 #2
    response2 = send_data(1, "lock")      # Device 1




    pass







