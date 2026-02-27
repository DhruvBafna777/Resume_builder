import streamlit as st
import os
from groq import Groq

if "GROQ_API_KEY" in st.secrets:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
else:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=GROQ_API_KEY)

# --- UI ENHANCEMENT 1: Page Config & Custom CSS ---
st.set_page_config(page_title="AI Resume Builder Pro", page_icon="💼", layout="wide")

# Injecting some basic CSS to make buttons and headers pop
st.markdown("""
<style>
    .stButton>button {
        background-color: #4CAF50; 
        color: white; 
        font-weight: bold; 
        border-radius: 8px;
        width: 100%;
    }
    h1, h2, h3 {
        color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

st.title("💼 Premium AI Resume Builder")
st.markdown("Fill in your details, and let AI write a full, ATS-optimized resume for you.")



st.header("📝 Step 1: Your Details")
name = st.text_input("Full Name")
role = st.text_input("Target Role (e.g., Data Scientist)")
email = st.text_input("Email / LinkedIn")

st.header("🎓 Step 2: Skills & Edu")
edu = st.text_input("Degree & University")
skills = st.text_area("Tech Stack (comma separated)")

st.header("⚙️ Step 3: Experience & Projects")
exp = st.text_area("Describe past internships or jobs (Keep it rough, AI will fix it!)", height=150)
projects = st.text_area("Describe your major projects", height=150)

st.markdown("---")
generate_btn = st.button("🚀 Generate Full Resume")

if generate_btn:
    if name and role and skills and projects:
        with st.spinner("Groq is formatting your full resume..."):
            st.header("📄 Generated Resume")
            # --- The Magic Prompt for a FULL Resume ---
            prompt = f"""
            You are an expert technical recruiter. Write a full, highly professional resume in Markdown format for {name}.
            Target Role: {role}
            Contact: {email}
            Education: {edu}
            Technical Skills: {skills}
            Experience: {exp}
            Projects: {projects}
            
            Instructions:
            1. Structure the resume with clear headers: Professional Summary, Skills, Work Experience, Projects, and Education.
            2. Rewrite the experience and projects into punchy, impactful bullet points starting with strong action verbs.
            3. Quantify achievements where possible.
            4. Ensure the formatting is clean Markdown. Do not include any conversational text before or after the resume.
            """
            
            try:
                response = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model="llama-3.1-8b-instant",
                )
                
                resume_text = response.choices[0].message.content
                
                # Display the beautiful markdown
                st.markdown(resume_text)
                
                # --- UI ENHANCEMENT 4: Download Button ---
                st.download_button(
                    label="⬇️ Download Resume (.txt)",
                    data=resume_text,
                    file_name=f"{name.replace(' ', '_')}_Resume.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"API Error: {e}")
    else:

        st.warning("👈 Please fill in all the details in the sidebar and left column first!")

