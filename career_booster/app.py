import streamlit as st
from backend.resume_processing import extract_text_from_pdf, extract_keywords
from backend.job_matching import match_resume_with_job
from backend.course_recommendation import get_free_courses_youtube, get_free_datasets_kaggle
from backend.web_scraping import scrape_linkedin_jobs
from backend.roadmap_generator import generate_learning_roadmap
from backend.resume_scoring import calculate_resume_score, generate_feedback
from backend.resume_restructuring import restructure_resume_with_gemini
from backend.tavily_search import search_career_insights
from backend.text_saver import save_resume_as_text  # Updated to save as text file
from utils.text_processing import clean_text
import sys
import os
import tensorflow as tf

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.ERROR)
sys.path.append(os.path.abspath("S:/career_booster"))

st.set_page_config(page_title="Career Booster", layout="wide")

st.title("🚀 Career Booster App")

# Sidebar Inputs
st.sidebar.header("📂 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload your resume (PDF)", type=["pdf"])
job_title = st.sidebar.text_input("Enter Job Title")
job_description = st.sidebar.text_area("Paste Job Description (Leave blank for auto-fetch)")
prep_time_weeks = st.sidebar.number_input("Preparation Time (Weeks)", min_value=1, max_value=52, value=4)

if uploaded_file and job_title:
    with st.spinner("Processing Resume..."):
        resume_text = extract_text_from_pdf(uploaded_file)
        resume_keywords = extract_keywords(resume_text)
        current_skills = resume_keywords  # Assign resume keywords as current skills

    if not job_description:
        with st.spinner("Fetching job descriptions from LinkedIn..."):
            job_descriptions = scrape_linkedin_jobs(job_title)
            job_description = " ".join(job_descriptions[:3]) if job_descriptions else ""

    with st.spinner("Matching Resume with Job Description..."):
        missing_skills = match_resume_with_job(resume_keywords, job_description)
        missing_skills = [] if isinstance(missing_skills, float) else missing_skills

    with st.spinner("Calculating Resume Score..."):
        resume_score = calculate_resume_score(resume_text, job_description)
        feedback = generate_feedback(resume_text, job_description)

    st.subheader("📊 Resume Score & Feedback")
    st.write(f"**Score:** {resume_score}%")
    st.write(f"**Feedback:** {feedback}")

    if st.button("Optimize Resume"):
        with st.spinner("Optimizing Resume with Gemini..."):
            optimized_resume = restructure_resume_with_gemini(resume_text, job_description)

        text_path = save_resume_as_text(optimized_resume)  # Save as text file

        st.subheader("📝 Optimized Resume")
        st.text_area("Updated Resume", optimized_resume, height=300)

        with open(text_path, "r", encoding="utf-8") as file:
            text_content = file.read()

        # ✅ Download as .txt file
        st.download_button("📥 Download Optimized Resume (TXT)", text_content, file_name="Optimized_Resume.txt", mime="text/plain")

    st.subheader("🌐 Career Insights (Powered by Gemini)")
    with st.spinner("Fetching career insights..."):
        career_insights = search_career_insights(job_title)
    st.write(career_insights if career_insights else "No insights found.")

    st.subheader("🔍 Missing Skills")
    if missing_skills:
        st.write("These skills are missing from your resume:")
        st.write(", ".join(missing_skills))
    else:
        st.success("✅ Your resume matches the job description well!")

    youtube_links, kaggle_links, udemy_links = [], [], []
    with st.spinner("Fetching free courses..."):
        for skill in missing_skills:
            try:
                youtube_courses = get_free_courses_youtube(skill)
                kaggle_datasets = get_free_datasets_kaggle(skill)
        

                youtube_links.extend([url for _, url in youtube_courses])
                kaggle_links.extend([url for _, url in kaggle_datasets])
                
            except Exception as e:
                st.error(f"Error fetching courses for {skill}: {str(e)}")

    st.subheader("📚 Recommended Free Courses")
    st.markdown("### 🎥 YouTube Courses")
    if youtube_links:
        for link in youtube_links:
            st.markdown(f"- [{link}]({link})")
    else:
        st.warning("⚠️ No YouTube courses found.")

    st.markdown("### 📊 Kaggle Datasets")
    if kaggle_links:
        for link in kaggle_links:
            st.markdown(f"- [{link}]({link})")
    else:
        st.warning("⚠️ No Kaggle datasets found.")

    

    with st.spinner("Generating Roadmap..."):
        roadmap = generate_learning_roadmap(job_title, current_skills, youtube_links + kaggle_links + udemy_links, prep_time_weeks)

    st.subheader("🗺️ Learning Roadmap")
    if roadmap:
        st.text_area("Generated Learning Roadmap", roadmap, height=300)
    else:
        st.warning("⚠️ No roadmap generated. Ensure you have missing skills and course recommendations.")

else:
    st.info("📢 Upload a resume and enter a job title to get started!")
