from random import randint
from typing import List

__all__ = ['GenerateByInstructionSetAndRandomConfig']

class ProgramGenerator:
    def generate(self):
        pass
    
    @property
    def name(self):
        pass


class GenerateByInstructionSetAndRandomConfig(ProgramGenerator):
    @property
    def instruction_set(self):
        raise NotImplementedError

    @property
    def config(self):
        raise NotImplementedError

    @property
    def preload_value(self):
        return False

    @property
    def instruction_count(self):
        return self._instruction_count

    @instruction_count.setter
    def instruction_count(self, value):
        self._instruction_count = value

    @staticmethod
    def insert_label(i, current: List[str]):
        pos = randint(0, len(current) - 1)
        current.insert(pos, f"label{i}:")

    def generate(self):
        output = []
        output.append(".data\n")
        for i in range(self.config.number_of_data):
            output.append(f"data{i}: .space 4\n")

        output.append("\n.text\n")
        instructions = ["ori $31, $0, 0x3000"]
        if self.preload_value:
            for reg in self.config.write_registers:
                instructions.append(f"lui ${reg}, " + self.config.random_16_bit_immediate())
                instructions.append(f"ori ${reg}, ${reg}, " + self.config.random_16_bit_immediate())

            for i in range(self.config.number_of_data):
                instructions.append(f"sw {self.config.random_read_register()}, data{i}")

        last_instruction = None
        for i in range(self.instruction_count):
            allow_branch = True
            if i < self.instruction_count * 0.4:
                allow_branch = False
            elif last_instruction is not None and last_instruction.is_branch:
                allow_branch = False

            new_inst = self.instruction_set.next(allow_branch)
            instructions.append(new_inst.populate(self.config))
            last_instruction = new_inst

        for i in range(self.config.number_of_labels):
            self.insert_label(i, instructions)

        instructions.append("ori $v0, $0, 10")
        instructions.append("syscall")

        return "\n".join(output + instructions)
