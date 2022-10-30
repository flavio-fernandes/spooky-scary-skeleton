# spooky-scary-skeleton
Circuit Python implementation of Kevin McAleer's Spooky Scary Skeleton

This directory contains the software used for controlling the [Spooky Scary Skeleton](https://www.kevsrobots.com/blog/spooky-scary-skeleton.html) using [Circuit Python](https://circuitpython.org/).

### Removing _all_ files from CIRCUITPY drive

```
# NOTE: Do not do this before backing up all files!!!
>>> import storage ; storage.erase_filesystem()
```

### Copying files from cloned repo to CIRCUITPY drive
```
# First, get to the REPL prompt so the board will not auto-restart as
# you copy files into it. To do that, hit CONTROL+C from the Circuit Python serial console:

<CTRL-C>
Adafruit CircuitPython 7.3.3 on 2022-08-29; Raspberry Pi Pico with rp2040
>>> 

# Then, from a shell terminal window, assuming that Pico
# is mounted under /Volumes/CIRCUITPY
$  cd ${THIS_REPO_DIR}/

$  [ -e ./code.py ] && \
   [ -d /Volumes/CIRCUITPY/ ] && \
   rm -rf /Volumes/CIRCUITPY/*.py && \
   (tar czf - *) | ( cd /Volumes/CIRCUITPY ; tar xzvf - ) && \
   echo ok || echo not_okay
```

### Libraries

Use [circup](https://learn.adafruit.com/keep-your-circuitpython-libraries-on-devices-up-to-date-with-circup)
to install these libraries into the Raspberry Pi Pico:

```text
$ python3 -m venv .env && source ./.env/bin/activate && \
  pip install --upgrade pip

$ pip3 install circup

$ for LIB in \
  adafruit_hcsr04 \
  asyncio \
  adafruit_motor \
  ; do circup install $LIB ; done
```

This is what it should look like:
```text
$ ls /Volumes/CIRCUITPY/
LICENSE		README.md	boot_out.txt	code.py		lib

$ ls /Volumes/CIRCUITPY/lib
adafruit_hcsr04.mpy	adafruit_ticks.mpy
adafruit_motor		asyncio

$ circup freeze
Found device at /Volumes/CIRCUITPY, running CircuitPython 7.3.3.
adafruit_hcsr04==0.4.15
adafruit_ticks==1.0.8
asyncio==0.5.17
adafruit_motor==3.4.5
```

At this point, all needed files should be in place, and all that
is needed is to let code.py run. From the Circuit Python serial console:

```text
>>  <CTRL-D>
soft reboot

Auto-reload is on. Simply save files over USB to run them or enter REPL to disable.
code.py output:
Distance: 70 Reads: [False, False, False]
...
```


