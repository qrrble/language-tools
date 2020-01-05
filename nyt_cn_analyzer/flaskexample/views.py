from flaskexample import app
from flask import render_template
from flask import request
from functions import *

@app.route('/')
def index():
    frontpage_articles = GetNYTHeadlines()

    return render_template("index.html", frontpage_articles = frontpage_articles)

@app.route('/', methods=['POST'])
def my_form_post():

    article_url = request.form['url'] # Parses URL input from index page
    #print('yt_url',yt_url)

    # Scrapes article text from website
    en_title, ch_title, eng_text, ch_text = GetDualArticleText(article_url)
    
    if en_title == None:
    	return 'Bad webpage!'

    # Does analysis of vocab in article, and creates difficulty plot
    vocab_df, difficulty_plot, ch_marked_para = ChTextAnalysis(ch_text)

    vocab_data = zip(vocab_df['Word'].values, vocab_df['Pinyin'].values, \
        vocab_df['Definitions'].values, vocab_df['Frequency'].values, \
        vocab_df['Level'].values, )

    #article_text = zip(eng_text, ch_text)
    article_text = zip(eng_text, ch_marked_para)
    
    return render_template("result.html",\
        article_url=article_url, \
        article_text = article_text, \
        en_title = en_title, \
        ch_title = ch_title,\
        difficulty_plot = difficulty_plot,\
        vocab_data = vocab_data)