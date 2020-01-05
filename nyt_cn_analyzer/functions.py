import requests
from bs4 import BeautifulSoup
import os
import io
import base64
import jieba
import pickle
import pandas as pd
import matplotlib.pyplot as plt

def GetNYTHeadlines():
    r1 = requests.get('https://cn.nytimes.com/')
    coverpage = r1.content
    soup = BeautifulSoup(coverpage)

    headline_data = soup.find_all('h3',class_='regularSummaryHeadline')

    frontpage_articles = {}
    for x in headline_data:
        article_url = 'https://cn.nytimes.com'+x.find('a')['href']+'dual/'
        article_title = x.get_text()
        frontpage_articles[article_title] = article_url
    
    return frontpage_articles

def GetDualArticleText(input_url):
	# Downloads page and soup data
    r1 = requests.get(input_url)
    coverpage = r1.content
    bilingual_soup = BeautifulSoup(coverpage)

    # Error handling for bad webpages
    active_links = bilingual_soup.find_all('a',class_="active")
    if active_links == None:
        return None, None, None

    bilingual_setting = None
    for x in active_links:
        span_tag = x.find('span',class_='setting-btn-text')
        if span_tag != None:
            bilingual_setting = span_tag.get_text()
        
    if bilingual_setting != '中英双语':
        return None, None, None
    
    # Title of article
    ch_title = bilingual_soup.find('div', class_='article-header').find('h1').get_text()
    en_title = bilingual_soup.find('h1',class_='en-title').get_text()

    # Extracts dual language paragraphs
    dual_items = bilingual_soup.find_all('div',class_='row article-dual-body-item')

    # Splits up English and Chinese paragraphs
    eng_items = []
    ch_items = []
    for x in dual_items:
        paragraphs = x.find_all('div',class_='article-paragraph')
        en_paragraph = paragraphs[0].get_text().replace(u'\xa0', u' ')
        ch_paragraph = paragraphs[1].get_text()
        eng_items.append(en_paragraph)
        ch_items.append(ch_paragraph)

    return en_title, ch_title, eng_items, ch_items

def ChTextAnalysis(ch_text):
	# Joins list of strings into one big string
	txt = ''.join(ch_text)
	#print('ch test',ch_text)
	# Loops over paragraphs and does word segmentation
	seg_list = []
	segmented_paragraphs = []
	for x in ch_text:
		#print('x',x)
		seg_list_para = jieba.cut(x, cut_all=False) # Generator object
		segmented_words_para = [x for x in seg_list_para] # Loops through generator to create list
		seg_list += segmented_words_para
		#print(segmented_words_para)

		segmented_paragraphs.append(segmented_words_para) 

	# Finds set of unique segmented words
	seg_list = jieba.cut(txt, cut_all=False)
	segmented_words = [x for x in seg_list]
	segmented_words = list(set(segmented_words))

	# Gets list of Chinese characters
	chn_character_word_dict = pickle.load(open('../data/chn_character_word_dict.pkl', 'rb'))
	character_set = set(chn_character_word_dict.keys())
	character_list = [x for x in txt if x in character_set]

	words = []
	pinyin = []
	definitions = []

	# Chinese-English dictionary data
	CEDict_word_key_dict = pickle.load(open('../data/CEDict_word_key_dict.pkl', 'rb'))
	for x in segmented_words:
	    word_info = CEDict_word_key_dict.get(x)
	    if word_info != None:
	        words.append(x)
	        pinyin.append(word_info['pinyin'][0])
	        definitions.append(word_info['def'][0])
	        
	df = pd.DataFrame({'Word':words, 'Pinyin':pinyin, 'Definitions':definitions})

	# Processes segmented_paragraphs and adds HTML for mouseover text to each of the segmented words
	mouseover_paragraphs = []
	for paragraph in segmented_paragraphs: # Loops over paragraphs, stored as lists
		paragraph_string = ''
		for word in paragraph: # Loops over segmented words
			word_info = CEDict_word_key_dict.get(word)

			if word_info != None:
				pinyin = word_info['pinyin'][0]
				definition = word_info['def'][0]

				lookup_string = " '{} ({}): {}' "
				lookup_string = lookup_string.format(word, pinyin, definition)

				span_string = "<span style='color:15035E' title={}>{}</span>"
				span_string = span_string.format(lookup_string, word)

			else:
				span_string = word

			paragraph_string += span_string

		mouseover_paragraphs.append(paragraph_string)


	# Word frequency data
	chn_character_frequency_dict = pickle.load(open('../data/chn_character_frequency_dict.pkl', 'rb'))
	frequency = [chn_character_frequency_dict.get(x) for x in df['Word']]
	df['Frequency'] = frequency

	# HSK word data
	hsk_vocab = pd.read_csv('../data/hsk_vocab.csv')
	#hsk_vocab['Level'] = hsk_vocab['Level'].astype(str)
	hsk_vocab_dict = dict(zip(hsk_vocab['Character'].values, hsk_vocab['Level'].values))

	hsk_level = [hsk_vocab_dict.get(x) for x in df['Word'].values]
	df['Level'] = hsk_level
	#df['Level'].fillna('NA', inplace=True)

	#df = df.sort_values(by=['Frequency']) # Sorts dataframe

	# HSK character data
	hsk_char = pd.read_csv('../data/hsk_char.csv')
	hsk_char_dict = dict(zip(hsk_char['Character'].values, hsk_char['Level'].values))

	character_levels = [hsk_char_dict.get(x) for x in character_list]


	# Plots distributions of word and character difficulties
	from collections import Counter

	difficulty_values = [x for x in df['Level'].values if x==x]
	hsk_word_level_count = Counter(difficulty_values)
	#print(hsk_word_level_count)
	img = io.BytesIO()

	fig = plt.figure(figsize=(9,4))
	#fig.tight_layout()

	plt.subplot(1, 2, 1)
	plt.bar(hsk_word_level_count.keys(),hsk_word_level_count.values())
	plt.title('Word difficulty distribution')
	plt.xlabel('HSK level')
	plt.ylabel('Count')
	plt.grid(True)

	hsk_character_level_count = Counter(character_levels)
	hsk_character_level_count.pop(None)

	plt.subplot(1, 2, 2)
	plt.bar(hsk_character_level_count.keys(),hsk_character_level_count.values())
	plt.title('Character difficulty distribution')
	plt.xlabel('HSK level')
	plt.ylabel('Count')
	plt.grid(True)
	plt.savefig(img, format='png')
	img.seek(0)

	graph_url = base64.b64encode(img.getvalue()).decode()

	plt.close() 
	return df, 'data:image/png;base64,{}'.format(graph_url), mouseover_paragraphs