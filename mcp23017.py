import smbus

# MCP23017 Register Map
REGISTERS={"BANK0":{"IODIRA":{"reg":            0x00,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "IODIRB":{"reg":            0x01,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "IPOLA":{"reg":             0x02,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "IPOLB":{"reg":             0x03,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "GPINTENA":{"reg":          0x04,
                                "0":            {"bitmask":0x01, "shift":0},
                                "1":            {"bitmask":0x02, "shift":1},
                                "2":            {"bitmask":0x04, "shift":2},
                                "3":            {"bitmask":0x08, "shift":3},
                                "4":            {"bitmask":0x10, "shift":4},
                                "5":            {"bitmask":0x20, "shift":5},
                                "6":            {"bitmask":0x40, "shift":6},
                                "7":            {"bitmask":0x80, "shift":7}},
                    "GPINTENB":{"reg":          0x05,
                                "0":            {"bitmask":0x01, "shift":0},
                                "1":            {"bitmask":0x02, "shift":1},
                                "2":            {"bitmask":0x04, "shift":2},
                                "3":            {"bitmask":0x08, "shift":3},
                                "4":            {"bitmask":0x10, "shift":4},
                                "5":            {"bitmask":0x20, "shift":5},
                                "6":            {"bitmask":0x40, "shift":6},
                                "7":            {"bitmask":0x80, "shift":7}},
                    "DEFVALA":{"reg":0x06,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "DEFVALB":{"reg":           0x07,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "INTCONA":{"reg":           0x08,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "INTCONB":{"reg":           0x09,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "IOCON":{"reg":             0x0A,
                             "-":               {"bitmask":0x01, "shift":0},
                             "intpol":          {"bitmask":0x02, "shift":1},
                             "odr":             {"bitmask":0x04, "shift":2},
                             "haen":            {"bitmask":0x08, "shift":3},
                             "disslw":          {"bitmask":0x10, "shift":4},
                             "seqop":           {"bitmask":0x20, "shift":5},
                             "mirror":          {"bitmask":0x40, "shift":6},
                             "bank":            {"bitmask":0x80, "shift":7}},
                    "GPPUA":{"reg":             0x0C,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "GPPUB":{"reg":             0x0D,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INTFA":{"reg":             0x0E,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INTFB":{"reg":             0x0F,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INCAPA":{"reg":            0x10,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "INCAPB":{"reg":            0x11,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "GPIOA":{"reg":             0x12,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "GPIOB":{"reg":             0x13,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "OLATA":{"reg":             0x14,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "OLATB":{"reg":             0x15,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}}},
           "BANK1":{"IODIRA":{"reg":            0x00,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "IPOLA":{"reg":             0x01,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "GPINTENA":{"reg":          0x02,
                                "0":            {"bitmask":0x01, "shift":0},
                                "1":            {"bitmask":0x02, "shift":1},
                                "2":            {"bitmask":0x04, "shift":2},
                                "3":            {"bitmask":0x08, "shift":3},
                                "4":            {"bitmask":0x10, "shift":4},
                                "5":            {"bitmask":0x20, "shift":5},
                                "6":            {"bitmask":0x40, "shift":6},
                                "7":            {"bitmask":0x80, "shift":7}},
                    "DEFVALA":{"reg":           0x03,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "INTCONA":{"reg":           0x04,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "IOCON":{"reg":             0x05,
                             "-":               {"bitmask":0x01, "shift":0},
                             "intpol":          {"bitmask":0x02, "shift":1},
                             "odr":             {"bitmask":0x04, "shift":2},
                             "haen":            {"bitmask":0x08, "shift":3},
                             "disslw":          {"bitmask":0x10, "shift":4},
                             "seqop":           {"bitmask":0x20, "shift":5},
                             "mirror":          {"bitmask":0x40, "shift":6},
                             "bank":            {"bitmask":0x80, "shift":7}},
                    "GPPUA":{"reg":             0x06,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INTFA":{"reg":             0x07,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INCAPA":{"reg":            0x08,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "GPIOA":{"reg":             0x09,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "OLATA":{"reg":             0x0A,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "IODIRB":{"reg":            0x10,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "IPOLB":{"reg":             0x11,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "GPINTENB":{"reg":          0x12,
                                "0":            {"bitmask":0x01, "shift":0},
                                "1":            {"bitmask":0x02, "shift":1},
                                "2":            {"bitmask":0x04, "shift":2},
                                "3":            {"bitmask":0x08, "shift":3},
                                "4":            {"bitmask":0x10, "shift":4},
                                "5":            {"bitmask":0x20, "shift":5},
                                "6":            {"bitmask":0x40, "shift":6},
                                "7":            {"bitmask":0x80, "shift":7}},
                    "DEFVALB":{"reg":           0x13,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "INTCONB":{"reg":           0x14,
                               "0":             {"bitmask":0x01, "shift":0},
                               "1":             {"bitmask":0x02, "shift":1},
                               "2":             {"bitmask":0x04, "shift":2},
                               "3":             {"bitmask":0x08, "shift":3},
                               "4":             {"bitmask":0x10, "shift":4},
                               "5":             {"bitmask":0x20, "shift":5},
                               "6":             {"bitmask":0x40, "shift":6},
                               "7":             {"bitmask":0x80, "shift":7}},
                    "GPPUB":{"reg":             0x16,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INTFB":{"reg":             0x17,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "INCAPB":{"reg":            0x18,
                              "0":              {"bitmask":0x01, "shift":0},
                              "1":              {"bitmask":0x02, "shift":1},
                              "2":              {"bitmask":0x04, "shift":2},
                              "3":              {"bitmask":0x08, "shift":3},
                              "4":              {"bitmask":0x10, "shift":4},
                              "5":              {"bitmask":0x20, "shift":5},
                              "6":              {"bitmask":0x40, "shift":6},
                              "7":              {"bitmask":0x80, "shift":7}},
                    "GPIOB":{"reg":             0x19,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}},
                    "OLATB":{"reg":             0x1A,
                             "0":               {"bitmask":0x01, "shift":0},
                             "1":               {"bitmask":0x02, "shift":1},
                             "2":               {"bitmask":0x04, "shift":2},
                             "3":               {"bitmask":0x08, "shift":3},
                             "4":               {"bitmask":0x10, "shift":4},
                             "5":               {"bitmask":0x20, "shift":5},
                             "6":               {"bitmask":0x40, "shift":6},
                             "7":               {"bitmask":0x80, "shift":7}}}}

class MCP23017:
    def __init__(self, bus, address):
        self.bus=bus
        self.address=address
        self.bank=self.get_bank()

    def _decode(self, key):
        raw_data=self.bus.read_byte_data(self.address, REGISTERS[self.bank][key]["reg"])
        data={}
        for reg_key in REGISTERS[self.bank][key].keys():
            if reg_key!="reg":
                data[reg_key]=(raw_data & REGISTERS[self.bank][key][reg_key]["bitmask"]) >> REGISTERS[self.bank][key][reg_key]["shift"]
        return data

    def _encode(self, key, val, reg_key):
        raw_data=self.bus.read_byte_data(self.address, REGISTERS[self.bank][key]["reg"])
        new_data=(raw_data & ~REGISTERS[self.bank][key][reg_key]["bitmask"]) | (val << REGISTERS[self.bank][key][reg_key]["shift"])
        self.bus.write_byte_data(self.addr, REGISTERS[self.bank][key]["reg"], new_data)
           
    def get_bank(self):
        return bool(self._decode("IOCON")["bank"])

    def set_bank(self, val=False):
        self._encode("IOCON", val, "bank")

    def get_interrupt_mirror(self):
        return bool(self._decode("IOCON")["mirroe"])

    def set_mirror(self, val=False):
        self._encode("IOCON", val, "mirror")

    def get_sequential_operation_(self):
        return bool(self._decode("IOCON")["seqop"])

    def set_seqop(self, val=False):
        self._encode("IOCON", val, "seqop")

    def get_slew_rate(self):
        return bool(self._decode("IOCON")["disslw"])

    def enable_slew_rate(self):
        self._encode("IOCON", 0, "disslw")

    def disable_slew_rate(self):
        self._encode("IOCON", 1, "disslw")

    def get_odr(self):
        return bool(self._decode("IOCON")["odr"])

    def enable_open_drain_output(self):
        self._encode("IOCON", 1, "odr")

    def disable_open_drain_output(self):
        self._encode("IOCON", 0, "odr")
        
    def get_intpol(self):
        return bool(self._decode("IOCON")["intpol"])

    def set_intpol(self, val=False):
        self._encode("IOCON", val, "intpol")
        
    def get_gpio_direction(self, port, pin):
        return bool(self._decode("IODIR"+port)[pin])

    def set_gpio_direction(self, port, pin, val):
        self._encode("IODIR"+port, val, pin)
    
    def get_input_polarity(self, port, pin):
        return bool(self._decode("IPOL"+port)[pin])

    def set_input_polarity(self, port, pin, val):
        self._encode("IPOL"+port, val, pin)

    def get_interrupt_on_change(self, port, pin):
        return bool(self._decode("GPINTEN"+port)[pin])

    def set_interrupt_on_change(self, port, pin, val):
        self._encode("GPINTEN"+port, val, pin)

    def get_default_campare_value(self, port, pin):
        return bool(self._decode("DEFVAL"+port)[pin])

    def set_default_campare_value(self, port, pin, val):
        self._encode("DEFVAL"+port, val, pin)

    def get_interrupt_control(self, port, pin):
        return bool(self._decode("INTCON"+port)[pin])

    def set_interrupt_control(self, port, pin, val):
        self._encode("INTCON"+port, val, pin)
    
    def get_pullup(self, port, pin):
        return bool(self._decode("GPPU"+port)[pin])

    def set_pullup(self, port, pin, val):
        self._encode("GPPU"+port, val, pin)

    def get_interrupt_flag(self, port, pin):
        return bool(self._decode("INTF"+port)[pin])

    def get_interrupt_captured(self, port, pin):
        return bool(self._decode("INTCAP"+port)[pin])

    def get_gpio(self, port, pin):
        return bool(self._decode("GPIO"+port)[pin])

    def set_gpio(self, port, pin, val):
        self._encode("GPIO"+port, val, pin)

    def get_output_latch(self, port, pin):
        return bool(self._decode("OLAT"+port)[pin])

    def set_output_latch(self, port, pin, val):
        self._encode("OLAT"+port, val, pin)
