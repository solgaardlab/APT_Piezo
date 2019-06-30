# Thorlabs APT compatibility library in Python

This module provides Thorlabs APT controller compatibility to all PCs that run Python.
It is platform independent and has one dependency on the PyFTDI library. This
module is not a complete implementation of the protocol, more so a subset that is
easily extendable. 

Feel free to fork this repository and change it to your needs. It is currently
designed to be compatible with the BPC-303 controller through USB connection.

### Functionality
* Connection set-up to the FTDI chip inside the Thorlabs APT controllers.
* Automatic detection of bays which are in use.
* Disconnecting from the Thorlabs APT controller gracefully.
* Provides helper methods for message building.
* Piezo zero'ing.
* Changing the Piezo control mode.
* Piezo movement in closed loop mode.

### How to use

The library should be able to automatically detect both the ThorLabs BPC-303 controller as well as a ThorLabs USB photosensor. These devices will have to be plugged in through USB ports on the host computer. Once plugged in and powered on the library can be ran and used as the user needs.

```python
from apt import APT // Controller
from pps import PPS // Photosensor

controller = APT() // Initialize controller
sensor = PPS() // Initialize photosensor
module1 = controller.modules["module1"] // Select modules each module is initialised as moduleX where X is the module number
module2 = controller.modules["module2"]
module3 = controller.modules["module3"]

module1.move(0.5) // Amount of microns to move
module2.move(0.1)
module3.move(0.3)

value = pps.read; // Read value from the power sensor
module1.move(0)
```

The code above initialised the APT class which will set-up a connection to
the Thorlabs APT controller and automatically check which bays are in use.

Every bay that's in use will be initialised as a module followed by it's
index number.

Modules provide move, zero and set closed loop methods. These methods will
automatically move a certain percentage, start the zero'ing proces or allow
the developer to switch between open and closed loop modes.
