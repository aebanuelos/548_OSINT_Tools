import tweepy as tweepy  # pip install tweepy
import os
import pandas as pd
from tabulate import tabulate
from tweepy import OAuthHandler

########################################################################################################################
# Verification Keys

# API keys that match to the settings of your twitter dev account
api_key = "***"
api_secrets = "***"
bearer_token = "***"
access_token = "***"
access_secret = "***"

client_id = "***"
client_secret = "***"

# goated Client documentation: https://docs.tweepy.org/en/stable/client.html#

Client = tweepy.Client(bearer_token=bearer_token, consumer_key=api_key, consumer_secret=api_secrets,
                       access_token=access_token, access_token_secret=access_secret, return_type=dict)
answer = Client.get_home_timeline()


# To make a tweet occur
# Client.create_tweet(text="Hey guys first try!")


def get_users_tweets(inputUsername):
    try:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        newFileName = f"{inputUsername}_Twitter_Connections.txt"
        filepath = os.path.join(desktop, newFileName)
        if not os.path.exists(desktop):
            os.makedirs(desktop)
        f = open(filepath, "a")
        # username_input = input("Enter Username for User's Timeline: ")
        users_id = Client.get_user(username=inputUsername)
        users_tweets = Client.get_users_tweets(id=users_id['data']['id'])
        recent_mentions = set()
        num_of_mentions = len(users_tweets['data'])
        for x in range(num_of_mentions):
            if "@" in users_tweets['data'][x]['text']:
                username_only = extract_string(users_tweets['data'][x]['text'])
                # recent_mentions[f'{x}_mention'] = username_only
                recent_mentions.add(username_only)
            else:
                continue
        updated_mentions = {s for s in recent_mentions if s}  # catches error of grabbing NULL user

        final_mentions = {}
        user_accounts = []
        link_to_accounts = []

        for accounts in updated_mentions:
            user_accounts.append(accounts)
            link_to_accounts.append(f"https://twitter.com/{accounts}")
        final_mentions["Username"] = user_accounts
        final_mentions["Links"] = link_to_accounts
        print(final_mentions)

        # appending accounts to text file on desktop
        i = 1
        for users in final_mentions['Username']:
            f.write(
                f"{i}: Username: {users} & Link: {final_mentions['Links'][final_mentions['Username'].index(users)]}\n")
            i += 1
        f.close()

        return (final_mentions)

    except Exception as e:
        print(
            f'\nPlease ensure the account exists, it is spelled right, and it has public settings.\nYou entered: "{inputUsername}"\nError: {e}')


''' 
Model for how pyqt5 interprets table data
data = {'col1':['1','2','3','4'],
        'col2':['1','2','1','3'],
        'col3':['1','1','2','1']}
'''


def extract_string(string):
    sub1 = "@"
    sub2 = " "
    idx1 = string.index(sub1)
    idx2 = string.index(sub2)
    res = ''
    # getting elements in between
    for idx in range(idx1 + len(sub1), idx2):
        res = res + string[idx]
    return (res)

# df = pd.DataFrame.from_dict(users_tweets)
# print(tabulate(df, headers='keys', tablefmt='psql'))
