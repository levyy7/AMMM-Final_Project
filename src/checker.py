import argparse
import re
import sys

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


def parse_solution_file(filepath):
    """Parses a file containing lines of space-separated integer pairs."""
    solution = []
    with open(filepath, 'r') as f:
        for line_num, line in enumerate(f, start=1):
            line = line.strip()
            if not line:  # Ignore empty lines
                continue
            
            parts = line.split()
            if len(parts) != 2:
                raise ValueError(f"Line {line_num} in '{filepath}' does not contain exactly two elements: '{line}'")
            
            solution.append((int(parts[0]), int(parts[1])))
            
    return solution


def main():
    parser = argparse.ArgumentParser(description="Check")
    parser.add_argument("first_filename", help="Path to the input file")
    parser.add_argument("second_filename", help="Path to the solution file")
    args = parser.parse_args()

    try:
        N, L, U, T, P, E = parse_input_file(args.first_filename)
        solution = parse_solution_file(args.second_filename)

    except Exception as err:
        print(f"Error reading file: {err}", file=sys.stderr)
        sys.exit(1)

    S = len(solution)
    for i in range(S):
        [ai, bi] = solution[i]

        if ai < 1:
            print(f"Error: time starts at 1", file=sys.stderr)
            sys.exit(1)

        if bi > N:
            print(f"Error: time ends at {N}", file=sys.stderr)
            sys.exit(1)
            
        if ai > bi:
            print(f"Error: {solution[i]} is not well-defined", file=sys.stderr)
            sys.exit(1)

        length = bi - ai + 1
        if L > length:
            print(f"Error: {solution[i]} is too short", file=sys.stderr)
            sys.exit(1)
        if length > U:
            print(f"Error: {solution[i]} is too long", file=sys.stderr)
            sys.exit(1)

        for j in range(i):
            [aj, bj] = solution[j]
            if ai <= bj and aj <= bi:
                print(f"Error: {solution[j]} and {solution[i]} overlap", file=sys.stderr)
                sys.exit(1)

    energy = 0
    profit = 0
    for [a, b] in solution:
        for i in range(a, b+1):
            energy += E[i-1]
            profit += P[i-1]

    print(f"Energy consumption is {energy}")
    print("OK")

    if profit < T:
        print(f"Error: profit is {profit} but should be at least {T}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
