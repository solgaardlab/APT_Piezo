from apt import APT
from pps import PPS
import time

sensor = PPS()
controller = APT()

print(controller.modules)
module1 = controller.modules["module1"]

# Sleep to make sure zero-ing finished
# FIXME: replace with waiting for zero'ing confirmation
time.sleep(15)
# Move piezo by 5 micron
module1.move(5)
# Sleep to make sure movement is completed
time.sleep(10)
# Re-zero Piezo
module1.zero()
# Disconnect from controller
controller.disconnect()
