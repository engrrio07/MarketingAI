import requests
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000/api"

def cleanup_user(email, password):
    # Login to get the token
    token = login(email, password)
    if token:
        # Delete all social media posts
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.delete(f"{BASE_URL}/social-media/posts", headers=headers)
        if response.status_code == 200:
            print("Deleted all social media posts")
        else:
            print(f"Failed to delete social media posts. Status code: {response.status_code}")
            print(f"Response content: {response.text}")

        # Delete the user
        response = requests.delete(f"{BASE_URL}/auth/users", headers=headers)
        if response.status_code == 200:
            print("Deleted user")
        else:
            print(f"Failed to delete user. Status code: {response.status_code}")
            print(f"Response content: {response.text}")
    else:
        print("Failed to login for cleanup (this is expected if the user doesn't exist)")

def register_user(email, password):
    response = requests.post(f"{BASE_URL}/auth/register", json={"email": email, "password": password})
    if response.status_code == 201:
        return True
    elif response.status_code == 400 and "Email already registered" in response.text:
        print("User already exists, proceeding with test")
        return True
    else:
        print(f"Registration failed. Status code: {response.status_code}")
        print(f"Response content: {response.text}")
        return False

def login(email, password):
    response = requests.post(f"{BASE_URL}/auth/token", data={"username": email, "password": password})
    if response.status_code == 200:
        return response.json()["access_token"]
    return None

def create_social_media_post(token, content, platform, scheduled_time):
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "content": content,
        "platform": platform,
        "scheduled_time": scheduled_time.isoformat()
    }
    response = requests.post(f"{BASE_URL}/social-media/posts", json=data, headers=headers)
    return response.json() if response.status_code == 200 else None

def get_social_media_posts(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/social-media/posts", headers=headers)
    return response.json() if response.status_code == 200 else None

# Test the social media posting feature
email = "test@example.com"
password = "testpassword"

# Cleanup before test
cleanup_user(email, password)

# Register a new user
if register_user(email, password):
    print("User registered successfully")

    # Login and get the access token
    token = login(email, password)
    if token:
        print("Logged in successfully")

        # Create a social media post
        content = "This is a test post for our MarketingAI application!"
        platform = "Twitter"
        scheduled_time = datetime.now(timezone.utc) + timedelta(hours=1)
        post = create_social_media_post(token, content, platform, scheduled_time)
        if post:
            print("Social media post created successfully")
            print(f"Post details: {post}")
        else:
            print("Failed to create social media post")

        # Get all social media posts for the user
        posts = get_social_media_posts(token)
        if posts:
            print("Retrieved social media posts:")
            for post in posts:
                print(f"- {post}")
        else:
            print("Failed to retrieve social media posts")
    else:
        print("Login failed")
else:
    print("User registration failed")

# Cleanup after test
cleanup_user(email, password)