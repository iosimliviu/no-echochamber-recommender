from flask import Flask
from processData import subreddit_recommender

app = Flask(__name__)


@app.route('/recommendations/<subreddit>')
def recomandSubreddit(subreddit):
    val = subreddit_recommender(subreddit)
    response = Flask.response_class(val.to_json())
    response.headers["Content-Type"] = "application/json"
    return response


if __name__ == '__main__':
    app.run()
