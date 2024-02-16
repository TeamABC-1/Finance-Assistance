import streamlit as st
import re
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import PyPDF2
import io

nltk.download('punkt')
nltk.download('stopwords')

# Function to extract important sentences from a PDF based on keywords
def extract_important_sentences_from_pdf(uploaded_file, keywords):
    pdf_reader = PyPDF2.PdfFileReader(uploaded_file)

    important_sentences = []

    for page_number in range(pdf_reader.numPages):
        page = pdf_reader.getPage(page_number)
        page_text = page.extractText()

        sentences = sent_tokenize(page_text)
        words = word_tokenize(page_text)
        stop_words = set(stopwords.words('english'))
        words = [word for word in words if word.lower() not in stop_words]

        fdist = FreqDist(words)

        for sentence in sentences:
            if any(keyword.lower() in sentence.lower() for keyword in keywords):
                important_sentences.append(sentence)

    important_sentences_text = '\n'.join(important_sentences)
    return important_sentences_text

# Streamlit app
def main():
    st.title("Document analyser")

    # File upload widget
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        keywords = st.text_input("Enter keywords separated by commas").split(',')

        # Extracting important sentences from the PDF based on keywords
        important_sentences = extract_important_sentences_from_pdf(uploaded_file, keywords)

        # Display the important sentences
        st.subheader("Summarization of Document:")
        st.text(important_sentences)

        # Display the first 500 characters of important sentences
        st.subheader("Important Sentences:")
        st.text(important_sentences[:500])

if __name__ == "__main__":
    main()


       

