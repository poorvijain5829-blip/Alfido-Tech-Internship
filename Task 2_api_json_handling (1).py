"""
Task 2: API Integration & JSON Handling
------------------------------------------
Goal: Understand how to call a public REST API using the 'requests' library,
parse the JSON response, and save/read structured data locally.

We use two free, no-auth-required public APIs as examples:
  1. GitHub API  -> fetch public profile info for a GitHub user
  2. JSONPlaceholder -> fetch sample post data (fallback / extra demo)

Author: (your name)
"""

import requests
import json
import os

# ----------------------------------------------------------------------
# 1. SETUP
# ----------------------------------------------------------------------
OUTPUT_DIR = "api_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

GITHUB_USERNAME = "octocat"   # GitHub's official demo account, always available
GITHUB_API_URL = f"https://api.github.com/users/{GITHUB_USERNAME}"
POSTS_API_URL = "https://jsonplaceholder.typicode.com/posts"


# ----------------------------------------------------------------------
# 2. FETCH DATA FROM A REST API
# ----------------------------------------------------------------------
def fetch_json(url, params=None):
    """
    Send a GET request to the given URL and return the parsed JSON.
    Handles network errors, bad status codes, and invalid JSON gracefully.
    """
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()   # raises HTTPError for 4xx/5xx responses
        return response.json()        # parses JSON text into a Python dict/list
    except requests.exceptions.Timeout:
        print(f"Error: request to {url} timed out.")
    except requests.exceptions.ConnectionError:
        print(f"Error: could not connect to {url}. Check your internet connection.")
    except requests.exceptions.HTTPError as e:
        print(f"Error: HTTP error occurred - {e}")
    except json.JSONDecodeError:
        print(f"Error: response from {url} was not valid JSON.")
    except requests.exceptions.RequestException as e:
        print(f"Error: an unexpected request error occurred - {e}")
    return None   # return None so the caller can check and handle failure


# ----------------------------------------------------------------------
# 3. SAVE JSON DATA TO A LOCAL FILE
# ----------------------------------------------------------------------
def save_json(data, filepath):
    """Save a Python object as a nicely formatted JSON file."""
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)   # indent=4 makes it human-readable
        print(f"Saved JSON data to '{filepath}'")
    except IOError as e:
        print(f"Error saving JSON file: {e}")


# ----------------------------------------------------------------------
# 4. READ JSON DATA FROM A LOCAL FILE
# ----------------------------------------------------------------------
def load_json(filepath):
    """Read and return JSON data from a local file."""
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: '{filepath}' not found.")
    except json.JSONDecodeError:
        print(f"Error: '{filepath}' contains invalid JSON.")
    return None


# ----------------------------------------------------------------------
# 5. MAIN DEMO
# ----------------------------------------------------------------------
if __name__ == "__main__":

    # ---- Demo 1: GitHub user profile ----
    print(f"Fetching GitHub profile for '{GITHUB_USERNAME}'...")
    user_data = fetch_json(GITHUB_API_URL)

    if user_data:
        # Extract a few useful fields from the JSON response
        summary = {
            "username": user_data.get("login"),
            "name": user_data.get("name"),
            "public_repos": user_data.get("public_repos"),
            "followers": user_data.get("followers"),
            "profile_url": user_data.get("html_url"),
        }
        print("\n--- GitHub Profile Summary ---")
        for key, value in summary.items():
            print(f"{key}: {value}")

        # Save the extracted summary (not the full raw response) to disk
        github_filepath = os.path.join(OUTPUT_DIR, "github_user.json")
        save_json(summary, github_filepath)

        # Read it back to prove the round-trip works
        loaded = load_json(github_filepath)
        print("\n--- Re-loaded from local JSON file ---")
        print(loaded)
    else:
        print("Could not fetch GitHub data.")

    # ---- Demo 2: Fetch a list of posts, filter, and save ----
    print(f"\nFetching sample posts from JSONPlaceholder...")
    posts = fetch_json(POSTS_API_URL)

    if posts:
        # JSON arrays map naturally to Python lists of dicts.
        # Here we filter to keep only the first 5 posts as a smaller sample.
        sample_posts = posts[:5]
        posts_filepath = os.path.join(OUTPUT_DIR, "sample_posts.json")
        save_json(sample_posts, posts_filepath)

        print(f"\n--- First {len(sample_posts)} Posts (title only) ---")
        for post in sample_posts:
            print(f"#{post['id']}: {post['title']}")
    else:
        print("Could not fetch posts data.")

    print("\nAPI integration & JSON handling demo completed.")
