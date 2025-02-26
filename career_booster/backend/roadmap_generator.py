import datetime
import google.generativeai as genai


def generate_learning_roadmap(job_title, current_skills, recommended_links, prep_time_weeks):
    """
    Uses Gemini API to generate a structured, timeline-based learning roadmap.
    """
    genai.configure(api_key="AIzaSyC4aQmveouqu9mQA9zKo9OKITycgiyvfMs")

    start_date = datetime.date.today()
    prompt = f"""
    You are an AI career coach. Generate a structured learning roadmap to help someone become a {job_title}.
    
    Current Skills: {', '.join(current_skills)}
    Recommended Learning Resources: {', '.join(recommended_links)}
    Preparation Time: {prep_time_weeks} weeks
    
    The roadmap should follow a timeline-based approach with weekly milestones, clearly defining:
    - Start date for each week
    - Key topics to focus on
    - Learning steps
    - Practical hands-on project
    - Best free resources available
    
    {job_title} Learning Roadmap ({prep_time_weeks}-Week Timeline)
    
    Current Skill Assessment:
    - Summarize the user's existing skills and their relevance to the job role.
    
    Overall Approach:
    - Outline the learning strategy and key focus areas.
    
    Week-by-Week Plan:
    """

    for week in range(1, prep_time_weeks + 1):
        week_start = start_date + datetime.timedelta(weeks=week - 1)
        prompt += f"""
        
        📅 Week {week} ({week_start.strftime('%B %d, %Y')} - { (week_start + datetime.timedelta(days=6)).strftime('%B %d, %Y') })
        
        **Key Focus Areas:**
        - Topic 1
        - Topic 2
        - Topic 3
        
        **Learning Steps:**
        1. Step 1
        2. Step 2
        3. Step 3
        
        **Project Idea:**
        - Suggested hands-on project to apply learning.
        
        **Best Free Resources:**
        - [Resource 1](URL)
        - [Resource 2](URL)
        - [Resource 3](URL)
        
        """
    
    prompt += "Ensure the roadmap is structured for readability, using headings, bullet points, and a timeline format."
    
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(prompt)
    
    return response.text


if __name__ == "__main__":
    # Example usage
    job_title = "Marketing Manager"
    current_skills = ["Python", "Excel", "Data Analysis"]
    recommended_links = [
        "https://www.hubspot.com/academy",
        "https://analytics.google.com/analytics/academy/",
        "https://www.coursera.org/specializations/digital-marketing"
    ]
    prep_time_weeks = 4

    roadmap = generate_learning_roadmap(job_title, current_skills, recommended_links, prep_time_weeks)
    print("Learning Roadmap:\n", roadmap)
