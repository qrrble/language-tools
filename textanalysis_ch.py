import jieba
import pickle
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
def ChTextAnalysis(txt):
	# Does word segmentation
	seg_list = jieba.cut(txt, cut_all=False)
	segmented_words = [x for x in seg_list]
	segmented_words = list(set(segmented_words))

	# Gets list of Chinese characters
	chn_character_word_dict = pickle.load(open('data/chn_character_word_dict.pkl', 'rb'))
	character_set = set(chn_character_word_dict.keys())
	character_list = [x for x in txt if x in character_set]

	words = []
	pinyin = []
	definitions = []

	# Chinese-English dictionary data
	CEDict_word_key_dict = pickle.load(open('data/CEDict_word_key_dict.pkl', 'rb'))
	for x in segmented_words:
	    word_info = CEDict_word_key_dict.get(x)
	    if word_info != None:
	        words.append(x)
	        pinyin.append(word_info['pinyin'][0])
	        definitions.append(word_info['def'][0])
	        
	df = pd.DataFrame({'Word':words, 'Pinyin':pinyin, 'Definitions':definitions})

	# Word frequency data
	chn_character_frequency_dict = pickle.load(open('data/chn_character_frequency_dict.pkl', 'rb'))
	frequency = [chn_character_frequency_dict.get(x) for x in df['Word']]
	df['Frequency'] = frequency

	# HSK word data
	hsk_vocab = pd.read_csv('data/hsk_vocab.csv')
	#hsk_vocab['Level'] = hsk_vocab['Level'].astype(str)
	hsk_vocab_dict = dict(zip(hsk_vocab['Character'].values, hsk_vocab['Level'].values))

	hsk_level = [hsk_vocab_dict.get(x) for x in df['Word'].values]
	df['Level'] = hsk_level
	#df['Level'].fillna('NA', inplace=True)

	st.write(df.sort_values(by=['Frequency']))

	# HSK character data
	hsk_char = pd.read_csv('data/hsk_char.csv')
	hsk_char_dict = dict(zip(hsk_char['Character'].values, hsk_char['Level'].values))

	character_levels = [hsk_char_dict.get(x) for x in character_list]


	# Plots distributions of word and character difficulties
	from collections import Counter
	hsk_word_level_count = Counter(df['Level'].values)

	fig = plt.figure(figsize=(9,4))
	fig.tight_layout()


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

	st.pyplot()