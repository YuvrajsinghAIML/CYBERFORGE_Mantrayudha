import os
import yaml
from pathlib import Path
from typing import Dict, Any, List

def load_policies_config() -> List[Dict[str, Any]]:
    mode = os.getenv("NOVAMART_DATA_MODE", "official")
    
    if mode == "demo":
        base_path = Path("demo_data/policies")
    else:
        base_path = Path("public/policies")
        
    if not base_path.exists():
        # Fallback to local config if no markdown policies exist, to avoid breaking logic that depends on yaml
        config_path = Path("config/policies.yaml")
        if config_path.exists():
            with open(config_path, "r") as f:
                config = yaml.safe_load(f)
                return config.get("versions", [])
        return []
        
    # Example logic to discover actual markdown policies and version structures
    policies = []
    # For now, just load the fallback YAML since markdown parsing logic depends on the specific structure
    config_path = Path("config/policies.yaml")
    if config_path.exists():
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)
            policies = config.get("versions", [])
            
    return policies
