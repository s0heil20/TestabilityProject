def parse_iscas_bench(filename):
    """ Parses an ISCAS .bench file and extracts inputs, outputs, and gate definitions. """
    inputs = []
    outputs = []
    gates = {}

    with open(filename, 'r') as file:
        for line in file:
            # Remove comments and whitespace
            line = line.split('#')[0].strip()

            # Skip empty lines
            if line == '':
                continue

            # Parse inputs
            if line.startswith('INPUT'):
                input_name = line.split('(')[1].split(')')[0].strip()
                inputs.append(input_name)

            # Parse outputs
            elif line.startswith('OUTPUT'):
                output_name = line.split('(')[1].split(')')[0].strip()
                outputs.append(output_name)

            # Parse gate definitions
            elif '=' in line:
                gate_name, gate_func = line.split('=')
                gate_name = gate_name.strip()
                gate_func = gate_func.strip()
                gates[gate_name] = gate_func

    return inputs, outputs, gates

# Usage
inputs, outputs, gates = parse_iscas_bench('c17.bench')

print('Inputs:', inputs)
print('Outputs:', outputs)
print('Gates:', gates)
