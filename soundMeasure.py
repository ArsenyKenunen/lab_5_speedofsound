import RPi.GPIO as GPIO
import spidev
import matplotlib.pyplot as plt


########################################
# Setting up SPI device
# and read function for MCU
########################################

spi = spidev.SpiDev()
spi.open(0, 0)
spi.mode = 0b01
spi.max_speed_hz = 5000000

def spi_read():
    GPIO.output(SPI_CS, 0)
    resp = spi.xfer2([0, 0])
    GPIO.output(SPI_CS, 1)
    return resp[0] << 8 | resp[1]


########################################
# Setting up GPIO pins for MCU control
########################################

GPIO.setmode(GPIO.BCM)

GO_pin = 17
is_sampled_pin = 27
ch_select_pin = 22
is_written_pin = 23
SPI_CS = 8

GPIO.setup(GO_pin, GPIO.OUT)
GPIO.setup(is_sampled_pin, GPIO.IN)
GPIO.setup(ch_select_pin, GPIO.OUT)
GPIO.setup(is_written_pin, GPIO.IN)
GPIO.setup(SPI_CS, GPIO.OUT)

GPIO.output(GO_pin, 0)
GPIO.output(SPI_CS, 1)

########################################
# Defining the write function 
# for saving samples
########################################

def write_list(arr, file_name):
    arr_str = list(map(str, arr))
    with open(file_name, 'w') as file:
        file.write('\n'.join(arr_str))


########################################
# Actual measuring script
########################################

try:
    data = [[] for _ in range(2)]

    # GO command to MCU
    GPIO.output(GO_pin, 1)

    # Waiting for sampling to be done
    while not GPIO.input(is_sampled_pin):
        continue

    # Reading from channels
    for ch in range(2):
        GPIO.output(ch_select_pin, ch)
        
        while GPIO.input(is_written_pin):
            continue
        while not GPIO.input(is_written_pin):
            sample = spi_read()
            data[ch].append(sample)

    # Cancelling GO command to MCU
    GPIO.output(GO_pin, 0)

    # Showing and saving samples
    data[0].pop(0)
    data[1].pop(0)

    plt.plot(data[0]) # blue
    plt.plot(data[1], 'r') # orange

    write_list(data[0], 'data_0.txt')
    write_list(data[1], 'data_1.txt')

    plt.show()

finally:
    GPIO.output(GO_pin, 0)
    GPIO.cleanup()
    spi.close()