import streamlit as st
from groq import Groq

# إعدادات الصفحة
st.set_page_config(page_title="AI Humanizer Elite Pro", page_icon="✍️")

# CSS يدعم اللغتين وتنسيق RTL/LTR تلقائي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Inter:wght@400;600&display=swap');
    
    html, body, .stMarkdown, .stTextArea textarea {
        font-family: 'Cairo', 'Inter', sans-serif;
    }
    
    /* تنسيق صندوق النص ليدعم الاتجاهين */
    .stTextArea textarea { 
        border-radius: 15px; 
        border: 1px solid #d4af37; 
        background-color: #1a1a1a; 
        color: white;
        direction: auto; 
    }
    
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white; border-radius: 25px; padding: 10px 25px; transition: 0.3s;
        width: 100%;
        font-weight: bold;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4); }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Humanizer Elite Pro")
st.write("حول تقاريرك الجامعية (عربي/إنجليزي) لنصوص بشرية 100%.")

# الجانب الجانبي
with st.sidebar:
    st.header("⚙️ Settings / الإعدادات")
    api_key = st.text_input("Enter Groq API Key:", type="password")
    model_name = st.selectbox("Select Model:", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    intensity = st.slider("Humanization Intensity / قوة التحويل:", 0.7, 1.5, 1.2)

input_text = st.text_area("أدخل النص هنا (عربي أو إنجليزي):", height=250, placeholder="Paste your AI text here...")

if st.button("Humanize Now / حول النص الآن ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key.")
    elif not input_text:
        st.warning("الرجاء إدخال نص أولاً.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # البرومبت "الجوهري" الذي يدمج اللغتين وقواعد كسر الـ AI
            system_msg = """You are a bilingual professional human editor. 
            Your goal is to rewrite the input (whether in Arabic or English) to be 100% human-like and bypass AI detectors.

            GENERAL RULES (For both languages):
            1. NO AI CLICHES: In English, avoid 'delve', 'moreover', 'testament'. In Arabic, avoid 'علاوة على ذلك', 'في جوهره', 'يعد هذا'.
            2. VARY SENTENCE LENGTH: Use the 'Short-Long-Short' technique. Break the smooth flow.
            3. BE DIRECT: Use 'spoken' language (Contractions in English like "don't"; Informal links in Arabic like "ببساطة").
            4. TONE: Write as a smart student explaining to a friend. Be slightly informal but keep the technical meaning.
            5. STRUCTURE: Avoid perfect symmetry. Humans are 'messy' writers.
            
            [IF INPUT IS ARABIC]: Use 'White Arabic' (simple Fusha). Use words like 'بصراحة', 'يعني', 'الفكرة إنو'.
            [IF INPUT IS ENGLISH]: Use contractions (it's, we're), simple vocabulary (use 'buy' instead of 'purchase'), and punchy sentences."""

            with st.spinner('جاري معالجة النص...'):
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Rewrite this text to be human-like. Keep the original language and meaning: {input_text}"}
                    ],
                    temperature=intensity,
                    top_p=0.9,
                    max_tokens=2048
                )
                
                result = completion.choices[0].message.content
                
                st.markdown("---")
                st.subheader("✅ النتيجة النهائية:")
                st.write(result)
                
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")

st.markdown("---")
st.info("نصيحة: إذا كان النص تقنياً جداً، يفضل اختيار Intensity حول 1.3 للحصول على أفضل تباين بشري.")
