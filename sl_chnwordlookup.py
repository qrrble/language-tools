import streamlit as st
import pandas as pd
import pickle

# Reads in pickle files
with open('data/ch_word_to_sentencenum_dict.pkl', 'rb') as handle:
    ch_word_to_sentencenum_dict = pickle.load(handle)

with open('data/num_CEK60k_sentence_dict.pkl', 'rb') as handle:
    num_CEK60k_sentence_dict	 = pickle.load(handle)

with open('data/CEDict_word_key_dict.pkl', 'rb') as handle:
    CEDict_word_key_dict = pickle.load(handle)

#########################

st.header('Chinese word lookup')
input_word = st.text_input('Enter a Chinese word', value='实验室')

#########################
wordinfo = CEDict_word_key_dict.get(input_word)

st.subheader('Pinyin:')

if wordinfo != None:
	pinyin = wordinfo.get('pinyin')
	st.write(pinyin)
else:
	st.write('[Not found]')

st.subheader('Definition:')
if wordinfo != None:
	meaning = wordinfo.get('def')
	st.write(meaning)
else:
	st.write('[Not found]')

#########################

st.subheader('Example sentences:')
sentence_numbers = ch_word_to_sentencenum_dict.get(input_word)
if sentence_numbers != None:
	for x in sentence_numbers[:20]:
		st.write(num_CEK60k_sentence_dict[x]['chn']+'\n'+num_CEK60k_sentence_dict[x]['eng'])
		#st.write()
else:
	st.write('Word not found!')