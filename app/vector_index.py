# Placeholder vector index wrapper. Replace with Chroma/pgvector/FAISS integration.
class VectorMenuIndex:
    def __init__(self):
        # sample in-memory dataset
        self.items = [
            {
                'provider_item_id': 'm1',
                'name': 'Grilled Chicken Bowl',
                'restaurant_name': 'Healthy Bites',
                'price_cents': 29900,
                'calories': 650,
                'macros': {'p':40,'c':60,'f':20},
                'tags': ['gluten-free','high-protein']
            },
            {
                'provider_item_id': 'm2',
                'name': 'Paneer Butter Masala with Rice',
                'restaurant_name': 'Tasty Indian',
                'price_cents': 19900,
                'calories': 900,
                'macros': {'p':20,'c':100,'f':35},
                'tags': ['vegetarian']
            },
            {
                'provider_item_id': 'm3',
                'name': 'Vegan Buddha Bowl',
                'restaurant_name': 'Green Eats',
                'price_cents': 24900,
                'calories': 520,
                'macros': {'p':15,'c':70,'f':18},
                'tags': ['vegan']
            }
        ]

    def search(self, pref, top_k=50):
        # simple filtered search using pref fields
        results = []
        for it in self.items:
            if pref is not None:
                if pref.budget_cents is not None and it.get('price_cents',0) > pref.budget_cents:
                    continue
                if pref.max_calories is not None and it.get('calories',0) > pref.max_calories:
                    continue
                if pref.dietary_restrictions:
                    # if any restriction not in tags, exclude (simple)
                    ok = True
                    for d in pref.dietary_restrictions:
                        if d.lower() not in [t.lower() for t in it.get('tags',[])] and d.lower() != 'vegetarian':
                            # note: this is simplified logic
                            ok = False
                    if not ok:
                        continue
            results.append(it)
        return results[:top_k]
