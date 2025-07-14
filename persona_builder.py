import re
from collections import Counter

USE_OLLAMA = True  # 🔁 Set to False for dummy fallback

def build_prompt(data):
    prompt = "Based on the following Reddit user's posts and comments, generate a detailed user persona. The persona should include:\n\n"
    prompt += "- Likely age group\n- Interests\n- Writing style\n- Personality traits\n- Any noticeable beliefs or opinions\n"
    prompt += "- Favorite subreddits\n- Overall tone of communication\n\n"
    prompt += "Also cite which post or comment supports each trait in the persona.\n\n"

    prompt += "=== Reddit Comments ===\n"
    for i, comment in enumerate(data.get("comments", []), 1):
        prompt += f"[Comment {i}]: {comment['text']}\nURL: {comment['permalink']}\n\n"

    prompt += "=== Reddit Posts ===\n"
    for i, post in enumerate(data.get("posts", []), 1):
        prompt += f"[Post {i}]: {post['title']}\nBody: {post['body']}\nURL: {post['permalink']}\n\n"

    return prompt

def generate_dummy_persona(data: dict) -> str:
    comments = data.get("comments", [])
    posts = data.get("posts", [])

    if not comments and not posts:
        return "Not enough data to generate persona."

    comment_texts = [c["text"] for c in comments]
    post_texts = [p["body"] for p in posts if p["body"]]

    all_texts = comment_texts + post_texts
    all_text = " ".join(all_texts).lower()
    words = re.findall(r'\b[a-z]{4,}\b', all_text)
    stopwords = {"that", "this", "have", "with", "about", "which", "from", "what", "would", "there", "their"}
    filtered = [word for word in words if word not in stopwords]
    top_keywords = Counter(filtered).most_common(10)
    interests = ", ".join([word for word, _ in top_keywords[:5]]) or "technology, programming"

    persona = "🧠 User Persona Summary\n"
    persona += "-" * 30 + "\n"
    persona += "- Likely Age Group: 20s to 30s\n"
    persona += f"- Interests: {interests}\n"
    persona += "- Writing Style: Informal and concise\n"
    persona += "- Personality Traits: Curious, active, expressive\n"
    persona += "- Tone: Balanced, slightly enthusiastic\n"
    persona += "- Favorite Subreddits: Inferred from topics\n\n"

    persona += "📌 Supporting Evidence (Citations):\n"
    for i, comment in enumerate(comments[:2], 1):
        persona += f"- Comment {i}: \"{comment['text'][:60]}...\" — {comment['permalink']}\n"
    for i, post in enumerate(posts[:2], 1):
        persona += f"- Post {i}: \"{post['title']}\" — {post['permalink']}\n"

    return persona

def generate_persona(data: dict) -> str:
    if USE_OLLAMA:
        try:
            import ollama
            prompt = build_prompt(data)
            print("⚙️ Sending prompt to Ollama...")

            response = ollama.chat(
                model='llama3',
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
        except Exception as e:
            print(f"⚠️ Ollama failed: {e}")
            print("🔁 Falling back to dummy persona.")
            return generate_dummy_persona(data)
    else:
        return generate_dummy_persona(data)
