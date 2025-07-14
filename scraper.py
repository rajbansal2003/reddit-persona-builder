import requests

def get_reddit_comments(username, required=5, limit=20):
    url = f"https://www.reddit.com/user/{username}/comments/.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # throws error for 4xx/5xx

        data = response.json()
        comments = []

        for item in data["data"]["children"]:
            body = item["data"].get("body", "")
            if body.lower() not in ["[deleted]", "[removed]"]:
                comments.append({
                    "text": body,
                    "permalink": "https://www.reddit.com" + item["data"].get("permalink", "")
                })
            if len(comments) == required:
                break

        return comments

    except Exception as e:
        print(f"Error fetching comments: {e}")
        return []


def get_reddit_submissions(username, required=5, limit=20):
    url = f"https://www.reddit.com/user/{username}/submitted/.json?limit={limit}"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        data = response.json()
        posts = []

        for item in data["data"]["children"]:
            post_data = item["data"]

            title = post_data.get("title", "").strip()
            selftext = post_data.get("selftext", "").strip()
            permalink = "https://www.reddit.com" + post_data.get("permalink", "")

            # 🔴 Skip if body is removed/deleted/empty
            if selftext.lower() in ["[deleted]", "[removed]", ""]:
                continue

            posts.append({
                "title": title,
                "body": selftext,
                "permalink": permalink
            })

            # ✅ Stop only if required reached
            if len(posts) == required:
                break

        # ✅ Even if < required, return what we got
        return posts

    except Exception as e:
        print(f"Error fetching posts: {e}")
        return []
