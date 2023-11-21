import random

class RandomConfiguration:
    def __init__(self):
        self._no_zero = False
        self._number_of_registers = None
        self.number_of_labels = 3
        self.number_of_data = 3
        self.maximum_register = 4
        self.maximum_immediate = 5
        self.write_registers = []
        self.read_registers = []
        self.refresh_register()

    @property
    def no_zero_register(self):
        return self._no_zero

    @no_zero_register.setter
    def no_zero_register(self, value):
        self._no_zero = value
        self.refresh_register()

    @property
    def maximum_register(self):
        return self._number_of_registers

    @maximum_register.setter
    def maximum_register(self, value):
        self._number_of_registers = value
        self.refresh_register()

    def refresh_register(self):
        start = 1 if self._no_zero else 0
        self.write_registers = list(range(start, self._number_of_registers))
        self.read_registers = self.write_registers + [31]

    def random_read_register(self):
        num = random.choice(self.read_registers)
        return f"${num}"

    def random_write_register(self):
        num = random.choice(self.write_registers)
        return f"${num}"

    def random_16_bit_immediate(self, max=65535):
        return str(random.randint(0, min(min(max, self.maximum_immediate), 65535) - 1))

    def random_signed_immediate(self):
        bound = min(self.maximum_immediate, 32767)
        return str(random.randint(-bound, bound))

    def random_5_bit_immediate(self):
        return str(random.randint(0, min(self.maximum_immediate, 31) - 1))

    def random_memory(self):
        return f"data{random.randint(0, self.number_of_data - 1)}"

    def random_label(self):
        return f"label{random.randint(0, self.number_of_labels - 1)}"
