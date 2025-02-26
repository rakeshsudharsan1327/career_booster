import google.generativeai as genai

# Configure Gemini API (Replace with your actual API key)
genai.configure(api_key="AIzaSyC4aQmveouqu9mQA9zKo9OKITycgiyvfMs")

def search_career_insights(job_title):
    """Fetch future job market insights using Gemini API."""
    try:
        prompt = (f"Provide a well-structured and concise analysis of the future job market trends, emerging skills, "
                  f"and industry outlook for the role: '{job_title}'. Format the response as bullet points for direct website display.")

        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)  # Indented correctly

        return response.text.strip()

    except Exception as e:
        return f"Error fetching job insights: {e}"
