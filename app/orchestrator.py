import json
from typing import List
try:
    from langchain.llms import OpenAI
    from langchain.chains import LLMChain
    from langchain.prompts import PromptTemplate
    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False

from app.mcp_adapters import MCPAdapterFactory
from app.vector_index import VectorMenuIndex

class Orchestrator:
    def __init__(self):
        self.llm_enabled = LLM_AVAILABLE
        if self.llm_enabled:
            self.llm = OpenAI(temperature=0.2)
            self.prompt = PromptTemplate(
                input_variables=["user_pref","retrieved_menu_snippets"],
                template="""You are a meal recommendation assistant.
User preferences:
{user_pref}

Menu:
{retrieved_menu_snippets}

Return JSON array of best 5 suggestions with:
item_id, name, restaurant, price_cents, calories, macros, why_recommended.
"""
            )
            self.chain = LLMChain(llm=self.llm, prompt=self.prompt)
        else:
            self.chain = None

        self.index = VectorMenuIndex()
        self.adapter_factory = MCPAdapterFactory()

    def recommend_meals(self, user_id:int, pref, limit=5):
        # get candidates from index (structured filters + semantic)
        hits = self.index.search(pref, top_k=50)
        snippets = "\n".join([f"{h['name']} | {h.get('price_cents')} | {h.get('calories')} | {h.get('tags','[]')}" for h in hits])

        if self.llm_enabled and self.chain:
            try:
                result = self.chain.run({
                    "user_pref": str(pref.dict()),
                    "retrieved_menu_snippets": snippets
                })
                parsed = json.loads(result)
                return {"recommendations": parsed}
            except Exception:
                pass

        # Fallback deterministic shortlist
        shortlist = hits[:limit]
        recs = []
        for h in shortlist:
            recs.append({
                "item_id": h.get("provider_item_id"),
                "name": h.get("name"),
                "restaurant": h.get("restaurant_name"),
                "price_cents": h.get("price_cents"),
                "calories": h.get("calories"),
                "macros": h.get("macros"),
                "why_recommended": "Meets basic filters"
            })
        return {"recommendations": recs}

    def place_order(self, user_id:int, provider:str, restaurant_id:str, items:List[dict], address:dict):
        adapter = self.adapter_factory.get_adapter(provider)
        if adapter is None:
            raise Exception(f"No adapter for provider {provider}")
        payload = adapter.create_order_payload(restaurant_id, items, address)
        resp = adapter.place_order(payload)
        return resp

    def post_order_tasks(self, order_info):
        # placeholder for post-order polling/notifications
        return
