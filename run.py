from apt import APT
import time


controller = APT()

print(controller.modules)
module1 = controller.modules["module1"]

# Sleep to make sure zero-ing finished
# FIXME: replace with waiting for zero'ing confirmation
time.sleep(15)
# Move piezo by half of it's full movement range
module1.move(0.5)
# Sleep to make sure movement is completed
time.sleep(10)
# Re-zero Piezo
module1.zero()
# Disconnect from controller
controller.disconnect()
