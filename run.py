import apt
import time


APT = apt.APT()

print(APT.modules)
module1 = APT.modules["module1"]

# Sleep to make sure zero-ing finished
# FIXME: replace with waiting for zero'ing confirmation
time.sleep(15)
# Move piezo by half of it's full movement range
module1.move(0.5)
# Sleep to make sure movement is completed
time.sleep(10)
# Re-zero Piezo
module1.zero()
