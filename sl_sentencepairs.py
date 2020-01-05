import streamlit as st
import pandas as pd
import pickle

df = pd.read_csv('data/1000sents.csv')

#Index(['ID', 'HEADWORD', 'POS', 'ENGLISH', 'JAPANESE', 'SPANISH', 'INDONESIAN',
       #'EXAMPLE (KO)', 'EXAMPLE (EN)', 'EXAMPLE (JA)', 'EXAMPLE (ES)',
       #'EXAMPLE (ID)'],

# Selects a random sample
random_sample = df.sample(n=10)

if st.button('Random sample'):
	random_sample = df.sample(n=10)

options = ('한일 단어','한일 문장','일한 문장', 'EN to KO/JA')
selection = st.selectbox('Select',options)

if selection == '한일 단어':
	for index,row in random_sample.iterrows():
		st.write(str(index) + '.'+row['HEADWORD'])
		st.sidebar.markdown(str(index) + '. '+row['JAPANESE'])
elif selection == '한일 문장':
	for index,row in random_sample.iterrows():
		st.write(str(index) + '.'+row['EXAMPLE (KO)'])
		st.sidebar.markdown(str(index) + '. '+row['EXAMPLE (JA)'])

elif selection == '일한 문장':
	for index,row in random_sample.iterrows():
		st.write(str(index) + '.'+row['EXAMPLE (JA)'])
		st.sidebar.markdown(str(index) + '. '+row['EXAMPLE (KO)'])

elif selection == 'EN to KO/JA':
	for index,row in random_sample.iterrows():
		st.write(str(index) + '. '+row['EXAMPLE (EN)'])
		st.sidebar.markdown(str(index) + '. '+row['EXAMPLE (KO)'])
		st.sidebar.markdown(str(index) + '. '+row['EXAMPLE (JA)'])

