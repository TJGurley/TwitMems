# Code by Tyler Gurley (tjg16)
# Florida State University Computer Science

import tweepy as tw
from guizero import App, Text, TextBox, PushButton, Window
import datetime

app = App(title="TwitMems", bg="#1dcaff")
text = Text(app, text="Enter Valid Handle")
textBox = TextBox(app, width=25)

def exitprogram():
    exit(1)


# Everything Kinda Happen in Here
def findTweets():
    user = textBox.value
    app.hide()

    # Loading Window Appears
    loadingWindow = Window(app, title="Loading Tweets", visible=True)
    loadingText = Text(loadingWindow, text="Loading Tweets... This may take up to 30 seconds")
    loadingWindow.update()

    # Checking to make sure everything is working on console
    print(user)
    myuser = api.get_user(screen_name=user)
    print(user, " has ", myuser.statuses_count, " total tweets")

    # Doing our first search so we can get our maxid to search from on the rest
    print("First Search...")
    for tweet in tw.Cursor(api.user_timeline, screen_name=user).items(200):
        tweets.append(tweet)

    for tweet in tweets:
        maxtweetid = tweet.id

    # Doing the rest of our searches resetting the maxid everytime.
    print("Rest of searches...")
    for x in range(0, 30):
        print(x, end=" ", flush=True)
        newtweets = tw.Cursor(api.user_timeline,
                              screen_name=user,
                              max_id=maxtweetid,
                              count=0).items(100)
        for tweet in newtweets:
            maxtweetid = tweet.id
            tweets.append(tweet)
    tracker = 0

    # Close our loading window
    loadingWindow.hide()

    tweetsWindow = Window(app, title="Tweets for @" + user)
    # Setting up our date stuff to print on window Format of datetime: YYYY-MM-DD
    createDate = str(myuser.created_at)
    createDate = createDate[:4]
    todayMonth = datetime.datetime.now()
    todayMonth = todayMonth.strftime("%B")
    todayDay = str(datetime.date.today())
    todayDay = todayDay[8:10]
    todayYear = str(datetime.date.today())
    todayYear = todayYear[0:4]

    text1 = Text(tweetsWindow, text="Tweet(s) from @" + user + " on " + todayMonth + " " + todayDay + " between " +
                                    createDate + "-" + todayYear)
    tweetsWindow.hide()

    myDate = str(datetime.date.today())
    newDate = myDate[4:]

    # Setting our text in our tweet window
    for tweet in tweets:
        if newDate in tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"):
            tracker = tracker + 1
            text = Text(tweetsWindow,
                        text="Tweet " + str(tracker) + ": \"" + tweet.text + "\"\n" + str(tweet.created_at) + "\n")
            # print("Tweet: ", tracker)
            # print("\"" + tweet.text + "\"")
            # print(tweet.created_at)
    # Display our tweets and program is concluded
    exitprogrambutton = PushButton(tweetsWindow, exitprogram, text="Exit")
    tweetsWindow.show()


enterUser = PushButton(app, findTweets, text="Enter")

print("logging in to api...")

# I did not put my personal keys for the WebAPI
consumer_key = 'Censored'
consumer_secret = 'Censored'
access_token = 'Censored'
access_token_secret = 'Censored'

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)

print("logged in to api")

tweets = []

app.display()
input("press something to end")
