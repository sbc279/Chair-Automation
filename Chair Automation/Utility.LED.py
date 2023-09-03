from machine import Pin, PWM
import time

# Function to dim the LED gradually
def dim_led(pwm_led, min_brightness, max_brightness):
    for duty_cycle in range(min_brightness, max_brightness + 1, 10):
        pwm_led.duty(duty_cycle)
        time.sleep(0.1)

# Function to turn off the passed PWM LED
def turn_off_led(pwm_led):
    pwm_led.duty(0)

# Function to turn on the passed PWM LED at maximum brightness
def turn_on_led(pwm_led, max_brightness):
    pwm_led.duty(max_brightness)

# Function to undim the LED gradually
def undim_led(pwm_led, max_brightness, min_brightness):
    for duty_cycle in range(max_brightness, min_brightness - 1, -10):
        pwm_led.duty(duty_cycle)
        time.sleep(0.1)

# Configure the LED pin and PWM object
led_pin = Pin(2, Pin.OUT)  # Replace 2 with the appropriate GPIO pin number
pwm = PWM(led_pin)

# Define the minimum and maximum brightness levels
min_brightness = 0  # 0% brightness
max_brightness = 1023  # 100% brightness

# Dim the LED using the dim_led function
dim_led(pwm, min_brightness, max_brightness)
time.sleep(2)  # Wait for 2 seconds

# Turn on the dimmed LED using the turn_on_led function
turn_on_led(pwm, max_brightness)
time.sleep(2)  # Wait for 2 seconds

# Turn off the LED using the turn_off_led function
turn_off_led(pwm)

# Undim the LED using the undim_led function
undim_led(pwm, max_brightness, min_brightness)

# Clean up and release resources
pwm.deinit()