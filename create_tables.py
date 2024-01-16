import itertools
import ParserIscas
from tabulate import tabulate
from LogicalCircuit import LogicalCircuit
def generate_binary_permutations(n):
    return list(itertools.product([0, 1], repeat=n))

class FaultTable:

    def __init__(self, inputs, outputs, gates, permutations) -> None:
        self.fault_table = {}
        self.test_set = []
        self.inputs = inputs
        self.outputs = outputs
        self.gates = gates
        self.permutations = permutations
        self.covers_all_faults = None

    def create_all_faults(self, ):
        # Get the list of all faults
        input_vector = {}
        input_size = len(self.inputs)
        for i in range(input_size):
            input_vector[self.inputs[i]] = self.permutations[0][i]
        LC = LogicalCircuit(self.inputs, self.outputs, self.gates)
        LC.run(input_vector)

        faults_list = []
        for net in list(LC.nets.keys()):
            faults_list.append(net + '-sa0')
            faults_list.append(net + '-sa1')
        return faults_list

    def create_fault_table(self,):
        faults_list = self.create_all_faults()

        for p in self.permutations:
            input_vector = {}
            for i in range(input_size):
                input_vector[self.inputs[i]] = p[i]
            LC = LogicalCircuit(self.inputs, self.outputs, self.gates)
            LC.run(input_vector)
            table_row = {}
            # Get covered faults
            covered_faults = set()
            for output in self.outputs:
                covered_faults.update(LC.nets[output].fault_set)
            
            for fault in faults_list:
                if fault in covered_faults:
                    table_row[fault] = 'Yes'
                else:
                    table_row[fault] = 'No'
            self.fault_table[p] = table_row
        

    def get_test_vectors(self, ):
        faults_list = self.create_all_faults()

        for p in self.permutations:
            if not faults_list:
                break
            covered_faults_in_set = [key for key, value in self.fault_table[p].items() if value == 'Yes']
            common_elements = set(faults_list).intersection(set(covered_faults_in_set))
            if not common_elements:
                continue
            self.test_set.append(p)
            for element in common_elements:
                try:
                    faults_list.remove(element)
                except ValueError:
                    pass
        if faults_list:
            self.covers_all_faults = False
        else:
            self.covers_all_faults = True

# All the permutations 
inputs, outputs, gates = ParserIscas.parse_iscas_bench("test3.txt")
input_size = len(inputs)
permutations = generate_binary_permutations(input_size)
fault_table = FaultTable(inputs, outputs, gates, permutations)
fault_table.create_fault_table()
fault_table.get_test_vectors()
print(fault_table.covers_all_faults)