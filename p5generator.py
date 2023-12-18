from instruction import *
from instructions import *
from generator1 import *
from instructionset import *

__all__ = ['P5Generator']

class P5Generator(GenerateByInstructionSetAndRandomConfig):
    def __init__(self, large=False):
        self._large = large
        self.instruction_count = 100  
        self._instruction_set = InstructionSet()
        self._instruction_set.populate_instruction_list([
                    (SimpleALU("addu"), 1),
                    (SimpleALU("add"), 1),
                    (SimpleALU("subu"), 1),
                    (SimpleALU("sub"), 1),
                    (SimpleALU("and"), 1),
                    (SimpleALU("or"), 1),
                    (SimpleALU("xor"), 1),
                    (SimpleALU("nor"), 1),
                    (SimpleALU("slt"), 1),
                    (SimpleALU("sltu"), 1),
                    (SimpleShift("sll"), 1),
                    (SimpleShift("srl"), 1),
                    (SimpleShift("sra"), 1),
                    (SimpleALU("sllv"), 1),
                    (SimpleALU("srlv"), 1),
                    (SimpleALU("srav"), 1),
                    (Lui(), 1),
                    (TwoOperandBranching("beq"), 1),
                    (TwoOperandBranching("bne"), 1),
                    (SimpleZeroBranching("bgtz"), 1),
                    (SimpleZeroBranching("bgez"), 1),
                    (SimpleZeroBranching("bltz"), 1),
                    (SimpleZeroBranching("blez"), 1),
                    (SimpleALUImmediate("slti", True, 32768), 1),
                    (SimpleALUImmediate("sltiu", False, 32768), 1),
                    (SimpleALUImmediate("addi"), 1),
                    (SimpleALUImmediate("addiu"), 1),
                    (SimpleALUImmediate("xori"), 1),
                    (SimpleALUImmediate("andi"), 1),
                    (SimpleALUImmediate("ori"), 1),
                    (J(), 1),
                    (Jal(), 1),
                    (Jr(), 0.3),
                    (Jalr(), 0.3),
                    (Lw(), 1),
                    (Sw(), 1),
                    (UnalignedLoad(MemoryOperationWidth.HalfWord, MemoryOperationFlags.ReadUnsigned), 1),
                    (UnalignedLoad(MemoryOperationWidth.HalfWord, MemoryOperationFlags.Read), 1),
                    (UnalignedLoad(MemoryOperationWidth.HalfWord, MemoryOperationFlags.Write), 1),
                    (UnalignedLoad(MemoryOperationWidth.Byte, MemoryOperationFlags.Write), 1),
                    (UnalignedLoad(MemoryOperationWidth.Byte, MemoryOperationFlags.ReadUnsigned), 1),
                    (UnalignedLoad(MemoryOperationWidth.Byte, MemoryOperationFlags.Read), 1),
                    (MultiplicationInstruction("mult"), 1),
                    (MultiplicationInstruction("multu"), 1),
                    (MultiplicationInstruction("div"), 1),
                    (MultiplicationInstruction("divu"), 1),
                    (MulMove("mthi"), 1),
                    (MulMove("mtlo"), 1),
                    (MulMove("mfhi"), 1),
                    (MulMove("mflo"), 1),
        ])

        self._config = RandomConfiguration()
        if large:
            self._config.maximum_immediate = 2147483647
            self._config.maximum_register = 20
            self._config.number_of_labels = 7
        else:
            self._config.maximum_immediate = 5
            self._config.maximum_register = 3
            self._config.number_of_labels = 3

        self._config.number_of_data = 3

    @property
    def instruction_set(self):
        return self._instruction_set

    @property
    def config(self):
        return self._config

    @property
    def name(self):
        return "Comprehensive test for P5" + (" (Large)" if self._large else "")

    @property
    def preload_value(self):
        return self._large
