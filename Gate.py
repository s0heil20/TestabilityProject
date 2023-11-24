from abc import ABC, abstractmethod
from Connection import Connection
import itertools

class Gate(ABC):
    def __init__(self, inputs, output):
        self.inputs = inputs
        self.output = output

    @abstractmethod
    def perform_logic(self):
        pass

    @abstractmethod    
    def perform_deductive_fault_simulation(self):
        pass

class AndGate(Gate):
    def perform_logic(self):
        if all(input.value == 1 for input in self.inputs):
            return 1
        elif any(input.value == 0 for input in self.inputs):
            return 0
        else:
            return 'U'
    
    def perform_deductive_fault_simulation(self):
        control_value = 0

        if any(input.value == control_value for input in self.inputs):
            inputs_that_have_to_change = []
            inputs_that_have_to_stay_the_same = []
            for input in self.inputs:
                if input.value == control_value:
                    inputs_that_have_to_change.append(input.fault_set)
                else:
                    inputs_that_have_to_stay_the_same.append(input.fault_set)
            
            return (set.intersection(*inputs_that_have_to_change) - set.union(set(), *inputs_that_have_to_stay_the_same) ) | { self.output.id + '-sa' + str(1-self.output.value)}
        else:
            inputs_that_can_change = []
            for input in self.inputs:
                inputs_that_can_change.append(input.fault_set)
            return set.union(set(), *inputs_that_can_change) | {self.output.id +'-sa'+str(1-self.output.value)}

            


class OrGate(Gate):
    def perform_logic(self):
        if all(input.value == 0 for input in self.inputs):
            return 0
        elif any(input.value == 1 for input in self.inputs):
            return 1
        else:
            return 'U'
        
    def perform_deductive_fault_simulation(self):
        control_value = 1


        if any(input.value == control_value for input in self.inputs):
            inputs_that_have_to_change = []
            inputs_that_have_to_stay_the_same = []
            for input in self.inputs:
                if input.value == control_value:
                    inputs_that_have_to_change.append(input.fault_set)
                else:
                    inputs_that_have_to_stay_the_same.append(input.fault_set)
            
            return (set.intersection(*inputs_that_have_to_change) - set.union(set(),*inputs_that_have_to_stay_the_same) ) | { self.output.id + '-sa' + str(1-self.output.value)}
        else:
            inputs_that_can_change = []
            for input in self.inputs:
                inputs_that_can_change.append(input.fault_set)
            return set.union(set(), *inputs_that_can_change) | {self.output.id +'-sa'+str(1-self.output.value)}

class NandGate(Gate):
    def perform_logic(self):
        if all(input.value == 1 for input in self.inputs):
            return 0
        elif any(input.value == 0 for input in self.inputs):
            return 1
        else:
            return 'U'
    
    def perform_deductive_fault_simulation(self):
        control_value = 0
        inversion = 1

        if any(input.value == control_value for input in self.inputs):
            inputs_that_have_to_change = []
            inputs_that_have_to_stay_the_same = []
            for input in self.inputs:
                if input.value == control_value:
                    inputs_that_have_to_change.append(input.fault_set)
                else:
                    inputs_that_have_to_stay_the_same.append(input.fault_set)
            
            return (set.intersection(*inputs_that_have_to_change) - set.union(set(),*inputs_that_have_to_stay_the_same) ) | { self.output.id + '-sa' + str(1-self.output.value)}
        else:
            inputs_that_can_change = []
            for input in self.inputs:
                inputs_that_can_change.append(input.fault_set)
            return set.union(set(), *inputs_that_can_change) | {self.output.id +'-sa'+str(1-self.output.value)}

class NorGate(Gate):
    def perform_logic(self):
        if all(input.value == 0 for input in self.inputs):
            return 1
        elif any(input.value == 1 for input in self.inputs):
            return 0
        else:
            return 'U'
        
    def perform_deductive_fault_simulation(self):
        control_value = 1
        inversion = 1

        if any(input.value == control_value for input in self.inputs):
            inputs_that_have_to_change = []
            inputs_that_have_to_stay_the_same = []
            for input in self.inputs:
                if input.value == control_value:
                    inputs_that_have_to_change.append(input.fault_set)
                else:
                    inputs_that_have_to_stay_the_same.append(input.fault_set)
            
            return (set.intersection(*inputs_that_have_to_change) - set.union(set(),*inputs_that_have_to_stay_the_same) ) | { self.output.id + '-sa' + str(1-self.output.value)}
        else:
            inputs_that_can_change = []
            for input in self.inputs:
                inputs_that_can_change.append(input.fault_set)
            return set.union(set(), *inputs_that_can_change) | {self.output.id +'-sa'+str(1-self.output.value)}

class XorGate(Gate):
    def perform_logic(self):
        if any(input.value == 'U' or input.value == 'Z' for input in self.inputs):
            return 'U'
        # else we have to count the number of ones!
        no_ones = 0
        for input in self.inputs:
            if input.value == 1:
                no_ones += 1
        if no_ones % 2 == 1:
            return 1
        else:
            return 0
    
    def perform_deductive_fault_simulation(self):
        all_possible_changes = []
        for i in range(1, len(self.inputs) + 1):
            if i % 2 == 1:
                inputs_that_have_to_change = list(itertools.combinations(self.inputs, i))
                for candidate in inputs_that_have_to_change:
                    includings = []
                    excludings = []
                    for input in self.inputs:
                        if input in candidate:
                            includings.append(input.fault_set)
                        else:
                            excludings.append(input.fault_set)
                    possible_change = set.intersection(*includings)
                    for ex in excludings:
                        possible_change = possible_change - ex
                    all_possible_changes.append(possible_change)
                    # print("EX:", str(excludings) , " ", "IN:", str(includings), "POS:", str(possible_change))
        return set.union(*all_possible_changes)  | {self.output.id + "-sa" + str(1 - self.output.value)}                   
                    

class XnorGate(Gate):
    def perform_logic(self):
        if any(input.value == 'U' or input.value == 'Z' for input in self.inputs):
            return 'U'
        # else we have to count the number of ones!
        no_ones = 0
        for input in self.inputs:
            if input.value == 1:
                no_ones += 1
        if no_ones % 2 == 1:
            return 0
        else:
            return 1
        
    def perform_deductive_fault_simulation(self):
        all_possible_changes = []
        for i in range(1, len(self.inputs) + 1):
            if i % 2 == 1:
                inputs_that_have_to_change = list(itertools.combinations(self.inputs, i))
                for candidate in inputs_that_have_to_change:
                    includings = []
                    excludings = []
                    for input in self.inputs:
                        if input in candidate:
                            includings.append(input.fault_set)
                        else:
                            excludings.append(input.fault_set)
                    possible_change = set.intersection(*includings)
                    for ex in excludings:
                        possible_change = possible_change - ex
                    all_possible_changes.append(possible_change)
        return set.union(*all_possible_changes) | {self.output.id + "-sa" + str(1 - self.output.value)}        

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
        
    def perform_deductive_fault_simulation(self):
        return self.inputs[0].fault_set | {self.output.id+"-sa"+str(1-self.output.value)}


class BufferGate(Gate):
    def perform_logic(self):
        # checking the number of inputs!
        assert(len(self.inputs) == 1), 'Buffer gate must have one input!'
        if self.inputs[0].value == 'U' or self.inputs[0].value == 'Z':
            return 'U'
        else:
            return self.inputs[0].value
    
    def perform_deductive_fault_simulation(self):
        return self.inputs[0].fault_set | {self.output.id+"-sa"+str(1-self.output.value)}


