import streamlit as st
from Transcript import Transcript
from Summarizer import Summarizer

def main():
    st.title("News Summarizer AIRIW Project by Nishan and Nishank")

    # Input for query
    query = st.text_input("Enter your query:")

    # Button to trigger summarization
    if st.button("Summarize"):
        # Fetch articles based on the query
        transcript = Transcript()
        combined_text = transcript.search_and_extract_articles(query)

        # Send the combined articles to the Summarizer
        summarizer = Summarizer()
        summarized_text = summarizer.summarize_with_tfidf(combined_text, per=0.1)

        # Display the summarized text
        st.subheader("Summarized Text:")
        st.write(summarized_text)

if __name__ == "__main__":
    main()
