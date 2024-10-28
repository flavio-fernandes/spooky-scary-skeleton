import asyncio
import board
import pwmio
import digitalio
from adafruit_motor import servo
import adafruit_hcsr04

DISTANCE_WHILE_SCARED = 24
DISTANCE_WHILE_NOT_SCARED = 58

class Controls:
    def __init__(self):
        self.debug = True
        self.scared = False


async def monitor_servo(controls):
    min_angle = 4
    # the max servo angle to be used
    scared_angle = 52

    # the number of angles to decrease while not scared
    angle_delta = 3

    pwm = pwmio.PWMOut(board.GP15, frequency=50)
    test_servo = servo.Servo(pwm, min_pulse=1000, max_pulse=1800)
    test_servo.angle = scared_angle
    await asyncio.sleep(3)
    test_servo.angle = min_angle
    await asyncio.sleep(1)
    last_scared = False

    while True:
        if controls.scared:
            if not last_scared:
                test_servo.angle = scared_angle
                await asyncio.sleep(3)
                last_scared = True
            await asyncio.sleep(0)
            continue

        
        # If we made it here, we are not scared.
        # So, servo should go back to angle 0.
        await asyncio.sleep(0.125)
        if not last_scared:
            continue
        
        if test_servo.angle < angle_delta:
            test_servo.angle = min_angle
            last_scared = False
        else:
            test_servo.angle -= angle_delta


async def monitor_sonar(controls):
    # Sonar reads may be a little unreliable. Being so, we will
    # collect sonar_reads_size samples in order to decide when to
    # declare skull scared.
    sonar_reads_size = 4
    sonar_reads = [False] * sonar_reads_size
    sonar_read_index = 0

    sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.GP0, echo_pin=board.GP1)
    while True:
        await asyncio.sleep(0.2)
        try:
            curr_distance = int(sonar.distance)
            if controls.debug:
                print("Distance:", curr_distance, "Reads:", sonar_reads)

                # Any sonar read distance less than scared_max_distance
                # means we should be scared.
                scared_max_distance = DISTANCE_WHILE_SCARED if controls.scared else DISTANCE_WHILE_NOT_SCARED

                sonar_reads[sonar_read_index] = True if curr_distance < scared_max_distance else False
            sonar_read_index += 1
            if sonar_read_index >= sonar_reads_size:
                sonar_read_index = 0
            controls.scared = all(sonar_reads)
        except RuntimeError as e:
            print("Sonar read failed", e)
            await asyncio.sleep(1)


async def main():
    controls = Controls()
    sonar_task = asyncio.create_task(monitor_sonar(controls))
    servo_task = asyncio.create_task(monitor_servo(controls))
    await asyncio.gather(sonar_task, servo_task)


asyncio.run(main())
