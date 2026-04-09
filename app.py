import streamlit as st
from groq import Groq

# إعدادات الصفحة بستايل إيثان المفضل
st.set_page_config(page_title="AI Humanizer Elite Pro", page_icon="✍️")

# CSS يدعم اللغتين وتنسيق احترافي
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Inter:wght@400;600&display=swap');
    
    html, body, .stMarkdown, .stTextArea textarea {
        font-family: 'Cairo', 'Inter', sans-serif;
    }
    
    .stTextArea textarea { 
        border-radius: 15px; 
        border: 1px solid #d4af37; 
        background-color: #1a1a1a; 
        color: white;
        direction: auto; 
    }
    
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white; border-radius: 25px; padding: 10px 25px; 
        width: 100%; font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Humanizer Elite Pro")
st.write("حول نصوصك الأكاديمية (عربي/إنجليزي) لأسلوب بشري 100% يصعب كشفه.")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل Groq API Key:", type="password")
    model_name = st.selectbox("النموذج:", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    intensity = st.slider("قوة التحويل (Intensity):", 0.7, 1.5, 1.3) # رفعنا الافتراضي لـ 1.3 لنتائج أقوى

input_text = st.text_area("أدخل النص هنا:", height=250, placeholder="ضع النص هنا...")

if st.button("تحويل النص الآن ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key.")
    elif not input_text:
        st.warning("الرجاء إدخال نص.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # البرومبت اللي جاب نتيجة 0% و 17% اللي جربناهم
            system_msg = """You are a student explaining a concept to a peer. Your goal is to be 100% human and pass AI detection.

            RULES:
            1. Language: Use simple, everyday language (White Arabic or Conversational English).
            2. Anti-AI Cliches: NEVER use words like 'furthermore', 'delve', 'moreover' in English, or 'علاوة على ذلك', 'في جوهره' in Arabic.
            3. Conversational Markers: Use filler phrases. (English: "honestly", "basically", "so yeah"). (Arabic: "بصراحة", "الفكرة إنو", "ببساطة").
            4. Sentence Variety: Use a very short sentence immediately after a long one.
            5. Tone: Sound a bit tired or informal, like a real student, not a professor. 
            6. Structure: Be slightly 'messy'. Don't be too organized or overly logical.
            """

            with st.spinner('جاري معالجة النص...'):
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Humanize this text while keeping the exact technical meaning: {input_text}"}
                    ],
                    temperature=intensity,
                    top_p=0.9
                )
                
                st.markdown("---")
                st.subheader("✅ النتيجة البشرية:")
                st.write(completion.choices[0].message.content)
                
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
