import yaml
import glob
from pathlib import Path

class PolicyConfigError(Exception):
    pass

def load_policies_config(filepath="config/policies.yaml"):
    base_dir = Path(__file__).resolve().parent.parent
    policy_path = base_dir / filepath
    if not policy_path.exists():
        raise PolicyConfigError(f"Policy config not found: {policy_path}")
    with open(policy_path, 'r') as f:
        return yaml.safe_load(f)

def discover_policy_documents(public_dir="public"):
    base_dir = Path(__file__).resolve().parent.parent
    policies_dir = base_dir / public_dir / "policies"
    if not policies_dir.exists():
        raise PolicyConfigError(f"Policies directory not found: {policies_dir}")
        
    documents = {}
    for filepath in policies_dir.glob("*.md"):
        with open(filepath, 'r', encoding='utf-8') as f:
            documents[filepath.stem] = f.read()
            
    if not documents:
        raise PolicyConfigError(f"No policy documents found in {policies_dir}")
        
    return documents
