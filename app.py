import streamlit as st
import json

st.set_page_config(page_title="סוכן מניות AI", page_icon="📈")
st.title("🚀 סוכן ה-AI: מניות לקראת פריצה")

try:
    with open('agent_memory.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
except:
    data = []

if not data:
    st.warning("הסוכן עדיין לא סיים את הסריקה הראשונה שלו. חזור לכאן מאוחר יותר!")
else:
    st.subheader(f"📅 עדכון אחרון: {data[0]['date']}")
    for stock in data:
        col1, col2, col3 = st.columns(3)
        col1.metric("מניה", stock['ticker'])
        col2.metric("מחיר", f"${stock['price']}")
        col3.metric("סנטימנט", stock['ai_sentiment'])
        st.info(f"**ניתוח ה-AI:** {stock['ai_reasoning']}")
        st.divider()
