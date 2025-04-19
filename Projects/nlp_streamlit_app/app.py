import streamlit as st

#NLP packages
import spacy
from txtblob import TextBlob

#other packages

def text_analyzer(my_text):
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(my_text)
    tokens = [token.text for token in docx]
    return tokens


def main():
    st.title("NLP Streamlit App")
    st.subheader("Natural Language Processing on the Go")

    # tokenization
    if st.checkbox("Show Tokens amd Lemma"):
        st.subheader("Tokenize your text")
        message = st.text_area("Enter your text here", placeholder="Type Here")	
        if st.button("Analyze"):
            nlp_reslt = text_analyzer(message)
            st.success(nlp_reslt)
        



    # named entity recognition

    # sentiment analysis

    # text summarization
if __name__ == "__main__":
    main()
    