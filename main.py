from scraper import get_reddit_comments, get_reddit_submissions
from persona_builder import generate_persona

def extract_username_from_url(url: str) -> str:
    """
    Extracts Reddit username from a valid profile URL.
    Example: https://www.reddit.com/user/kojied/ → kojied
    """
    if not url.startswith("https://www.reddit.com/user/"):
        raise ValueError("❌ Invalid Reddit profile URL format.")
    
    return url.rstrip("/").split("/")[-1]

def build_user_persona(url):
    try:
        username = extract_username_from_url(url)
        print(f"\n🔍 Fetching data for: {username}")

        comments = get_reddit_comments(username, required=5, limit=20)
        posts = get_reddit_submissions(username, required=5, limit=20)

        if not comments and not posts:
            print("❌ No usable data found. Skipping persona generation.")
            return

        data = {"comments": comments, "posts": posts}

        print("\n🧠 Generating persona...")
        persona = generate_persona(data)

        filename = f"{username}_persona.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(persona)

        print(f"\n✅ Persona saved to: {filename}")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"\n❌ Unexpected error occurred: {e}")

# 🔧 RUN STARTS HERE
if __name__ == "__main__":
    input_url = r"https://www.reddit.com/user/kojied/".strip()
    build_user_persona(input_url)
