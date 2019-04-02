# Thorlabs APT communications through Python

This library is a small and cohesive library that allows for 
communications with Thorlabs APT stage controllers. This library
depends on PyFTDI as the Thorlabs APT controllers function through 
FTDI USB to Serial chips.

### Preqequisites

* PyFTDI - A Python library for connecting with FTDI chips
* libusb or an alternative - as a back-end USB implementation for PyFTDI

### Usage

An exmaple of usage:

```python
APT = apt.APT()

controller = APT.controller
module1 = APT.module1
module2 = APT.module2
module3 = APT.module3
mbuilder = APT.mbuilder

message = mbuilder.gen_header(0x0005, [0x00, 0x00], 0x11)

controller.write_data(message)
controller.read_data(90, 1)
```

Initialise a new APT instance, this will connect to the first Thorlabs
APT Stage Controller that can be found through USB.

The controller property allows for messages to be written and read from
the Thorlabs APT Stage Controller. The modules are automatically initiated
based on an information request received from the controller.

The APT class includes a message builder which builds the header and data
messages for the communications protocol.