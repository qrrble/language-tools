import streamlit as st
import pandas as pd
import pickle

# Reads in pickle files
with open('data/ch_word_to_sentencenum_dict.pkl', 'rb') as handle:
    ch_word_to_sentencenum_dict = pickle.load(handle)

with open('data/num_ch_sentence_dict.pkl', 'rb') as handle:
    num_ch_sentence_dict	 = pickle.load(handle)
with open('data/num_eng_sentence_dict.pkl', 'rb') as handle:
    num_eng_sentence_dict = pickle.load(handle)
with open('data/num_kor_sentence_dict.pkl', 'rb') as handle:
    num_kor_sentence_dict = pickle.load(handle)


st.header('Chinese sentence lookup')
input_word = st.text_input('Enter a Chinese word', value='实验室')

sentence_numbers = ch_word_to_sentencenum_dict.get(input_word)
if sentence_numbers != None:
	for x in sentence_numbers:
		st.write(num_ch_sentence_dict[x])
		st.write(num_eng_sentence_dict[x])
else:
	st.write('Word not found!')