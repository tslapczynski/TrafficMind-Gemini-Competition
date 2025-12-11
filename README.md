# 🚗 TrafficMind - AI Dashcam Auditor

TrafficMind is an automated fleet safety tool powered by **Gemini 2.5 Flash / Gemini 3**.
Built for the **Gemini API Developer Competition**.

## 🎥 Demo
https://www.youtube.com/watch?v=ZQMLJJEumPg

## 💡 How it works
1. User uploads a dashcam video.
2. The app sends the footage to **Gemini 1.5/2.5 Pro** using the Multimodal API.
3. The model analyzes the video for traffic violations, aggressive driving, and accidents.
4. A structured Markdown report is generated instantly.

## 🛠️ Tech Stack
- **AI Model:** Gemini 2.5 Flash / Gemini 3 Preview
- **Frontend:** Streamlit
- **Language:** Python
- **Tools:** Cursor (Vibe Coding)

## 🚀 How to run
1. Clone the repo.
2. Install dependencies: `pip install -r requirements.txt`
3. Add your API key to `.env`.
4. Run: `streamlit run app.py`
