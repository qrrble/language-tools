import streamlit as st
import pandas as pd
import pickle

# Reads in pickle files
ch_word_to_sentencenum_dict = pickle.load(open('data/ch_word_to_sentencenum_dict.pkl', 'rb'))
num_CEK60k_sentence_dict = pickle.load(open('data/num_CEK60k_sentence_dict.pkl', 'rb'))
CEDict_word_key_dict = pickle.load(open('data/CEDict_word_key_dict.pkl', 'rb'))
chn_character_word_dict = pickle.load(open('data/chn_character_word_dict.pkl', 'rb'))
pinyin_char_dict = pickle.load(open('data/pinyin_char_dict.pkl', 'rb'))
chn_char_radical_dict = pickle.load(open('data/chn_char_radical_dict.pkl', 'rb'))
heisig_rsh_dict = pickle.load(open('data/heisig_rsh_dict.pkl', 'rb'))

#########################

st.header('Chinese dictionary lookup')
input_word = st.text_input('Enter a Chinese character/word', value='实')

search_option = st.radio('Search type', ('Character', 'Word'))

#########################
wordinfo = CEDict_word_key_dict.get(input_word)

st.subheader('Pinyin:')

if wordinfo != None:
	pinyin = wordinfo.get('pinyin')
	for x in pinyin:
		st.write(x)
else:
	st.write('[Not found]')

st.subheader('Definition:')
if wordinfo != None:
	meaning = wordinfo.get('def')
	for x in meaning:
		st.write(x)
else:
	st.write('[Not found]')

#########################
if search_option == 'Character' and pinyin != None:
	st.subheader('Characters with same pronunciation:')
	homophones = ''
	for x in pinyin:
		words_with_same_pinyin = pinyin_char_dict.get(x)

		if words_with_same_pinyin != None:
			new_homophones = ''.join(words_with_same_pinyin)
			homophones += new_homophones
	homophones = list(set(homophones))
	homophones.sort()
	st.write(''.join(homophones))

#########################
if search_option == 'Character':
	st.subheader('Radical decomposition:')
	radicals = chn_char_radical_dict[input_word]
	st.write(''.join(radicals))

#########################
heisig_info = heisig_rsh_dict.get(input_word)
if search_option == 'Character' and heisig_info!= None:
	st.subheader('Heisig keyword:')
	st.write(heisig_info['Keyword'])

	st.subheader('Kanji equivalent:')
	st.write(heisig_info['Kanji'])

#########################
if search_option == 'Character':
	st.subheader('Words containing character:')
	words_with_char = chn_character_word_dict.get(input_word)

	if words_with_char != None:
		word_list = []
		word_pinyin = []
		word_definition = []
		for x in words_with_char:
			x_info = CEDict_word_key_dict.get(x)
			if x_info != None:
				word_list.append(x)
				word_pinyin.append(x_info['pinyin'][0])
				word_definition.append(x_info['def'][0])

		wordlist_df = pd.DataFrame({'Word':word_list,'Pinyin':word_pinyin,'Definition':word_definition})
		st.write(wordlist_df)
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