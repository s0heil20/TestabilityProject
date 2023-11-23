import re
from Connection import Connection
from Gate import *
from ParserIscas import parse_iscas_bench
import random

class LogicalCircuit:

    def __init__(self, inputs: list, outputs: list, gates: dict):
        # First scanning gates inputs for potential FANOUTS!
        self.hasFanout = {}
        for out_net in gates:
            gate_name, gate_inputs = self._parse_gate(gates[out_net])
            for input in gate_inputs:
                if input in self.hasFanout:
                    self.hasFanout[input] = True
                else:
                    self.hasFanout[input] = False

        self.gates = {}
        self.nets = {}
        self.outputs = []
        self.inputs = []

        for input in inputs:
            new_input = Connection(input, "IN")
            self.inputs.append( new_input )
            if input not in self.nets:
                self.nets[input] = new_input
        for output in outputs:
            new_output = Connection(output, "OUT")
            self.outputs.append( new_output )
            if output not in self.nets:
                self.nets[output] = new_output
        for out_net in gates:
            
            gate_name, gate_inputs = self._parse_gate(gates[out_net])

            new_net = Connection(out_net,"NET")
            if out_net not in self.nets:
                self.nets[out_net] = new_net

            output_of_gate = self.nets[out_net]
            
            inputs_of_gate = []
            for input in gate_inputs:
                if self.hasFanout[input]:
                    new_fanout_net_id = input + "_" + self.nets[input].get_new_fan_out_net_name()
                    new_fanouted_net = Connection(new_fanout_net_id, "NET")
                    self.nets[input].fanouts.append(new_fanouted_net)
                    inputs_of_gate.append(new_fanouted_net)
                    self.nets[new_fanout_net_id] = new_fanouted_net
                else:
                    inputs_of_gate.append(self.nets[input])

            if gate_name == "AND":
                self.gates[out_net] = AndGate(inputs_of_gate, output_of_gate)
            elif gate_name == "OR":
                self.gates[out_net] = OrGate(inputs_of_gate, output_of_gate)
            elif gate_name == "NAND":
                self.gates[out_net] = NandGate(inputs_of_gate, output_of_gate)
            elif gate_name == "NOR":
                self.gates[out_net] = NorGate(inputs_of_gate, output_of_gate)
            elif gate_name == "XOR":
                self.gates[out_net] = XorGate(inputs_of_gate, output_of_gate)
            elif gate_name == "XNOR":
                self.gates[out_net] = XnorGate(inputs_of_gate, output_of_gate)
            elif gate_name == "NOT":
                self.gates[out_net] = NotGate(inputs_of_gate, output_of_gate)
            elif gate_name == "BUFF":
                self.gates[out_net] = BufferGate(inputs_of_gate, output_of_gate)
            else:
                print("Invalid gate name! " + gate_name)

    def _parse_gate(self, gate: str):
        # Use regular expression to match the first word and the numbers inside parentheses
        match = re.match(r'^([A-Z]+)\(([\d\s,]+)\)', gate)

        if match:
            # Extract the first word and the comma-separated numbers
            gate_name = match.group(1)
            inputs_ids = [id.replace(" ", '') for id in match.group(2).split(',')] 
            return gate_name, inputs_ids
        else:
            print("Invalid format for gate!")
            return None

    def simulate_input_vector(self, input_vector: dict) -> dict :
        for input in input_vector:
            self.nets[input].value = input_vector[input]
            self.nets[input].apply_value_to_fanouts()
                    
        for out_net in self.gates:
            output_value = self.gates[out_net].perform_logic()
            self.nets[out_net].value = output_value
            self.nets[out_net].apply_value_to_fanouts()

        output_vector = {}
        for output in self.outputs:
            output_vector[output.id] = output.value

        return output_vector
    
    def simulate_deductive_fault(self):
        # Checking if all the nets have a logical value!
        for net in self.nets:
            if self.nets[net].value == 'U' or self.nets[net].value == 'Z':
                print("ALL NETS MUST BE 0/1 FOR DEDUCTIVE TO WORK!")
                return
        # Applying fault to PIs!
        for input in self.inputs:
            input.fault_set = {input.id + "-sa" + str(1-input.value)}
            input.apply_fault_to_fanouts()

        for out_net in self.gates:
            self.nets[out_net].fault_set = self.gates[out_net].perform_deductive_fault_simulation()
            self.nets[out_net].apply_fault_to_fanouts()

    def simulate_random_input(self, include_U_or_Z = False):
        input_vector = {}
        random_pool = []
        if include_U_or_Z:
            random_pool = [1, 0, 'U', 'Z']
        else:
            random_pool = [1, 0]
        for input in self.inputs:
            input_vector[input.id] = random.choice(random_pool)
        
        LogicalCircuit.write_input_vector('random_simulation_input.txt', input_vector)
        self.simulate_input_vector(input_vector)
        self.simulate_deductive_fault()
        self.print_net_values()
        self.print_net_fault_sets()
        self.write_results_to('random_simulation_results.txt')

    def write_input_vector(filename, input_vector):
        with open(filename, 'w') as f:
            for input in input_vector:
                f.write(input + ' ')
            f.write('\n')
            for input in input_vector:
                f.write(str(input_vector[input]) + ' ')
    
    def run(self, filename):
        # reading the input file
        input_vector = {}
        with open(filename, 'r') as f:
            input_ids = f.readline().strip().split(' ')
            input_values = f.readline().strip().split(' ')
            for id, value in zip(input_ids, input_values):
                if value == '1' or value == '0':
                    input_vector[id] = int(value)
                else:
                    input_vector[id] = value
        self.simulate_input_vector(input_vector)
        self.simulate_deductive_fault()
        self.write_results_to("results_of_" + filename + ".txt")


    def print_net_fault_sets(self):
        for net in self.nets:
            print("net : " + net + " -> "+str(self.nets[net].fault_set))
        
    def print_net_values(self):
        for net in self.nets:
            print("net : " + net + " -> "+ str(self.nets[net].value))

    def write_results_to(self, filename):
        with open(filename, 'w') as f:
            f.write('inputs:\n')
            for input in self.inputs:
                f.write('input :' + input.id + " -> " + str(input.value) + '\n')
            f.write('values:\n')
            for net in self.nets:
                f.write("net : " + net + " -> " + str(self.nets[net].value )+ '\n')
            f.write('fault sets:\n')
            for net in self.nets:
                f.write("net : " + net + " -> " + str(self.nets[net].fault_set )+ '\n')
                
inputs, outputs, gates = parse_iscas_bench('test3.txt')
LC = LogicalCircuit(inputs, outputs, gates)
LC.simulate_random_input()
# LC.simulate_random_input(include_U_or_Z=True)



