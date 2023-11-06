from abc import ABC, abstractmethod
from Connection import Connection

class Gate(ABC):
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

    @abstractmethod
    def perform_logic(self):
        pass

class AndGate(Gate):
    def perform_logic(self):
        if all(input.value == 1 for input in self.inputs):
            return 1
        elif any(input.value == 0 for input in self.inputs):
            return 0
        else:
            return 'U'

class OrGate(Gate):
    def perform_logic(self):
        if all(input.value == 0 for input in self.inputs):
            return 0
        elif any(input.value == 1 for input in self.inputs):
            return 1
        else:
            return 'U'

class NandGate(Gate):
    def perform_logic(self):
        if all(input.value == 1 for input in self.inputs):
            return 0
        elif any(input.value == 0 for input in self.inputs):
            return 1
        else:
            return 'U'

class NorGate(Gate):
    def perform_logic(self):
        if all(input.value == 0 for input in self.inputs):
            return 1
        elif any(input.value == 1 for input in self.inputs):
            return 0
        else:
            return 'U'

class XorGate(Gate):
    def perform_logic(self):
        if any(input.value == 'U' or input.value == 'Z' for input in self.inputs):
            return 'U'
        # else we have to count the number of ones!
        no_ones = 0
        for input in self.inputs:
            if input.value == 0:
                no_ones += 1
        if no_ones % 2 == 1:
            return 1
        else:
            return 0

class XnorGate(Gate):
    def perform_logic(self):
        if any(input.value == 'U' or input.value == 'Z' for input in self.inputs):
            return 'U'
        # else we have to count the number of ones!
        no_ones = 0
        for input in self.inputs:
            if input.value == 0:
                no_ones += 1
        if no_ones % 2 == 1:
            return 0
        else:
            return 1

class NotGate(Gate):
    def perform_logic(self):
        # checking the number of inputs!
        assert(len(self.inputs) == 1) , 'Not gate must have one input!'
        if self.inputs[0].value == 'U' or self.inputs[0].value == 'Z':
            return 'U'
        elif self.inputs[0].value == 0:
            return 1
        else:
            return 0


class BufferGate(Gate):
    def perform_logic(self):
        # checking the number of inputs!
        assert(len(self.inputs) == 1), 'Buffer gate must have one input!'
        if self.inputs[0].value == 'U' or self.inputs[0].value == 'Z':
            return 'U'
        else:
            return self.inputs[0].value


