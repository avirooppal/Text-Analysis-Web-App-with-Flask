from flask import Flask, render_template, request
from textblob import TextBlob
from summarizer import Summarizer
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import base64
from io import BytesIO

app = Flask(__name__)

def analyze_sentiment(text):
    analysis = TextBlob(text)
    sentiment_score = analysis.sentiment.polarity

    # Map sentiment score to emojis
    if sentiment_score > 0:
        sentiment_emoji = "😊 Good"  # Positive sentiment
    elif sentiment_score < 0:
        sentiment_emoji = "😞 Negative"  # Negative sentiment
    else:
        sentiment_emoji = "😐 Neutral"  # Neutral sentiment

    return sentiment_emoji

def generate_word_cloud(text):
    wordcloud = WordCloud(width=800, height=400, random_state=21, max_font_size=110, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis('off')

    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_str

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    if request.method == 'POST':
        text = request.form['text']

        sentiment_emoji = analyze_sentiment(text)

        summarizer = Summarizer()
        summary = summarizer(text)

        wordcloud_img = generate_word_cloud(text)

        result_data = {
            'text': text,
            'sentiment_emoji': sentiment_emoji,
            'summary': summary,
            'wordcloud_img': wordcloud_img
        }

        return render_template('result.html', result=result_data)

if __name__ == '__main__':
    app.run(debug=True)
