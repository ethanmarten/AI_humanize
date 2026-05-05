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
st.write("أداة إيثان الخاصة لتحويل النصوص إلى أسلوب بشري مع التحكم الكامل في الطول.")

with st.sidebar:
    st.header("⚙️ الإعدادات التقنية")
    api_key = st.text_input("أدخل Groq API Key:", type="password")
    
    model_name = st.selectbox("النموذج (يفضل 8b للتقرير):", ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"])
    
    mode = st.radio("اختر وضع التعديل:", ["Creative", "Professional", "Scientific/Technical Summary"])
    
    st.markdown("---")
    st.header("📏 التحكم في الطول")
    
    # خيار لتحديد نوع القيد (كلمات أم جمل)
    length_type = st.selectbox("القيد بناءً على:", ["عدد الكلمات", "عدد الجمل", "نفس طول النص الأصلي"])
    
    length_val = 0
    if length_type != "نفس طول النص الأصلي":
        length_val = st.number_input(f"أدخل {length_type} المطلوب:", min_value=10, max_value=2000, value=150)

    intensity = st.slider("قوة التحويل (Temperature):", 0.7, 1.5, 1.2)
    st.info("نصيحة: استخدم 1.2 للحصول على أقل نسبة كشف AI.")

input_text = st.text_area("أدخل النص الأصلي هنا:", height=250, placeholder="ضع النص هنا...")

if st.button("تحويل النص الآن ✨"):
    if not api_key:
        st.error("الرجاء إدخال API Key.")
    elif not input_text:
        st.warning("الرجاء إدخل نص.")
    else:
        try:
            client = Groq(api_key=api_key)
            
            # إعداد رسالة القيد للطول
            if length_type == "عدد الكلمات":
                length_instruction = f"The output must be approximately {length_val} words long."
            elif length_type == "عدد الجمل":
                length_instruction = f"The output must consist of exactly or very close to {length_val} sentences."
            else:
                length_instruction = "Keep the output length similar to the original text."

            # البرومبتس
            if mode == "Creative":
                system_msg = """
                Role: A university student (Ethan) talking casually.
                Goal: 0% AI Detection.
                Strategy: 
                - Use very casual transitions: 'Anyway', 'So basically', 'The thing is'.
                - Add 'Self-Correction': (e.g., "I used a loop—wait, no, I actually just used simple math").
                - Avoid perfect grammar. Use contractions like 'gonna', 'it's', 'would've'.
                - Structure: Write like a stream of consciousness. One thought leads to another without clear headers.
                - Vibe: Sound slightly tired, using human-like filler words.
                """

            elif mode == "Professional":
                system_msg = """
                Role: A practical Engineer/Developer with years of experience.
                Goal: Bypass AI while staying formal.
                Strategy:
                - Avoid 'AI fluff' like "In conclusion" or "It is important to note".
                - Use 'Direct Action' verbs: "I opted for", "We implemented", "I saw a performance gain by...".
                - Add 'Technical Reasoning': Mention why you didn't do it another way.
                - Use varied sentence lengths. A long technical explanation followed by a short summary sentence.
                - Tone: Expert but personal. Not a textbook.
                """

            elif mode == "Scientific/Technical Summary":
                system_msg = """
                Role: A Computer Science student writing a quick lab reflection.
                Objective: BYPASS ALL AI DETECTORS by being 'perfectly imperfect'.
                
                RULES:
                1. Use 'I' or 'We' constantly. (e.g., "I figured out that...", "We ran into this...").
                2. VARIED SENTENCE LENGTH: Use a very long sentence followed by a short, 3-4 word sentence.
                3. NO ROBOT TRANSITIONS: Ban 'Firstly', 'Moreover', 'In conclusion'. Use 'So', 'Basically', 'The thing is'.
                4. LOGIC OVER SYNTAX: Explain the thinking process. "I was going to use a loop but honestly, modulo is just faster for this."
                5. ADD 'CONTEXTUAL NOISE': Mention something specific like "handling memory" or "the C++ math library".
                6. Avoid lists. Write in continuous, slightly disorganized paragraphs to mimic human writing pressure.
                """

            with st.spinner('جاري كسر نمط الذكاء الاصطناعي وضبط الطول...'):
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_msg},
                        {"role": "user", "content": f"Rewrite this text while keeping technical accuracy but making it sound 100% human. {length_instruction}: {input_text}"}
                    ],
                    temperature=intensity,
                    top_p=0.85
                )
                
                st.markdown("---")
                st.subheader(f"✅ النتيجة ({mode}):")
                result = completion.choices[0].message.content
                st.write(result)
                
                # حسابات سريعة للمستخدم
                word_count = len(result.split())
                st.caption(f"📊 الإحصائيات: عدد الكلمات التقريبي: {word_count}")
                st.caption("💡 نصيحة: أضف جملة شخصية واحدة يدوياً لخفض نسبة الكشف إلى 0%.")
                
        except Exception as e:
            st.error(f"حدث خطأ: {e}")
