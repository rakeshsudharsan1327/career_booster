from googleapiclient.discovery import build
import kaggle
from config.api_keys import YOUTUBE_API_KEY
# ---- API KEYS (FILL THESE) ----
#YOUTUBE_API_KEY = "AIzaSyDu1Uo31VV8LaixtQF6O_EDLVMfXxi-H90"
#YOUTUBE_API_KEY = "ytapi"
kaggle.api.authenticate()

def get_free_courses_youtube(keyword):
    """
    Fetch free courses from YouTube based on a keyword.
    :param keyword: Search keyword
    :return: List of (title, video link) tuples
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    request = youtube.search().list(
        part="snippet", q=f"{keyword} free course", maxResults=1, type="video"
    )
    response = request.execute()
    return [(item["snippet"]["title"], f"https://www.youtube.com/watch?v={item['id']['videoId']}") for item in response["items"]]

from kaggle.api.kaggle_api_extended import KaggleApi

def get_free_datasets_kaggle(skill):
    api = KaggleApi()
    api.authenticate()
    
    datasets = api.dataset_list(search=skill)  # ✅ Remove 'page_size'
    
    course_links = []
    for dataset in datasets[:2]:  # ✅ Manually limit to 5 results
        course_links.append((dataset.ref, f"https://www.kaggle.com/{dataset.ref}"))
    
    return course_links


if __name__ == "_main_":
    # Example usage
    skill = "machine learning"
    print("YouTube Courses:", get_free_courses_youtube(skill))
    print("Kaggle Datasets:", get_free_datasets_kaggle(skill))