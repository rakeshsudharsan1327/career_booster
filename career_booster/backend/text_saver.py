import os

def save_resume_as_text(optimized_resume, filename="Optimized_Resume.txt"):
    save_dir = "./generated_resumes"  # Use a local directory for testing

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    text_path = os.path.join(save_dir, filename)

    try:
        # ✅ Ensure content is not empty
        if not optimized_resume.strip():
            optimized_resume = "Error: Resume content is empty."

        # ✅ Handle encoding issues
        optimized_resume = optimized_resume.encode('utf-8', 'replace').decode('utf-8')

        with open(text_path, "w", encoding="utf-8") as file:
            file.write(optimized_resume)

        print(f"Text file successfully saved at: {text_path}")
        return text_path
    except Exception as e:
        print(f"Error while saving text file: {e}")
        return None
