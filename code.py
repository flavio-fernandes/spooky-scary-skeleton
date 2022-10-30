import asyncio
import board
import pwmio
import digitalio
from adafruit_motor import servo
import adafruit_hcsr04

pwm = pwmio.PWMOut(board.GP15, frequency=50)
test_servo = servo.Servo(pwm, min_pulse=1000, max_pulse=2000)
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)

debug = False

class Controls:
    def __init__(self):
        self.angle = 0
        self.scared = False


async def monitor_servo(controls):
    # the max servo angle to be used
    scared_angle = 71

    # the number of angles to decrease while not scared
    angle_delta = 3

    while True:
        if controls.scared:
            test_servo.angle = scared_angle
            await asyncio.sleep(3)
            continue

        # If we made it here, we are not scared.
        # So, servo should go back to angle 0.
        await asyncio.sleep(0.125)
        if test_servo.angle == 0:
            pass
        elif test_servo.angle < angle_delta:
            test_servo.angle = 0
        else:
            test_servo.angle -= angle_delta


async def monitor_sonar(controls):
    # Sonar reads may be a little unreliable. Being so, we will
    # collect sonar_reads_size samples in order to decide when to
    # declare skull scared.
    sonar_reads_size = 3
    sonar_reads = [False] * sonar_reads_size
    sonar_read_index = 0

    # Any sonar read distance less than scared_max_distance
    # means we should be scared.
    scared_max_distance = 29

    while True:
        await asyncio.sleep(0.1)
        try:
            curr_distance = int(sonar.distance)
            if debug:
                print("Distance:", curr_distance, "Reads:", sonar_reads)
            sonar_reads[sonar_read_index] = curr_distance < scared_max_distance
            sonar_read_index = (sonar_read_index + 1) % sonar_reads_size
            controls.scared = all(sonar_reads)
        except RuntimeError as e:
            print("Sonar read failed", e)


async def blink(controls):
    with digitalio.DigitalInOut(board.LED) as led:
        led.switch_to_output()
        while True:
            if not controls.scared:
                led.value = not led.value
            await asyncio.sleep(1.25)


async def main():
    controls = Controls()

    sonar_task = asyncio.create_task(monitor_sonar(controls))
    servo_task = asyncio.create_task(monitor_servo(controls))
    blink_task = asyncio.create_task(blink(controls))
    await asyncio.gather(sonar_task, servo_task, blink_task)


test_servo.angle = 0
asyncio.run(main())
