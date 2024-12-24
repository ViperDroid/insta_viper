# Import instaloader package
import instaloader
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Creating an Instaloader() object
ig = instaloader.Instaloader()

# Banner
print(Fore.YELLOW + """
     ██╗   ██╗██╗██████╗ ███████╗███████╗██████╗ 
     ██║   ██║██║██╔══██╗██╔════╝██╔════╝██╔══██╗
     ██║   ██║██║██████╔╝█████╗  █████╗  ██████╔╝
     ██║   ██║██║██╔═══╝ ██╔══╝  ██╔══╝  ██╔══██╗
     ╚██████╔╝██║██║     ███████╗███████╗██║  ██║
      ╚═════╝ ╚═╝╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝
    Powered by Viper Droid
""")

# Taking the session ID as input from the user
session_cookie = input(Fore.GREEN + "Enter your session ID: ")

# Set the session cookie in Instaloader
ig.context._session.cookies.set("sessionid", session_cookie)

# Taking the Instagram username as input from the user
usrname = input(Fore.GREEN + "Enter username: ")

try:
    # Fetching the details of the provided username using Instaloader object
    profile = instaloader.Profile.from_username(ig.context, usrname)

    # Printing the fetched profile details with colors
    print(Fore.CYAN + "\nProfile Details for: " + Fore.MAGENTA + profile.username)
    print(Fore.YELLOW + "-----------------------------")
    print(Fore.GREEN + f"Full Name: {profile.full_name}")
    print(Fore.GREEN + f"Number of Posts: {profile.mediacount}")
    print(Fore.GREEN + f"Followers: {profile.followers}")
    print(Fore.GREEN + f"Following: {profile.followees}")
    print(Fore.GREEN + f"Bio: {profile.biography}")
    print(Fore.GREEN + f"Profile Picture URL: {profile.profile_pic_url}")
    print(Fore.GREEN + f"Is Private: {profile.is_private}")
    print(Fore.GREEN + f"Is Verified: {profile.is_verified}")
    print(Fore.GREEN + f"External URL: {profile.external_url}")
    print(Fore.GREEN + f"Is Business Account: {profile.is_business_account}")

    # Displaying business category if it's a business account
    if profile.is_business_account:
        print(Fore.GREEN + f"Business Category: {profile.business_category}")

    # Profile engagement statistics: Average likes/comments per post
    total_likes = 0
    total_comments = 0
    total_posts = 0

    for post in profile.get_posts():
        total_likes += post.likes
        total_comments += post.comments
        total_posts += 1

    if total_posts > 0:
        avg_likes = total_likes / total_posts
        avg_comments = total_comments / total_posts
        print(Fore.GREEN + f"Average Likes per Post: {avg_likes:.2f}")
        print(Fore.GREEN + f"Average Comments per Post: {avg_comments:.2f}")

    # Engagement Rate calculation
    if profile.followers > 0:
        engagement_rate = (total_likes + total_comments) / profile.followers
        print(Fore.GREEN + f"Engagement Rate: {engagement_rate * 100:.2f}%")

    # List of followers (first 5)
    print(Fore.YELLOW + "\nFollowers (first 5):")
    for idx, follower in enumerate(profile.get_followers()):
        if idx >= 5:
            break
        print(Fore.CYAN + f"- {follower.username}")

    # List of followees (first 5)
    print(Fore.YELLOW + "\nFollowing (first 5):")
    for idx, followee in enumerate(profile.get_followees()):
        if idx >= 5:
            break
        print(Fore.CYAN + f"- {followee.username}")

    # Displaying recent posts with engagement info, hashtags, and locations
    print(Fore.YELLOW + "\nRecent Posts:")
    top_liked_posts = []
    top_commented_posts = []
    for post in profile.get_posts():
        print(Fore.CYAN + f"Post URL: https://www.instagram.com/p/{post.shortcode}/")
        print(Fore.GREEN + f"Post Caption: {post.caption}")
        print(Fore.GREEN + f"Post Date: {post.date_utc}")
        print(Fore.GREEN + f"Likes: {post.likes} | Comments: {post.comments}")

        # Media Type (Image, Video, Carousel)
        if post.is_video:
            print(Fore.GREEN + "Post Media Type: Video")
        elif post.mediacount > 1:
            print(Fore.GREEN + "Post Media Type: Carousel (Multiple Images/Videos)")
        else:
            print(Fore.GREEN + "Post Media Type: Image")

        # Extract hashtags from the caption
        hashtags = [tag for tag in post.caption.split() if tag.startswith('#')]
        if hashtags:
            print(Fore.GREEN + f"Hashtags: {', '.join(hashtags)}")

        # Location of the post, if tagged
        if post.location:
            print(Fore.GREEN + f"Post Location: {post.location.name}")
        else:
            print(Fore.GREEN + "Post Location: Not tagged")

        # Post dimensions (for images/videos)
        print(Fore.GREEN + f"Post Dimensions: {post.width}x{post.height} pixels")

        # Post Media URL (Image/Video URL)
        print(Fore.GREEN + f"Post Media URL: {post.url}")

        # Add to top liked/commented lists
        top_liked_posts.append((post.likes, post))
        top_commented_posts.append((post.comments, post))

        # Print mentions in comments if any
        print(Fore.GREEN + "Mentions in Comments:")
        for comment in post.get_comments():
            if comment.owner.username != profile.username:
                print(Fore.CYAN + f"  - {comment.owner.username}: {comment.text}")
        
        print(Fore.YELLOW + "-" * 50)

    # Sort top posts by likes and comments
    top_liked_posts.sort(reverse=True, key=lambda x: x[0])
    top_commented_posts.sort(reverse=True, key=lambda x: x[0])

    # Display top 3 liked posts
    print(Fore.YELLOW + "\nTop 3 Most Liked Posts:")
    for idx, (_, post) in enumerate(top_liked_posts[:3]):
        print(Fore.GREEN + f"{idx + 1}. URL: {post.url} | Likes: {post.likes}")

    # Display top 3 commented posts
    print(Fore.YELLOW + "\nTop 3 Most Commented Posts:")
    for idx, (_, post) in enumerate(top_commented_posts[:3]):
        print(Fore.GREEN + f"{idx + 1}. URL: {post.url} | Comments: {post.comments}")

    # Calculate the total likes and comments across all posts
    print(Fore.YELLOW + f"\nTotal Likes Across All Posts: {total_likes}")
    print(Fore.YELLOW + f"Total Comments Across All Posts: {total_comments}")

    # Downloading the profile picture of that account
    ig.download_profile(usrname, profile_pic_only=True)

except instaloader.exceptions.ProfileNotExistsException:
    print(Fore.RED + "The profile does not exist.")
except instaloader.exceptions.InstaloaderException as e:
    print(Fore.RED + f"An error occurred: {e}")
