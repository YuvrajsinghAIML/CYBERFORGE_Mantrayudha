from typing import Dict, Any, List, Optional
import yaml
from pathlib import Path
from src.policy_engine import PolicyEngine

class PolicyLab:
    def __init__(self, policy_engine: PolicyEngine, config_path: str = 'config/policies_demo_v3.yaml'):
        self.policy_engine = policy_engine
        self.config_path = Path(config_path)

    def load_v3_config(self) -> List[Dict[str, Any]]:
        if not self.config_path.exists():
            return [{'version': 'v3', 'effective_from': '2020-01-01', 'return_window_days': 45, 'restocking_fee_percent': 5}]
        with open(self.config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            versions = data.get('versions', [])
            for v in versions:
                v['effective_from'] = '2020-01-01'
            return versions

    def run_mutation_experiment(self, order_date: str = '2026-05-01', current_date: str = '2026-05-25', item_price: float = 10000.0, category: str = 'laptop') -> Dict[str, Any]:
        base_eligible, base_pol = self.policy_engine.is_eligible_for_return(order_date, current_date)
        base_refund = self.policy_engine.calculate_refund(item_price, category, base_pol)
        
        base_result = {
            'policy_version': base_pol.get('version', 'v2'),
            'window_days': self.policy_engine.calculate_refund_window(base_pol),
            'is_eligible': base_eligible,
            'terminal_move': 'ACT' if base_eligible else 'ANSWER',
            'calculated_refund': base_refund
        }

        v3_versions = self.load_v3_config()
        self.policy_engine.apply_mutation(v3_versions)

        mutated_eligible, mutated_pol = self.policy_engine.is_eligible_for_return(order_date, current_date)
        mutated_refund = self.policy_engine.calculate_refund(item_price, category, mutated_pol)

        mutated_result = {
            'policy_version': mutated_pol.get('version', 'v3'),
            'window_days': self.policy_engine.calculate_refund_window(mutated_pol),
            'is_eligible': mutated_eligible,
            'terminal_move': 'ACT' if mutated_eligible else 'ANSWER',
            'calculated_refund': mutated_refund
        }

        self.policy_engine.restore_base_config()

        return {
            'case_description': f'Return request after 24 days (Order: {order_date}, Current: {current_date}, Category: {category})',
            'base_policy': base_result,
            'mutated_policy': mutated_result,
            'outcome_changed': (base_result['terminal_move'] != mutated_result['terminal_move'] or base_result['calculated_refund'] != mutated_result['calculated_refund']),
            'status': 'success'
        }
