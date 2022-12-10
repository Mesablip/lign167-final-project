from pytwitter import StreamApi, Api
import twitter_credentials
import re
import model

api = Api(
    consumer_key=twitter_credentials.CONSUMER_KEY,
    consumer_secret=twitter_credentials.CONSUMER_SECRET,
    access_token=twitter_credentials.ACCESS_TOKEN,
    access_secret=twitter_credentials.ACCESS_TOKEN_SECRET,
)

def check_single_mention(tweet_text):
    if len(re.findall("@[a-zA-Z0-9_]{0,15}", tweet_text)) == 2:
        return True
    return False

class MyStream(StreamApi):
    def on_tweet(self, tweet):
        text_reply = tweet.text
        if check_single_mention(text_reply):
            parent_tweet = api.get_tweet(tweet.conversation_id)
            output, score = model.clickbait_checker(parent_tweet.data.text)
            if output == 1:
                api.create_tweet(text="This title seems to be clickbait (" + str(round(score * 100, 2)) + "%)", reply_in_reply_to_tweet_id=tweet.id, reply_exclude_reply_user_ids=[])
            else:
                api.create_tweet(text="This title seems to not be clickbait (" + str(round(score * 100, 2)) + "%)", reply_in_reply_to_tweet_id=tweet.id, reply_exclude_reply_user_ids=[])



stream = MyStream(bearer_token=twitter_credentials.BEARER_TOKEN)

rules = {"add": [{"value": "track:Clickbait_Check", "tag": "track the mentions"}]}

stream.manage_rules(rules=rules, dry_run=True)

stream.search_stream(tweet_fields="conversation_id")