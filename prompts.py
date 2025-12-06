SYSTEM_PROMPT = """
You generate FINAL, HR-ready job application emails.

RULES:
1. Output ONLY the schema fields: subject_line, body, HR_email_address.
2. Email must be polished, concise, and immediately sendable.
3. Highlight EXPERIENCE first, then education (never reverse this order).
4. Select ONLY the most relevant experience based on the job description.
5. No placeholders, no invented facts, no questions.
6. Extract HR email if present; otherwise infer from domain.
7. Tone: professional, confident, impact-focused, short.
8. Result must read like a perfect real-world HR email.
"""

def build_user_prompt(job_description: str) -> str:
    return f"""
Generate a complete, HR-ready job application email.

------------------------------------------
APPLICANT DETAILS
------------------------------------------
Name: Apurba Manna  
Phone: 9083172958  
Email: 98apurbamanna@gmail.com  

Experience:
• Product Engineer – AI Certs (Sep 2025–Present)
  - Multi-agent automation (OpenAI Agents SDK)
  - Competitor monitoring automations (Apify)
  - LLM-based content research pipelines

• AI/ML Engineer – mTouch Labs (Jun 2025–Sep 2025)
  - ML-based voice ordering agent (Google STT, OpenAI LLMs, TTS, Twilio)
  - RAG document system (Unstructured + PostgreSQL)
  - LangGraph agents + MySQL automation

• AI/ML Intern – mTouch Labs (Mar 2025–Jun 2025)
  - Riva + Llama 3 real-time voice assistant
  - LangGraph ride-booking agent
  - Exotel telephony workflow automation

• AI Intern – AI Chef Master (Aug 2024–Nov 2024)
  - Food recommendation system
  - LlamaIndex/HF/Mistral chatbot
  - Streamlit UI for AI workflows

Projects:
• Stock Sentiment Analysis (IIT Roorkee, May–Jun 2024)
  - 80% accuracy sentiment model, LSTM RMSE 0.03

Education:
• M.Tech, Applied Mathematics & Scientific Computing, IIT Roorkee  
  - Completed: Jun 2025  
  - CGPA: 8.65

Skills:
Python, ML, NLP, RAG, LLMs, LangGraph, Data Pipelines,
Pandas, NumPy, Scikit-learn, MySQL, PostgreSQL

Achievements:
• GATE 2023 AIR 309  
• Winner – Express to Inspire, IIT Roorkee  

------------------------------------------
TASK
------------------------------------------
Return ONLY:
1. subject_line  
2. body (experience-first, precise, confident)  
3. HR_email_address  

INSTRUCTIONS:
• Start the email by emphasizing relevant experience.  
• Then add academics at the end.  
• Keep it short, HR-friendly, and tailored to the JD.  
• No placeholders. No extra commentary.  

------------------------------------------
JOB DESCRIPTION
------------------------------------------
{job_description}
------------------------------------------
"""
