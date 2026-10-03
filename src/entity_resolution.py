import re
from typing import Dict, Any, List, Optional

class EntityResolver:
    """Deterministic entity resolution following the strict priority:
    1. authenticated customer
    2. current session state
    3. current message
    4. previous conversation
    5. open ticket context
    6. customer's own orders
    """
    def __init__(self, datasets: Optional[Dict[str, Any]] = None):
        self.datasets = datasets

    def resolve(self, customer_id: Optional[str], message: str, session: Any) -> Dict[str, Any]:
        result = {
            "order_id": None,
            "product_id": None,
            "product_name": None,
            "category": None,
            "ticket_id": None,
            "amount_claimed": None,
            "is_ambiguous": False,
            "candidate_matches": {},
            "ownership_error": False,
            "clarification_prompt": None
        }

        msg_lower = message.lower()

        # Step 1: Check if this message resolves an active candidate choice in session
        if session and (session.candidate_orders or session.candidate_products):
            matched_cand = session.resolve_from_candidates(message)
            if matched_cand:
                result["order_id"] = matched_cand.get("order_id")
                result["product_id"] = matched_cand.get("product_id")
                result["product_name"] = matched_cand.get("product_name")
                result["category"] = matched_cand.get("category")
                return result

        # Step 2: Extract explicit identifiers in the current message
        # Order ID pattern: ORD-000001, O001, ORD-12345
        order_match = re.search(r'\b(ORD-\d{4,8}|O\d{3})\b', message, re.IGNORECASE)
        if order_match:
            explicit_oid = order_match.group(1).upper()
            # Verify ownership if customer_id and datasets are available
            if customer_id and self.datasets and "orders" in self.datasets:
                orders_df = self.datasets["orders"]
                matching = orders_df[orders_df["order_id"] == explicit_oid]
                if not matching.empty:
                    owner = matching.iloc[0]["customer_id"]
                    if owner != customer_id:
                        # Belongs to someone else!
                        result["ownership_error"] = True
                        result["order_id"] = explicit_oid
                        return result
                    else:
                        result["order_id"] = explicit_oid
                else:
                    # Order does not exist in db
                    result["order_id"] = explicit_oid
            else:
                result["order_id"] = explicit_oid

        # Product ID pattern: PROD-00001, P001
        prod_match = re.search(r'\b(PROD-\d{4,6}|P\d{3})\b', message, re.IGNORECASE)
        if prod_match:
            result["product_id"] = prod_match.group(1).upper()

        # Ticket ID pattern: TICK-00001, T001
        ticket_match = re.search(r'\b(TICK-\d{4,6}|T\d{3})\b', message, re.IGNORECASE)
        if ticket_match:
            result["ticket_id"] = ticket_match.group(1).upper()

        # Amount extraction: ₹50,000 or 50000 INR
        amt_match = re.search(r'(?:₹|rs\.?|inr)?\s*([0-9]{1,3}(?:,[0-9]{3})*(?:\.[0-9]+)?|[0-9]{3,})\s*(?:₹|rs\.?|inr|rupees)?', message, re.IGNORECASE)
        if amt_match:
            raw_val = amt_match.group(1).replace(',', '')
            try:
                val = float(raw_val)
                # Ignore numbers that look like years or small integers unless prefixed with currency
                if "₹" in message or "inr" in msg_lower or "rs" in msg_lower or "refund" in msg_lower:
                    if val > 10:
                        result["amount_claimed"] = val
            except ValueError:
                pass

        # If order_id already resolved explicitly, return
        if result["order_id"]:
            return result

        # Step 3: Check references to previous session state ("that order", "it", "the item")
        if session and session.active_order and any(w in msg_lower for w in ["that order", "it", "this order", "the order", "same order"]):
            result["order_id"] = session.active_order
            return result

        # Step 4: Resolve semantic references using Customer's own orders
        # E.g. "my last order", "my recent order", "my laptop", "my headphones"
        if customer_id and self.datasets and "orders" in self.datasets:
            cust_orders = self.datasets["orders"][self.datasets["orders"]["customer_id"] == customer_id]
            order_items = self.datasets.get("order_items")
            products = self.datasets.get("products")

            # "my last order" / "recent order"
            if any(w in msg_lower for w in ["my last order", "last order", "recent order", "latest order"]):
                if not cust_orders.empty:
                    sorted_orders = cust_orders.sort_values(by="order_date", ascending=False)
                    result["order_id"] = sorted_orders.iloc[0]["order_id"]
                    return result

            # "the item I mentioned yesterday" / ticket follow-up
            if any(w in msg_lower for w in ["mentioned yesterday", "ticket", "previous conversation"]):
                tickets = self.datasets.get("support_tickets")
                if tickets is not None:
                    cust_tickets = tickets[tickets["customer_id"] == customer_id]
                    if not cust_tickets.empty:
                        sorted_tickets = cust_tickets.sort_values(by="created_at", ascending=False)
                        top_ticket = sorted_tickets.iloc[0]
                        result["ticket_id"] = top_ticket["ticket_id"]
                        if "order_id" in top_ticket and str(top_ticket["order_id"]) != "nan":
                            result["order_id"] = str(top_ticket["order_id"])
                            return result

            # Product/category mentions: "my laptop", "my headphones", "the monitor", "earbuds", "phone"
            known_categories = [
                "laptop", "headphones", "smartphones", "smartphone", "phone",
                "smartwatches", "smartwatch", "watch", "earbuds", "tablets", "tablet",
                "cameras", "camera", "monitors", "monitor", "gaming", "accessories",
                "speakers", "speaker", "keyboards", "keyboard", "mice", "mouse"
            ]

            mentioned_cat = None
            for cat in known_categories:
                if cat in msg_lower:
                    mentioned_cat = cat
                    break

            if mentioned_cat and order_items is not None and products is not None:
                # Find all order items for this customer
                cust_order_ids = cust_orders["order_id"].tolist()
                items_for_cust = order_items[order_items["order_id"].isin(cust_order_ids)]
                # Join with products
                items_with_prod = items_for_cust.merge(products, on="product_id", how="inner")
                
                # Match by category or product name
                prod_col = "product_name" if "product_name" in items_with_prod.columns else ("name" if "name" in items_with_prod.columns else "title")
                prod_series = items_with_prod[prod_col].astype(str).str.lower() if prod_col in items_with_prod.columns else ""
                cat_series = items_with_prod["category"].astype(str).str.lower() if "category" in items_with_prod.columns else ""
                
                cat_filter = items_with_prod[
                    cat_series.str.contains(mentioned_cat, na=False) |
                    prod_series.str.contains(mentioned_cat, na=False)
                ]

                distinct_orders = cat_filter["order_id"].unique()
                if len(distinct_orders) == 1:
                    # Exactly one safe match!
                    result["order_id"] = distinct_orders[0]
                    result["product_id"] = cat_filter.iloc[0]["product_id"]
                    result["product_name"] = cat_filter.iloc[0].get(prod_col, "")
                    result["category"] = cat_filter.iloc[0].get("category", "")
                    return result
                elif len(distinct_orders) > 1:
                    # Multiple matches -> ASK! Never silently select first match!
                    candidate_list = []
                    for _, row in cat_filter.iterrows():
                        candidate_list.append({
                            "order_id": row["order_id"],
                            "product_id": row["product_id"],
                            "product_name": row.get(prod_col, ""),
                            "brand": row.get("brand", ""),
                            "category": row.get("category", "")
                        })
                    result["is_ambiguous"] = True
                    result["candidate_matches"]["orders"] = candidate_list
                    if session:
                        session.set_candidates(orders=candidate_list)
                        session.set_pending("need_order_choice", f"You have {len(distinct_orders)} orders matching '{mentioned_cat}'. Which one are you referring to?")
                    result["clarification_prompt"] = f"I found {len(distinct_orders)} orders matching '{mentioned_cat}'. Could you please specify which order or product brand you mean?"
                    return result

        # Fallback to session active order if still not found and message implies a specific transaction
        if not result["order_id"] and session and session.active_order:
            result["order_id"] = session.active_order

        return result
