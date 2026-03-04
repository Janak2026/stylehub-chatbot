import streamlit as st
from groq import Groq

STORE_CONTEXT = """
You are ShopBot, a friendly customer service assistant for StyleHub - an online fashion store.
Store Information:
- We sell men's and women's clothing, shoes, and accessories
- Free shipping on orders above USD 50
- Standard delivery: 3-5 business days
- Express delivery: 1-2 business days (USD 9.99)
- Return policy: 30 days, free returns
- Sizes available: XS, S, M, L, XL, XXL
- Payment methods: Credit/Debit cards, PayPal, UPI
- Customer support email: support@stylehub.com
- Working hours: Mon-Sat, 9am-6pm IST
Current Offers:
- 20% off on all summer collection
- Buy 2 get 1 free on accessories
- Extra 10% off for first-time customers (code: FIRST10)
Always be helpful, friendly and concise.
"""

st.set_page_config(page_title="ShopBot", page_icon="🛍️")
st.title("🛍️ ShopBot — StyleHub Assistant")
st.caption("Ask me anything about orders, shipping, returns or products!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Type your question here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": STORE_CONTEXT},
                *[{"role": m["role"], "content": m["content"]}
                  for m in st.session_state.messages]
            ]
        )
        reply = response.choices[0].message.content
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
