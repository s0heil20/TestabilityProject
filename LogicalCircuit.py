import re
from Connection import Connection
from Gate import *
from ParserIscas import parse_iscas_bench

class LogicalCircuit:

    def __init__(self, inputs: list, outputs: list, gates: dict):
        self.gates = {}
        self.nets = {}
        self.outputs = []
        for input in inputs:
            new_input = Connection(input, "IN")
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
            inputs_of_gate = [self.nets[input] for input in gate_inputs]

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
            
        for out_net in self.gates:
            output_value = self.gates[out_net].perform_logic()
            self.nets[out_net].value = output_value

        output_vector = {}
        for output in self.outputs:
            output_vector[output.id] = output.value

        return output_vector
    
    def print_net_values(self):
        for net in self.nets:
            print("net : " + net + " -> "+ str(self.nets[net].value))


inputs, outputs, gates = parse_iscas_bench('c17.bench')
LC = LogicalCircuit(inputs, outputs, gates)
LC.simulate_input_vector( {'1': 1, '2': 0, '3': 1, '6': 1, '7': 1})
LC.print_net_values()

