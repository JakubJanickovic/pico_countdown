from lcd import LCD_1inch14

from machine import Pin,SPI,PWM, I2C
import framebuf
import time
import binascii

from rtc import ds3231


BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

I2C_PORT = 0
I2C_SDA = 20
I2C_SCL = 21

ALARM_PIN = 3

def read_time_format(timestamp_str):
    date_str, time_str, day_name = timestamp_str.split()
    year, month, day = map(int, date_str.split('/'))
    hour, minute, second = map(int, time_str.split(':'))
    time_tuple = (year, month, day, hour, minute, second, 0, 0, -1)
    timestamp = time.mktime(time_tuple)
    
    return timestamp

def countdown(now):
    target_date = time.mktime((2024, 12, 31, 0, 0, 0, 0, 0, -1))
    time_remaining = target_date - now
    if time_remaining > 0:
    # Convert remaining seconds into days, hours, minutes, and seconds
        days = time_remaining // (24 * 3600)
        hours = (time_remaining % (24 * 3600)) // 3600
        minutes = (time_remaining % (3600)) // 60
        seconds = time_remaining % 60
        
        formatted_seconds = f"{int(seconds):02}"
        formatted_minutes = f"{int(minutes):02}"
        formatted_hours = f"{int(hours):02}"
        
        return f"{int(days)} days | {int(formatted_hours)}:{int(formatted_minutes)}:{int(formatted_seconds)}"

def main():
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch14()
    #color BRG
    LCD.fill(LCD.white)
    
    rtc = ds3231(I2C_PORT,I2C_SCL,I2C_SDA)

    t = rtc.read_time()
    ts = read_time_format(t)
    remaining = countdown(ts)
    LCD.text(remaining,10,50,LCD.blue)
    LCD.show()
    

if __name__=='__main__':
    while True:
        main()