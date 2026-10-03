import yaml
from pathlib import Path

def load_policies(filepath="config/policies.yaml"):
    base_dir = Path(__file__).resolve().parent.parent
    policy_path = base_dir / filepath
    with open(policy_path, 'r') as f:
        return yaml.safe_load(f)
