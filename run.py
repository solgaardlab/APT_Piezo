from apt import APT
from pps import PPS
import time
from string import Template

print("Initializing sensor")
sensor = PPS()
print("Waiting 10 seconds for sensor to be available...")
time.sleep(10)

print("Initializing controller")
controller = APT()
print(controller.modules)
module1 = controller.modules["module1"]
module2 = controller.modules["module2"]
module3 = controller.modules["module3"]

# TODO: Replace with polling to see if zero'ing is finished on all modules
# Sleep to make sure zero-ing finished
print("Waiting 10 seconds for Piezo Zero process to be completed...")
time.sleep(10)
print("Initializing finished")

scanning_x_step_size = 5
scanning_y_step_size = 5

result = []
line = ""
value_template = Template('| $value |')

for y in range(int((30 + scanning_y_step_size)/scanning_y_step_size)):
    # Move Y to desired location
    y_step = y * scanning_y_step_size
    module1.move(y_step)
    for x in range(int((30 + scanning_x_step_size)/scanning_x_step_size)):
        # Move X to desired location
        x_step = x * scanning_x_step_size
        module2.move(x_step)

        # Read value from photo sensor and put in array in format (x, y, value)
        value = sensor.read()
        result.append((x_step, y_step, value))

        # Append value in printable matrix lines
        line += value_template.substitute(value=value)

        # Print matrix of lines at the end of the X loop
        if x >= 30 / scanning_x_step_size:
            print(line)
            line = ""

print(result)

# Disconnect from controller
controller.disconnect()