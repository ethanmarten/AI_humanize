import streamlit as st
from groq import Groq

# إعداد واجهة المستخدم بلمسة Minimalist
st.set_page_config(page_title="AI Humanizer", page_icon="✨")

st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 10px; border: 1px solid #d4af37; }
    .stButton>button { background: linear-gradient(45deg, #d4af37, #f4e0a1); color: black; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("✍️ AI Humanizer Pro")
st.write("حول نصوص الذكاء الاصطناعي إلى نصوص بشرية بضغطة زر.")

# إدخال المفتاح (يمكنك وضعه كـ Secret في Streamlit Cloud لاحقاً)
api_key = st.sidebar.text_input("Enter Groq API Key:", type="password")

input_text = st.text_area("النص الأصلي:", height=200)

if st.button("Humanize ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key من موقع Groq أولاً.")
    elif input_text:
        try:
            client = Groq(api_key=api_key)
            
            # البرومبت الاحترافي لكسر كواشف الـ AI
            completion = client.chat.completions.create(
                model="llama3-8b-8192", # أو gemma2-9b
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional human editor. Rewrite the input to sound natural, conversational, and varied in structure. Avoid AI patterns. High perplexity and burstiness are required."
                    },
                    {"role": "user", "content": input_text}
                ],
                temperature=0.9,
                top_p=1,
            )
            
            result = completion.choices[0].message.content
            st.markdown("---")
            st.success("النتيجة البشرية:")
            st.write(result)
            
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
    else:
        st.warning("أدخل نصاً للمعالجة.")
