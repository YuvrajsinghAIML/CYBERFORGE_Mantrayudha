import os

def update_file(path):
    if not os.path.exists(path): return
    with open(path, 'r') as f: content = f.read()
    
    content = content.replace('import os\\nos.environ["NOVAMART_DATA_MODE"] = "demo"\\ndatasets = load_datasets()', 'import os\nos.environ["NOVAMART_DATA_MODE"] = "demo"\ndatasets = load_datasets()')
        
    with open(path, 'w') as f: f.write(content)

for root, _, files in os.walk('tests'):
    for file in files:
        if file.endswith('.py'):
            update_file(os.path.join(root, file))

print('Tests updated properly')
