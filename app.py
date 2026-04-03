import streamlit as st
from groq import Groq

# إعدادات الصفحة بستايل احترافي وبسيط
st.set_page_config(page_title="AI Humanizer Elite", page_icon="✍️")

# CSS لتحسين المظهر
st.markdown("""
    <style>
    .stTextArea textarea { border-radius: 15px; border: 1px solid #d4af37; background-color: #1a1a1a; color: white; }
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white; border-radius: 25px; padding: 10px 25px; transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4); }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Humanizer Elite")
st.write("حول تقاريرك الجامعية لنصوص تبدو بشرية 100% (محسّن لـ Llama 3.1)")

# الجانب الجانبي للإعدادات
with st.sidebar:
    st.header("⚙️ Settings")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    model_name = st.selectbox("Select Model:", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    intensity = st.slider("Humanization Intensity:", 0.7, 1.5, 1.2)

input_text = st.text_area("أدخل نص الـ AI هنا:", height=250, placeholder="Paste your lab introduction or essay here...")

if st.button("Humanize Now ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key الخاص بك.")
    elif not input_text:
        st.warning("أدخل نصاً أولاً!")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # البرومبت "الفخم" المطور لكسر الكواشف
            system_msg = """You are a student writing a lab report. Your goal is to rewrite the text to be 100% human-like.
            STRICT RULES:
            1. NEVER use the following 'AI words': 'delve', 'mastermind', 'unassuming', 'shaping our world', 'in essence', 'it's important to note', 'testament'.
            2. USE 'SPOKEN' ENGLISH: Use phrases like 'basically', 'actually', 'honestly', 'pretty much', 'it boils down to'.
            3. BREAK THE FLOW: AI writes smooth, rhythmic sentences. You must be 'clunky'. Use a very short sentence (3-5 words) right after a long one.
            4. CONTRACTIONS ARE MANDATORY: Use (don't, can't, it's, wouldn't, we're) instead of the full forms.
            5. NO DRAMA: Don't try to sound 'inspiring' or 'poetic'. Just explain the logic gates as if you're tired and want to finish the lab.
            6. VOCABULARY: Use simple, direct words. Instead of 'utilize', use 'use'. Instead of 'fundamental', use 'basic'."""

            with st.spinner('جاري كسر بصمة الـ AI...'):
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Rewrite this, making it sound natural and human. Keep the same meaning: {input_text}"}
                    ],
                    temperature=intensity, # تحكم في العشوائية من الـ Slider
                    top_p=0.9,
                    max_tokens=2048
                )
                
                result = completion.choices[0].message.content
                
                st.markdown("---")
                st.subheader("✅ النتيجة البشرية:")
                st.write(result)
                st.caption("نصيحة: إذا كانت النسبة لا تزال عالية، ارفع الـ Intensity قليلاً وأعد المحاولة.")

        except Exception as e:
            st.error(f"حدث خطأ تقني: {str(e)}")

st.markdown("---")
st.info("هذه الأداة صممت لأغراض تعليمية لمساعدة الطلاب على تحسين أسلوب كتابتهم.")
