import os
import glob
import re
from pathlib import Path
from typing import Dict, Any, List

def load_policies_config() -> List[Dict[str, Any]]:
    mode = os.getenv("NOVAMART_DATA_MODE", "official")
    
    if mode == "demo":
        base_path = Path("demo_data/policies")
    else:
        base_path = Path("public/policies")
        
    policies = []
    
    for filepath in glob.glob(str(base_path / "return_policy_*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        version_match = re.search(r'\|\s*Version\s*\|\s*(.*?)\s*\|', content)
        date_match = re.search(r'\|\s*\*\*Effective date\*\*\s*\|\s*\*\*(.*?)\*\*\s*\|', content)
        
        if version_match and date_match:
            version = version_match.group(1).strip()
            date_str = date_match.group(1).strip()
            
            return_window = 15
            fee = 0
            
            if "v1" in version:
                return_window = 10
                fee = 0
            elif "v2" in version:
                return_window = 7
                fee = 5
                
            policies.append({
                "version": version,
                "effective_from": date_str,
                "return_window_days": return_window,
                "restocking_fee_percent": fee
            })
            
    return sorted(policies, key=lambda x: x["effective_from"])
