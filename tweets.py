import json
import subprocess
import datetime


# Execute the Twitter search command and save the results to a file.
def search_tweets(query, max_results=None, since=None, until=None):
    
    cmd = "snscrape --jsonl "
    if max_results:
        cmd += f"--max-results {max_results} "
    if since:
        cmd += f"--since {since} "
    if until:
        cmd += f"--until {until} "
    cmd += f"twitter-search '{query}' > tweets.json"

    subprocess.run(cmd, shell=True)

# Read the input JSON file
with open('input.json', 'r') as f:
    input_data = json.load(f)

# Extract the user, hashtag, and general search query from input data
user = input_data.get('user')
hashtag = input_data.get('hashtag')
query = input_data.get('query')

# Limit the number of tweets to 10 by default
max_results = input_data.get('max_results', 10)

# Execute the Twitter search command for user or hashtag
if user:
    search_tweets(f"from:{user}", max_results=max_results)
elif hashtag:
    search_tweets(f"#{hashtag}", max_results=max_results)

# Execute the Twitter search command for general query
if query:
    since = input_data.get('since')
    until = input_data.get('until')
    search_tweets(query, max_results=max_results, since=since, until=until)

# Extract the raw text from the tweets and write to a file
with open('tweets.json', 'r') as f:
    tweets = [json.loads(line) for line in f]

text = '\n\n'.join([tweet['content'].strip() for tweet in tweets])

with open('text.txt', 'w') as f:
    f.write(text)
