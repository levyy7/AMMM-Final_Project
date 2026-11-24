import re

def parse_input_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Dictionary to hold scalar integer values
    scalars = {}
    for var_name in ['N', 'L', 'U', 'T']:
        match = re.search(r'^\s*' + var_name + r'\s*=\s*(\d+)', content, re.MULTILINE)
        if not match:
            raise ValueError(f"Could not find integer value for variable '{var_name}'")
        scalars[var_name] = int(match.group(1))

    # Extract single-line or multi-line array for P
    p_match = re.search(r'P\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if not p_match:
        raise ValueError("Could not find array 'P'")
    p_list = [int(x) for x in re.findall(r'\b\d+\b', p_match.group(1))]

    # Extract multi-line matrix/array block for E
    e_match = re.search(r'E\s*=\s*\[(.*?)\];', content, re.DOTALL)
    if not e_match:
        raise ValueError("Could not find array 'E'")
    e_list = [int(x) for x in re.findall(r'\b\d+\b', e_match.group(1))]

    return (
        scalars['N'],
        scalars['L'],
        scalars['U'],
        scalars['T'],
        p_list,
        e_list
    )

class Instance:
    def __init__(self, path):
        self.N, self.L, self.U, self.T, self.P, self.E = parse_input_file(path)
        self.preP = [0] * (self.N + 1)
        self.preE = [0] * (self.N + 1)
        for i in range(1, self.N + 1):
            self.preP[i] = self.preP[i - 1] + self.P[i - 1]
            self.preE[i] = self.preE[i - 1] + self.E[i - 1]

    def profit(self, a, b):
        return self.preP[b] - self.preP[a - 1]

    def energy(self, a, b):
        return self.preE[b] - self.preE[a - 1]

    def candidates(self):
        result = []
        for length in range(self.L, self.U + 1):
            for a in range(1, self.N - length + 2):
                b = a + length -1
                result.append((a, b))
        return result

if __name__ == "__main__":
    inst = Instance("data/project.1.dat")
    print(inst.N, inst.L, inst.U, inst.T)
    print(inst.P)
    print(inst.profit(1,4), inst.energy(1,4))
    print(len(inst.candidates()))