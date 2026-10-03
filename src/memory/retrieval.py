import os
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

class PolicyRetriever:
    """Lightweight deterministic heading/keyword retriever over official policy markdown files."""
    def __init__(self, policies_dir: Optional[str] = None):
        if policies_dir:
            self.base_dir = Path(policies_dir)
        else:
            mode = os.getenv("NOVAMART_DATA_MODE", "official")
            self.base_dir = Path("public/policies") if mode != "demo" else Path("demo_data/policies")
        
        self.documents = {}
        self._load_documents()

    def _load_documents(self):
        if not self.base_dir.exists():
            return
        for file in self.base_dir.glob("*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self.documents[file.name] = f.read()
            except Exception:
                pass

    def get_policy_version_for_date(self, order_date_str: Optional[str]) -> str:
        if not order_date_str:
            return "v2"
        try:
            # v1 was effective 2026-01-01, v2 is effective 2026-06-01
            date_clean = str(order_date_str).split(" ")[0]
            if date_clean < "2026-06-01":
                return "v1"
            return "v2"
        except Exception:
            return "v2"

    def retrieve_policy_sections(self, intent: str, order_date: Optional[str] = None, keywords: Optional[List[str]] = None) -> List[Dict[str, str]]:
        ver = self.get_policy_version_for_date(order_date)
        intent_lower = intent.lower()
        
        target_files = []
        if any(k in intent_lower for k in ["refund", "money", "debit"]):
            target_files.append(f"refund_policy_{ver}.md")
        if any(k in intent_lower for k in ["return", "replace"]):
            target_files.append(f"return_policy_{ver}.md")
            if "replace" in intent_lower:
                target_files.append("replacement_policy.md")
        if "cancel" in intent_lower:
            target_files.append("cancellation_policy.md")
        if any(k in intent_lower for k in ["delivery", "shipping", "transit", "delay", "address", "otp"]):
            target_files.append("shipping_policy.md")
        if "warranty" in intent_lower:
            target_files.append("warranty_policy.md")
        if any(k in intent_lower for k in ["payment", "cod", "bank", "card", "upi"]):
            target_files.append("payment_policy.md")
        if any(k in intent_lower for k in ["safety", "legal", "human", "escalat", "abuse", "fraud"]):
            target_files.append("customer_escalation_policy.md")

        if not target_files:
            target_files = [f"return_policy_{ver}.md", f"refund_policy_{ver}.md"]

        results = []
        search_terms = [intent_lower]
        if keywords:
            search_terms.extend([k.lower() for k in keywords])

        for fname in target_files:
            content = self.documents.get(fname)
            if not content:
                # Try fallback
                alt_name = fname.replace(f"_{ver}", "_v2") if ver != "v2" else fname
                content = self.documents.get(alt_name)
            if not content:
                continue

            sections = re.split(r'\n(?=##\s+)', content)
            for sec in sections:
                sec_lower = sec.lower()
                score = sum(1 for term in search_terms if term in sec_lower)
                if score > 0 or len(sections) <= 3:
                    # Extract heading
                    lines = sec.strip().split('\n')
                    heading = lines[0].replace('##', '').strip() if lines else fname
                    body = '\n'.join(lines[1:]).strip() if len(lines) > 1 else lines[0]
                    results.append({
                        "file": fname,
                        "heading": heading,
                        "content": body[:600] # Pass only top relevant excerpt
                    })

        return results[:3] # Max 3 sections


class ProductSpecRetriever:
    """Lightweight deterministic retriever over official category product spec files."""
    def __init__(self, specs_dir: Optional[str] = None):
        if specs_dir:
            self.base_dir = Path(specs_dir)
        else:
            mode = os.getenv("NOVAMART_DATA_MODE", "official")
            self.base_dir = Path("public/products") if mode != "demo" else Path("demo_data/products")
        self.specs = {}
        self._load_specs()

    def _load_specs(self):
        if not self.base_dir.exists():
            return
        for file in self.base_dir.glob("*.md"):
            try:
                with open(file, 'r', encoding='utf-8') as f:
                    self.specs[file.stem.lower()] = f.read()
            except Exception:
                pass

    def retrieve_spec(self, category: str, product_id: Optional[str] = None, product_name: Optional[str] = None, query: str = "") -> Dict[str, Any]:
        cat_key = category.lower().strip()
        spec_content = self.specs.get(cat_key)
        if not spec_content:
            # Try partial category matching
            for k in self.specs:
                if k in cat_key or cat_key in k:
                    spec_content = self.specs[k]
                    break

        if not spec_content:
            return {"found": False, "details": "Category specification not found."}

        # Look for product block
        product_section = None
        if product_id:
            pattern = re.compile(rf'##\s+.*?\(({re.escape(product_id)})\)(.*?)(?=\n##\s+|$)', re.DOTALL | re.IGNORECASE)
            match = pattern.search(spec_content)
            if match:
                product_section = match.group(0)

        if not product_section and product_name:
            clean_name = product_name.split('(')[0].strip()
            pattern = re.compile(rf'##\s+.*?{re.escape(clean_name)}.*?\n(.*?)(?=\n##\s+|$)', re.DOTALL | re.IGNORECASE)
            match = pattern.search(spec_content)
            if match:
                product_section = match.group(0)

        if not product_section:
            return {
                "found": False,
                "category": category,
                "details": f"Product details for {product_id or product_name or 'item'} not specified in category specifications."
            }

        # Extract structured details
        extracted_info = {}
        # Parse table rows | Spec | Value |
        table_rows = re.findall(r'\|\s*([^|\n]+?)\s*\|\s*([^|\n]+?)\s*\|', product_section)
        for spec_k, spec_v in table_rows:
            if spec_k.lower() not in ["specification", "field", "---", "--"]:
                extracted_info[spec_k.strip().lower()] = spec_v.strip()

        # Parse bullet points - **Field:** Value
        bullets = re.findall(r'-\s*\*\*([^:]+?):\*\*\s*([^|\n]+)', product_section)
        for bk, bv in bullets:
            extracted_info[bk.strip().lower()] = bv.strip()

        return {
            "found": True,
            "category": category,
            "product_id": product_id,
            "raw_section": product_section[:1000],
            "specifications": extracted_info
        }
