import streamlit as st
from groq import Groq

# إعدادات الصفحة بستايل إيثان (Luxara/Beyond Elegance style)
st.set_page_config(page_title="AI Humanizer Elite Pro", page_icon="✍️")

# CSS يدعم اللغتين وتنسيق احترافي (Black & Gold)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&family=Inter:wght@400;600&display=swap');
    
    html, body, [data-testid="stSidebar"], .stMarkdown, .stTextArea textarea {
        font-family: 'Cairo', 'Inter', sans-serif;
    }
    
    .stTextArea textarea { 
        border-radius: 15px; 
        border: 1px solid #d4af37; 
        background-color: #0e1117; 
        color: white;
        direction: auto; 
    }
    
    /* ستايل الأزرار */
    .stButton>button { 
        background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white; border-radius: 25px; padding: 10px 25px; 
        width: 100%; font-weight: bold; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✨ AI Humanizer Elite Pro")
st.write("حول نصوصك لأسلوب بشري فريد أو تقارير رسمية رصينة.")

with st.sidebar:
    st.header("⚙️ الإعدادات")
    api_key = st.text_input("أدخل Groq API Key:", type="password")
    model_name = st.selectbox("النموذج:", ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"])
    
    # اختيار نوع التقرير
    mode = st.radio("اختر نمط الكتابة:", ["بشري عفوي (Student Mode)", "تقرير رسمي (Formal Lab Report)"])
    
    intensity = st.slider("قوة التحويل (Temperature):", 0.7, 1.5, 1.1)

input_text = st.text_area("أدخل النص الأكاديمي أو المسودة هنا:", height=250, placeholder="ضع النص هنا...")

if st.button("تحويل النص الآن ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key.")
    elif not input_text:
        st.warning("الرجاء إدخال نص.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # تحديد البرومبت بناءً على النمط المختار
            if mode == "بشري عفوي (Student Mode)":
                system_msg = """You are a student explaining a concept to a friend. 
                - Be informal, use fillers like 'honestly', 'basically', 'so yeah'.
                - Use a bit of 'messy' structure. 
                - Avoid academic cliches. Sound tired but smart."""
            else:
                system_msg = """You are a professional Academic Engineer writing a formal lab report.
                - Use precise technical terminology.
                - Maintain a professional, objective, and clear tone.
                - Structure the information logically without being robotic.
                - Avoid personal pronouns and conversational fillers."""

            with st.spinner('جاري معالجة النص...'):
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Rewrite this text in the chosen style while keeping technical accuracy: {input_text}"}
                    ],
                    temperature=intensity,
                    top_p=0.9
                )
                
                st.markdown("---")
                st.subheader(f"✅ النتيجة ({mode}):")
                st.write(completion.choices[0].message.content)
                
                # زر للنسخ السريع
                st.button("نسخ النص", on_click=lambda: st.write("تم النسخ (محاكاة)"))
                
        except Exception as e:
            st.error(f"حدث خطأ: {str(e)}")
