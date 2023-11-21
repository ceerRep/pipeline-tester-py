import random

class InstructionSet:
    def __init__(self):
        self.full_list = []
        self.non_branching_list = []

    def populate_instruction_list(self, list_of_instructions):
        self.full_list = list(list_of_instructions)
        self.non_branching_list = [inst for inst in list_of_instructions if not inst[0].is_branch]

    def next(self, allow_branch):
        if allow_branch:
            return self.choose_with_probability(self.full_list)
        else:
            return self.choose_with_probability(self.non_branching_list)

    @staticmethod
    def choose_with_probability(instruction_list):
        total = sum(weight for _, weight in instruction_list)
        r = random.uniform(0, total)
        upto = 0
        for inst, weight in instruction_list:
            if upto + weight >= r:
                return inst
            upto += weight
        assert False, "Shouldn't get here"
