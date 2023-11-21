from config import RandomConfiguration

class Instruction:
    def __init__(self, name=None):
        self._name = name

    @property
    def name(self):
        return self._name

    def populate(self, config: RandomConfiguration):
        raise NotImplementedError("Must be implemented in subclasses")

    def get(self, *parameters):
        return self._name + " " + ','.join(parameters)

    @staticmethod
    def static_get(name, parameters):
        return name + " " + ','.join(parameters)

    @property
    def is_branch(self):
        return False

    @property
    def need_memory(self):
        return False


class Addu(Instruction):
    def __init__(self):
        super().__init__("addu")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register(), config.random_read_register(), config.random_read_register())


class Lui(Instruction):
    def __init__(self):
        super().__init__("lui")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register(), config.random_16_bit_immediate())

class Subu(Instruction):
    def __init__(self):
        super().__init__("subu")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register(), config.random_read_register(), config.random_read_register())

class Ori(Instruction):
    def __init__(self):
        super().__init__("ori")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register(), config.random_read_register(), config.random_16_bit_immediate())

class Lw(Instruction):
    def __init__(self):
        super().__init__("lw")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register(), config.random_memory())

    @property
    def need_memory(self):
        return True

class Nop(Instruction):
    def __init__(self):
        super().__init__("nop")

    def populate(self, config: RandomConfiguration):
        return self.get()

class Sw(Instruction):
    def __init__(self):
        super().__init__("sw")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_read_register(), config.random_memory())

    @property
    def need_memory(self):
        return True

class TwoOperandBranching(Instruction):
    def __init__(self, name):
        super().__init__(name)

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_read_register(), config.random_read_register(), config.random_label())

    @property
    def is_branch(self):
        return True

class J(Instruction):
    def __init__(self):
        super().__init__("j")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_label())

    @property
    def is_branch(self):
        return True

class Jal(Instruction):
    def __init__(self):
        super().__init__("jal")

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_label())

    @property
    def is_branch(self):
        return True

class Jr(Instruction):
    def __init__(self):
        super().__init__("jr")

    def populate(self, config: RandomConfiguration):
        return self.get("$ra")

    @property
    def is_branch(self):
        return True

class Jalr(Instruction):
    def __init__(self):
        super().__init__("jalr")

    def populate(self, config: RandomConfiguration):
        register = config.random_read_register()
        while register == "$31":
            register = config.random_read_register()
        return self.get(register, "$ra")

    @property
    def is_branch(self):
        return True
