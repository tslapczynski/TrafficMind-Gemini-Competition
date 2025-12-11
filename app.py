import streamlit as st
import google.generativeai as genai
import os
import time
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(
    page_title="TrafficMind - AI Fleet Auditor",
    page_icon="🚗",
    layout="wide"
)

# 2. Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error("❌ API Key missing! Please check your .env file.")
    st.stop()

genai.configure(api_key=api_key)

# 3. User Interface
st.title("🚗 TrafficMind: AI Fleet Auditor")
st.markdown("""
**Automate your fleet safety analysis.** 
This tool uses **Gemini 1.5 Flash/Pro** to audit dashcam footage, identifying traffic violations, aggressive driving, and near-misses in seconds.
""")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("1. Upload Footage")
    uploaded_file = st.file_uploader("Upload dashcam video (mp4, mov, avi)", type=['mp4', 'mov', 'avi'])

    if uploaded_file is not None:
        st.video(uploaded_file)
        
        # Primary Action Button
        analyze_btn = st.button("🚀 Start AI Analysis", type="primary")

# Analysis Logic
if uploaded_file is not None and analyze_btn:
    with col2:
        st.subheader("2. AI Audit Report")
        status_box = st.empty()
        
        try:
            # A. Save temp file
            status_box.info("💾 Caching video locally...")
            temp_filename = "temp_video.mp4"
            with open(temp_filename, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # B. Upload to Google
            status_box.info("☁️ Uploading to Gemini API...")
            video_file = genai.upload_file(path=temp_filename)
            
            # C. Processing Loop (Critical)
            while video_file.state.name == "PROCESSING":
                status_box.warning("⏳ Neural network is processing the video frames... (Please wait)")
                time.sleep(3)
                video_file = genai.get_file(video_file.name)
            
            if video_file.state.name == "FAILED":
                raise ValueError("Video processing failed on Google servers.")

            # D. Analysis Prompt (English)
            status_box.info("🧠 Analyzing traffic patterns and violations...")
            
            model = genai.GenerativeModel(model_name="gemini-2.5-flash")
            
            # PROMPT IN ENGLISH FOR GLOBAL AUDIENCE
            prompt = """
            You are an expert AI Traffic Safety Auditor and Insurance Claim Adjuster.
            Analyze this dashcam footage second by second.
            
            Your goal is to generate a safety audit report. Identify EVERY traffic violation, road hazard, or aggressive driving behavior.
            
            Output Format (Markdown):
            
            ## 📋 Incident Log
            Create a structured list for each event found:
            
            ### ⏱️ [MM:SS] - [Short Event Name]
            * **Description:** What happened? Who was at fault?
            * **Severity:** 🟢 Low / 🟡 Medium / 🔴 High / 💀 Critical
            * **Regulation:** Cite general traffic rules violated (e.g., "Failure to yield", "Red light").
            
            ## 🏁 Summary
            * **Driver Safety Score:** [1-10] (10 is perfect)
            * **Final Verdict:** One sentence summary of the driver's behavior.
            """
            
            response = model.generate_content([video_file, prompt])
            
            # E. Display Result
            status_box.success("✅ Audit Complete!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
        finally:
            if os.path.exists("temp_video.mp4"):
                os.remove("temp_video.mp4")