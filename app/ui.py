import streamlit as st
import requests
import os

API = os.getenv('API_URL','http://localhost:8000')

st.set_page_config(page_title='Smart Meal Agent', layout='centered')
st.title('Smart Meal Agent — Demo')

user_id = st.number_input('User ID', value=1, min_value=1, step=1)
budget = st.number_input('Budget (₹)', value=300, min_value=50)
max_cal = st.number_input('Max calories', value=800, min_value=100)

diet = st.multiselect('Dietary restrictions', ['vegan','vegetarian','halal','nut-free'])

if st.button('Get recommendations'):
    payload = {
        'user_id': int(user_id),
        'pref': {
            'budget_cents': int(budget*100),
            'max_calories': int(max_cal),
            'dietary_restrictions': diet
        }
    }
    try:
        r = requests.post(f"{API}/recommend", json=payload, timeout=10).json()
        recs = r.get('recommendations', [])
        for rec in recs:
            st.subheader(f"{rec.get('name')} — {rec.get('restaurant')}")
            st.write(f"Price: ₹{rec.get('price_cents',0)/100}")
            st.write(f"Calories: {rec.get('calories')}")
            st.write(rec.get('why_recommended',''))
            if st.button(f"Order {rec.get('name')}", key=rec.get('item_id')):
                order_payload = {
                    'user_id': int(user_id),
                    'provider': 'mock',
                    'restaurant_id': rec.get('restaurant'),
                    'items': [{'provider_item_id': rec.get('item_id'), 'qty':1, 'price_cents': rec.get('price_cents',0)}],
                    'address': {'line1':'Demo Address','city':'Chennai'}
                }
                o = requests.post(f"{API}/order", json=order_payload, timeout=10).json()
                st.success(f"Order Response: {o}")
    except Exception as e:
        st.error(str(e))
