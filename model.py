class Model:
    SOURCE_DESTINATION = {
        "host": 0x01,
        "rack/motherboard": 0x11,
        "bay0": 0x21,
        "bay1": 0x22,
        "bay2": 0x23,
        "bay3": 0x24,
        "bay4": 0x25,
        "bay5": 0x26,
        "bay6": 0x27,
        "bay7": 0x28,
        "bay8": 0x29,
        "bay9": 0x2A,
        "usb": 0x50
    }

    class __Model:
        # Set values to defaults
        def __init__(self):
            # 0x50 means generic USB device as destination
            self.destination = Model.SOURCE_DESTINATION["rack/motherboard"]
            # 0x01 means main controller as source
            self.source = Model.SOURCE_DESTINATION["host"]
            # 0x01 means the first channel of the controller
            self.channel = 0x01

    instance = None

    def __init__(self):
        # Only initialize a new __Model when none exists yet
        if not Model.instance:
            Model.instance = Model.__Model()

    def __getattr__(self, name):
        # Change the get attribute function to return the corresponding __model attribute
        return getattr(self.instance, name)

    def __setattr__(self, key, value):
        # Change the set attribute function to write the corresponding __model attribute
        setattr(self.instance, key, value)

    @staticmethod
    # Method returns the instance of the __model class
    def get_instance():
        if Model.instance:
            return Model.instance
        else:
            Model.instance = Model.__Model()
            return Model.instance
