import praw
import pandas as pd
from datetime import datetime
import time

# Reddit API credentials (replace with your own)
reddit = praw.Reddit(
    client_id="your_client_id", # replace with your client ID
    client_secret="your_client_secret", # replace with your client secret
    user_agent="python:CryptoScraper:v1.0 (by /u/IllSoup9651)"
)

# Define the subreddit and time range
subreddit = reddit.subreddit('CryptoCurrency')
start_date = int(datetime(2023, 6, 1).timestamp())  # Example: June 1, 2023
end_date = int(datetime(2023, 6, 30).timestamp())   # Example: June 30, 2023

# Storage for posts and comments
posts_data = []
comments_data = []

print("Starting scrape of r/CryptoCurrency...")
print(f"Time range: {datetime.fromtimestamp(start_date)} to {datetime.fromtimestamp(end_date)}")

# Initial settings
batch_size = 1000  # Max posts per API call
last_timestamp = end_date  # Start at the end of your range
total_posts = 0

while True:
    print(f"\nScraping batch starting before {datetime.fromtimestamp(last_timestamp)}...")
    post_count = 0
    batch_posts = []
    
    # Fetch the next batch of posts
    for submission in subreddit.new(limit=batch_size, params={'before': f't3_{submission.id}' if post_count > 0 else None}):
        current_time = submission.created_utc
        if current_time > end_date:  # Skip posts after your range
            continue
        if current_time < start_date:  # Stop if we’ve gone past the start
            break
        
        post_count += 1
        total_posts += 1
        batch_posts.append(submission)
        print(f"Processing post #{total_posts}: '{submission.title}' (ID: {submission.id}, Time: {datetime.fromtimestamp(current_time)})")
        
        # Store post data
        posts_data.append({
            'post_id': submission.id,
            'title': submission.title,
            'text': submission.selftext,
            'created_utc': datetime.fromtimestamp(current_time),
            'score': submission.score,
            'num_comments': submission.num_comments,
            'url': submission.url
        })
        
        # Fetch all comments
        try:
            submission.comments.replace_more(limit=None)
            comment_count = 0
            for comment in submission.comments.list():
                comment_count += 1
                comments_data.append({
                    'post_id': submission.id,
                    'comment_id': comment.id,
                    'body': comment.body,
                    'created_utc': datetime.fromtimestamp(comment.created_utc),
                    'score': comment.score,
                    'parent_id': comment.parent_id
                })
            print(f"  -> Fetched {comment_count} comments for post {submission.id}")
        except Exception as e:
            print(f"  -> Error fetching comments for post {submission.id}: {e}")
        
        time.sleep(1)  # Respect rate limits
    
    # Update the last timestamp for the next batch
    if not batch_posts or batch_posts[-1].created_utc < start_date:
        print(f"\nReached {datetime.fromtimestamp(start_date)} or no more posts. Stopping.")
        break
    
    last_timestamp = batch_posts[-1].created_utc
    print(f"Batch complete: Processed {post_count} posts. Next batch starts before {datetime.fromtimestamp(last_timestamp)}")
    
    # Save intermediate results (optional, to avoid losing data if interrupted)
    posts_df = pd.DataFrame(posts_data)
    comments_df = pd.DataFrame(comments_data)
    posts_df.to_csv('crypto_posts_temp.csv', index=False)
    comments_df.to_csv('crypto_comments_temp.csv', index=False)
    print("Saved temporary files: 'crypto_posts_temp.csv' and 'crypto_comments_temp.csv'")

# Final save
posts_df = pd.DataFrame(posts_data)
comments_df = pd.DataFrame(comments_data)
posts_df.to_csv('crypto_posts.csv', index=False)
comments_df.to_csv('crypto_comments.csv', index=False)

# Summary
print("\nScraping complete!")
print(f"Total posts collected: {len(posts_df)}")
print(f"Total comments collected: {len(comments_df)}")
print(f"Final files saved: 'crypto_posts.csv' and 'crypto_comments.csv'")