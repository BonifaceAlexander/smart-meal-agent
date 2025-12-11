import uuid
from typing import Dict, Any


class MCPAdapter:
    def create_order_payload(self, restaurant_id, items, address) -> Dict[str, Any]:
        raise NotImplementedError

    def place_order(self, payload) -> Dict[str, Any]:
        raise NotImplementedError

    def get_order_status(self, provider_order_id):
        raise NotImplementedError


class MockMCPAdapter(MCPAdapter):
    def create_order_payload(self, restaurant_id, items, address):
        # Transform internal items to provider format
        return {
            "restaurant_id": restaurant_id,
            "items": items,
            "address": address,
            "idempotency_key": str(uuid.uuid4()),
        }

    def place_order(self, payload):
        # Simulate provider response
        return {
            "status": "ok",
            "provider_order_id": str(uuid.uuid4()),
            "total_cents": sum(
                int(i.get("qty", 1)) * int(i.get("price_cents", 0))
                for i in payload.get("items", [])
            ),
            "raw": payload,
        }

    def get_order_status(self, provider_order_id):
        return {"provider_order_id": provider_order_id, "status": "delivered"}


class MCPAdapterFactory:
    def __init__(self):
        self.adapters = {"mock": MockMCPAdapter()}

    def get_adapter(self, provider_name: str):
        return self.adapters.get(provider_name)
