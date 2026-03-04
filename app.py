import streamlit as st
import anthropic

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ShopSmart AI Assistant",
    page_icon="🛍️",
    layout="centered"
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; }
    .chat-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 20px;
        text-align: center;
    }
    .chat-header h1 { font-size: 1.8rem; margin: 0; }
    .chat-header p  { font-size: 0.95rem; margin: 6px 0 0; opacity: 0.9; }
    .faq-chip {
        display: inline-block;
        background: #fff;
        border: 1px solid #667eea;
        color: #667eea;
        border-radius: 20px;
        padding: 6px 14px;
        margin: 4px;
        font-size: 0.82rem;
        cursor: pointer;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="chat-header">
    <h1>🛍️ ShopSmart AI Assistant</h1>
    <p>Instant answers about orders, shipping, returns & more — 24/7</p>
</div>
""", unsafe_allow_html=True)

# ── System prompt with 10 real Q&As ──────────────────────────────────────────
SYSTEM_PROMPT = """You are a friendly, helpful AI customer support assistant for ShopSmart — 
an online fashion and lifestyle e-commerce store. You are knowledgeable, concise, and always 
professional. You help customers with questions about orders, shipping, returns, products, 
payments, and account issues.

Here are the key facts about ShopSmart you must use when answering:

SHIPPING & DELIVERY:
Q: How long does standard shipping take?
A: Standard shipping takes 5–7 business days. Express shipping (2–3 days) is available for $9.99. 
   Free standard shipping on all orders over $50.

Q: Do you ship internationally?
A: Yes! We ship to 40+ countries. International orders take 10–14 business days. 
   Duties and taxes are the buyer's responsibility.

Q: How do I track my order?
A: Once your order ships, you'll receive a tracking email with a link. 
   You can also log in to your account and visit 'My Orders' to track in real time.

RETURNS & REFUNDS:
Q: What is your return policy?
A: We offer a 30-day hassle-free return policy. Items must be unworn, unwashed, 
   and in original packaging. Sale items are final sale and cannot be returned.

Q: How long does a refund take?
A: Refunds are processed within 3–5 business days after we receive your return. 
   It may take an additional 3–5 days to appear on your bank statement.

Q: Can I exchange an item for a different size?
A: Yes! We offer free size exchanges within 30 days. Just start a return online 
   and select 'Exchange' — we'll ship the new size at no extra cost.

ORDERS & PAYMENTS:
Q: What payment methods do you accept?
A: We accept Visa, Mastercard, Amex, PayPal, Apple Pay, and Google Pay. 
   We also offer Buy Now Pay Later via Klarna (4 interest-free installments).

Q: Can I cancel or modify my order?
A: Orders can be cancelled or modified within 1 hour of placing them. 
   After that, they enter fulfilment and cannot be changed. Contact support immediately.

Q: I received the wrong item — what do I do?
A: We're so sorry! Email support@shopsmart.com with your order number and a photo 
   of the wrong item. We'll ship the correct item and cover return shipping — no cost to you.

ACCOUNT & LOYALTY:
Q: Do you have a loyalty or rewards program?
A: Yes! ShopSmart Rewards gives you 1 point per $1 spent. Every 100 points = $5 off. 
   You also get early access to sales and a birthday discount. Sign up is free.

GENERAL GUIDELINES:
- Be warm, helpful, and solution-oriented
- If you don't know something specific, say so and offer to connect them with the human support team at support@shopsmart.com
- Keep answers concise but complete
- Always end with a follow-up like "Is there anything else I can help you with?"
- Never make up facts not listed above
"""

# ── FAQ quick-buttons ─────────────────────────────────────────────────────────
FAQ_QUESTIONS = [
    "How long does shipping take?",
    "What's your return policy?",
    "How do I track my order?",
    "Can I cancel my order?",
    "Do you ship internationally?",
    "What payment methods do you accept?",
]

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

if "faq_clicked" not in st.session_state:
    st.session_state.faq_clicked = None

# ── FAQ chips ─────────────────────────────────────────────────────────────────
st.markdown("**💡 Common questions — click to ask:**")
cols = st.columns(3)
for i, q in enumerate(FAQ_QUESTIONS):
    if cols[i % 3].button(q, key=f"faq_{i}", use_container_width=True):
        st.session_state.faq_clicked = q

# ── Display chat history ──────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Handle FAQ click or typed input ──────────────────────────────────────────
user_input = st.chat_input("Ask me anything about your order or our store...")

# FAQ button overrides text input
if st.session_state.faq_clicked:
    user_input = st.session_state.faq_clicked
    st.session_state.faq_clicked = None

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call Claude API
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY env var

                response = client.messages.create(
                    model="claude-opus-4-6",
                    max_tokens=512,
                    system=SYSTEM_PROMPT,
                    messages=[
                        {"role": m["role"], "content": m["content"]}
                        for m in st.session_state.messages
                    ],
                )
                reply = response.content[0].text
                st.markdown(reply)
                st.session_state.messages.append({"role": "assistant", "content": reply})

            except Exception as e:
                err = f"⚠️ Could not reach the AI. Error: {e}"
                st.error(err)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🛍️ ShopSmart Support")
    st.markdown("""
    **Store Hours**  
    Mon–Fri: 9am – 6pm EST  
    Sat–Sun: 10am – 4pm EST
    
    **Contact Us**  
    📧 support@shopsmart.com  
    📞 1-800-SHOP-123
    
    **Quick Links**  
    🔗 [Track Your Order](#)  
    🔗 [Start a Return](#)  
    🔗 [Size Guide](#)  
    🔗 [ShopSmart Rewards](#)
    """)
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    st.caption("Powered by Claude AI · Built by Jana Rao")
