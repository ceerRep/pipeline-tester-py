from instruction import Instruction
from config import RandomConfiguration

from enum import Enum


class SimpleALU(Instruction):
    def populate(self, config: RandomConfiguration):
        return self.get(
            config.random_write_register(),
            config.random_read_register(),
            config.random_read_register(),
        )


class SimpleALUImmediate(Instruction):
    def __init__(self, name, signed_immediate=False, max=65535):
        super().__init__(name)
        self._signed = signed_immediate
        self.max = max

    def populate(self, config: RandomConfiguration):
        if self._signed:
            immediate = config.random_signed_immediate()
        else:
            immediate = config.random_16_bit_immediate(self.max)
        return self.get(
            config.random_write_register(), config.random_read_register(), immediate
        )


class SimpleShift(Instruction):
    def populate(self, config: RandomConfiguration):
        return self.get(
            config.random_write_register(),
            config.random_read_register(),
            config.random_5_bit_immediate(),
        )


class MultiplicationInstruction(Instruction):
    def populate(self, config: RandomConfiguration):
        reg1 = config.random_write_register()
        return self.get(config.random_read_register(), reg1)


class MulMove(Instruction):
    def populate(self, config: RandomConfiguration):
        return self.get(config.random_write_register())


class SimpleZeroBranching(Instruction):
    @property
    def is_branch(self):
        return True

    def populate(self, config: RandomConfiguration):
        return self.get(config.random_read_register(), config.random_label())


class MemoryOperationWidth(Enum):
    Byte = 1
    HalfWord = 2


class MemoryOperationFlags(Enum):
    Read = 1
    ReadUnsigned = 2
    Write = 3


class UnalignedLoad(Instruction):
    def __init__(self, width, flags):
        self._width = width
        opstr = "s" if flags == MemoryOperationFlags.Write else "l"
        wstr = "b" if width == MemoryOperationWidth.Byte else "h"
        ustr = "u" if flags == MemoryOperationFlags.ReadUnsigned else ""
        self._name = opstr + wstr + ustr

    def populate(self, config):
        reg = config.random_write_register()
        ins1 = Instruction.static_get(
            "andi",
            [reg, reg, "2" if self._width == MemoryOperationWidth.HalfWord else "3"],
        )
        return (
            ins1
            + "\n"
            + self.get(
                config.random_write_register(), f"{config.random_memory()}({reg})"
            )
        )

    @property
    def need_memory(self):
        return True
