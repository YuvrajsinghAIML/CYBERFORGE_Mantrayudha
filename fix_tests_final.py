import os

def fix_test_file(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    
    with open(path, 'w') as f:
        for line in lines:
            if 'import os' in line and 'NOVAMART_DATA_MODE' in line:
                continue
            if 'os.environ["NOVAMART_DATA_MODE"]' in line:
                continue
            if 'datasets = load_datasets()' in line:
                indent = line[:len(line) - len(line.lstrip())]
                f.write(f'{indent}import os\n')
                f.write(f'{indent}os.environ["NOVAMART_DATA_MODE"] = "demo"\n')
                f.write(f'{indent}datasets = load_datasets()\n')
            else:
                f.write(line)

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            fix_test_file(os.path.join(root, file))

print("Fixed test files.")
