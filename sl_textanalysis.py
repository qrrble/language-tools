import streamlit as st
import time


st.header('Text analyzer')
language_options = ('Chinese', 'Finnish')
language = st.selectbox('Select language',language_options)
txt = st.text_area('Text to analyze')

#######
if language == 'Chinese':
	from textanalysis_ch import * 
	start = time.time()
	ChTextAnalysis(txt)
	end = time.time()

	t_elapsed = end - start
	st.write('Processing time (s): '+str(t_elapsed))

elif language == 'Finnish':
	st.write('Coming soon...')