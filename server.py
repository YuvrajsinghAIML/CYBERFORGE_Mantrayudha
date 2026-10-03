import json
import os
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Any

from db.dataset_loader import load_datasets
from config.config_loader import load_policies_config
from src.tools import Tools
from src.policy_engine import PolicyEngine
from src.action_log import ActionLog
from src.decision.verify import Verifier
from src.decision.decider import Decider
from src.decision.guardrail import Guardrail
from src.pipeline import Pipeline
from src.memory.session import SessionMemory
from src.adversarial_runner import AdversarialRunner
from src.eval_runner import EvaluationRunner
from src.policy_lab import PolicyLab

# Global state for server
print('Initializing NovaMart authoritative backend pipeline...')
DATASETS = load_datasets()
ACTION_LOG = ActionLog()
POLICIES_CFG = load_policies_config()
versions = POLICIES_CFG if isinstance(POLICIES_CFG, list) else POLICIES_CFG.get('versions', [])
if not versions:
    versions = [
        {'version': 'v1', 'effective_from': '2026-01-01', 'return_window_days': 15, 'restocking_fee_percent': 0},
        {'version': 'v2', 'effective_from': '2026-06-01', 'return_window_days': 7, 'restocking_fee_percent': 10}
    ]
POLICY_ENGINE = PolicyEngine(versions)
TOOLS = Tools(DATASETS, ACTION_LOG, POLICY_ENGINE)
VERIFIER = Verifier(TOOLS)
DECIDER = Decider(VERIFIER, POLICY_ENGINE)
GUARDRAIL = Guardrail(TOOLS)
PIPELINE = Pipeline(TOOLS, VERIFIER, POLICY_ENGINE, DECIDER, GUARDRAIL)

ADVERSARIAL_RUNNER = AdversarialRunner(PIPELINE)
EVAL_RUNNER = EvaluationRunner(PIPELINE)
POLICY_LAB = PolicyLab(POLICY_ENGINE)

SESSIONS: Dict[str, SessionMemory] = {}

class NovaMartHandler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        path = self.path.split('?')[0]

        if path in ['/health', '/api/status']:
            res = {
                'status': 'healthy',
                'dataset_mode': os.getenv('NOVAMART_DATA_MODE', 'official'),
                'records': {
                    'customers': len(DATASETS.get('customers', [])),
                    'orders': len(DATASETS.get('orders', [])),
                    'order_items': len(DATASETS.get('order_items', [])),
                    'products': len(DATASETS.get('products', [])),
                    'support_tickets': len(DATASETS.get('support_tickets', [])),
                    'reviews': len(DATASETS.get('reviews', [])),
                    'conversations': len(DATASETS.get('conversations', []))
                }
            }
            self._respond_json(res)

        elif path in ['/customers', '/api/customers']:
            custs = []
            cdf = DATASETS.get('customers')
            odf = DATASETS.get('orders')
            if cdf is not None:
                for idx, c in cdf.head(10).iterrows():
                    cid = c['customer_id']
                    c_orders = odf[odf['customer_id'] == cid]['order_id'].tolist() if odf is not None else []
                    custs.append({
                        'customer_id': cid,
                        'name': c.get('name', cid),
                        'email': c.get('email', ''),
                        'status': c.get('status', 'active'),
                        'loyalty_tier': c.get('loyalty_tier', 'standard'),
                        'sample_orders': c_orders[:4]
                    })
            self._respond_json({'customers': custs})

        elif path in ['/eval', '/api/eval']:
            c_active = 'CUST-00001'
            o_active = 'ORD-000001'
            c_suspended = 'CUST-00003'
            o_suspended = 'ORD-000003'
            res = EVAL_RUNNER.run_evaluation(c_active, o_active, c_suspended, o_suspended)
            self._respond_json(res)

        else:
            self._respond_json({'error': 'Not found'}, status=404)

    def do_POST(self):
        path = self.path.split('?')[0]

        try:
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length).decode('utf-8')
            data = json.loads(body) if body else {}
        except Exception as e:
            self._respond_json({'error': f'Invalid JSON: {str(e)}'}, status=400)
            return

        if path in ['/chat', '/api/chat']:
            customer_id = data.get('customer_id', 'CUST-00001')
            message = data.get('message', '')
            now = data.get('current_date', '2026-06-10')
            session_id = data.get('session_id') or customer_id

            if session_id not in SESSIONS:
                SESSIONS[session_id] = SessionMemory()
            session = SESSIONS[session_id]

            reply, decisions, trace, session = PIPELINE.handle_message(customer_id, message, now, session)

            res = {
                'reply': reply,
                'decisions': decisions,
                'session': {
                    'active_order': getattr(session, 'active_order', None),
                    'active_product': getattr(session, 'active_product', None),
                    'active_intent': getattr(session, 'active_intent', None),
                    'pending': getattr(session, 'pending', 'null'),
                    'messages_count': len(getattr(session, 'history', []))
                },
                'trace': {
                    'understanding': trace.understanding.model_dump() if hasattr(trace.understanding, 'model_dump') else vars(trace.understanding),
                    'verification': trace.verification,
                    'decisions': trace.decisions,
                    'tool_calls': trace.tool_calls,
                    'metrics': trace.metrics
                },
                'metrics': trace.metrics
            }
            self._respond_json(res)

        elif path in ['/attack', '/api/attack']:
            c_active = data.get('customer_id', 'CUST-00001')
            o_active = data.get('order_id', 'ORD-000001')
            res = ADVERSARIAL_RUNNER.run_all(c_active, o_active)
            self._respond_json(res)

        elif path in ['/policy-lab', '/api/policy-lab']:
            order_date = data.get('order_date', '2026-05-01')
            current_date = data.get('current_date', '2026-05-25')
            item_price = float(data.get('item_price', 10000.0))
            category = data.get('category', 'laptop')
            res = POLICY_LAB.run_mutation_experiment(order_date, current_date, item_price, category)
            self._respond_json(res)

        else:
            self._respond_json({'error': 'Not found'}, status=404)

    def _respond_json(self, data: Any, status: int = 200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self._send_cors()
        self.end_headers()
        self.wfile.write(json.dumps(data, default=str).encode('utf-8'))

def run_server(port=8080):
    server = HTTPServer(('0.0.0.0', port), NovaMartHandler)
    print(f'NovaMart AI Backend running on port {port} (CORS enabled)')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('Shutting down server...')
        server.server_close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8080)
    args = parser.parse_args()
    run_server(args.port)
