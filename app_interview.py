import streamlit as st
import google.generativeai as genai
import random

# --- 1. Page Configuration ---
st.set_page_config(page_title="AI Mock Interviewer", page_icon="🎓", layout="centered")

# --- 2. Secure Backend API Initialization ---
try:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
except Exception:
    st.error("⚠️ System Offline: Developer API Key missing in backend secrets.")
    st.stop()

# --- 3. Enhanced Question Bank (With Hidden Intents) ---
QUESTIONS = [
    {
        "q": "How would your best friend describe you in three words, and why?",
        "intent": "💡 **What they are really asking:** Are you self-aware? What role do you play in your peer group? They don't want to hear 'smart' or 'nice'. They want to hear 'loyal', 'analytical', or 'the problem-solver', backed up by a specific story of what you did for your friend."
    },
    {
        "q": "If you had a free afternoon with no homework and no screens allowed, what would you do?",
        "intent": "💡 **What they are really asking:** Are you intrinsically motivated? Do you have genuine offline hobbies (like reading, building things, or sports)? They want to see intellectual curiosity or passion outside of academics and video games."
    },
    {
        "q": "What is something you’ve changed your mind about recently?",
        "intent": "💡 **What they are really asking:** Are you open-minded and capable of intellectual growth? It's okay to admit you were wrong about something. Focus on *how* and *why* your perspective shifted based on a new experience."
    },
    {
        "q": "Tell me about a time you failed at something or made a mistake. What did you learn?",
        "intent": "💡 **What they are really asking:** How resilient are you? Do you blame others, or do you take responsibility? The 'failure' itself matters less than the specific actions you took to fix it and improve."
    }
]

# --- 4. Session State ---
if 'current_q_obj' not in st.session_state:
    st.session_state.current_q_obj = random.choice(QUESTIONS)

def generate_new_question():
    st.session_state.current_q_obj = random.choice(QUESTIONS)

# --- 5. Clean UI ---
st.markdown("<h3 style='text-align: center; color: #1e293b;'>🎓 AI Admissions Coach</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #64748b;'>Practice your boarding school interview. Get instant feedback and brainstorming guidance.</p>", unsafe_allow_html=True)

st.markdown("##### 🗣️ Interview Question:")
st.info(f"**{st.session_state.current_q_obj['q']}**")

# 💡 新增：启发式折叠面板 (答题前指导)
with st.expander("Need a hint? What is the interviewer actually asking?"):
    st.markdown(st.session_state.current_q_obj['intent'])

st.button("🔄 Shuffle Question", on_click=generate_new_question)

st.write("")
user_answer = st.text_area("Your Answer (Try your best, it doesn't have to be perfect):", height=150, placeholder="Well, I think...")

# --- 6. AI Evaluation & Coaching ---
if st.button("Submit for AI Feedback", type="primary", use_container_width=True):
    if len(user_answer.strip()) < 15:
        st.warning("Please provide a little more detail (at least a sentence or two) so I can help you expand it!")
    else:
        with st.spinner("Analyzing and preparing brainstorming tips..."):
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            
            prompt = f"""
            You are an elite US Boarding School Admissions Coach. You are tough but deeply encouraging.
            A 14-year-old applicant answered this question:
            Question: "{st.session_state.current_q_obj['q']}"
            Applicant's Answer: "{user_answer}"
            
            Evaluate this and guide them to a better answer. Format exactly as follows:
            
            ### 📊 Coach's Evaluation
            
            **1. Authenticity & Depth (Score: X/10):**
            *Feedback:* Be honest about whether this sounds like a real, specific teenager or a generic template. Point out if it lacks a personal story ("Show, don't tell").
            
            **2. The Missed Opportunity:**
            *Feedback:* What is the core weakness of this answer? (e.g., "You stated a fact, but didn't explain the *why* behind it.")
            
            ### 🧠 Let's Brainstorm (How to fix it)
            To make this answer unforgettable, ask yourself these 3 questions. Try to rewrite your answer by picking ONE of these to focus on:
            * [Ask a specific, guiding question to help them dig into their memory, e.g., "Think about your sports or hobbies. Was there ever a time when...?"]
            * [Ask a second guiding question focusing on a personal struggle or detail.]
            * [Ask a third guiding question focusing on their impact on others or intellectual curiosity.]
            """
            
            try:
                response = model.generate_content(prompt)
                st.success("✅ Feedback & Coaching Ready!")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
