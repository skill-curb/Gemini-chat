from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.document_loaders.csv_loader import CSVLoader
from langchain.chains.question_answering import load_qa_chain
import streamlit as st
import os
import tempfile
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

genai.configure(api_key="AIzaSyBRkhTYu6Is6Q_Yvkrd_s8v_caZrcUK4nM")
os.environ["GOOGLE_API_KEY"] = "AIzaSyBRkhTYu6Is6Q_Yvkrd_s8v_caZrcUK4nM"


# Function to get response from GEMINI PRO
def get_model_response(file, query):
    # Split the context text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    context = "\n\n".join(str(p.page_content) for p in file)

    data = text_splitter.split_text(context)

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    searcher = Chroma.from_texts(data, embeddings).as_retriever()

    q = "Which employee has maximum salary?"
    records = searcher.get_relevant_documents(q)
    print(records)

    prompt_template = """
      You have to answer the question from the provided context and make sure that you provide all the details\n
      Context: {context}?\n
      Question:{question}\n

      Answer:
    """

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    model = ChatGoogleGenerativeAI(model="gemini-pro",
                                   temperature=0.9)

    chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    response = chain(
        {
            "input_documents": records,
            "question": query
        }
        , return_only_outputs=True)

    return response['output_text']


# Main app
def main():
    st.title("Chat with CSV using Gemini Pro")
    st.image('path/to/image', use_column_width=True)
    uploaded_file = st.file_uploader("Upload your file", type=['pdf'], accept_multiple_files=False)
    user_question = st.text_input("Your question:")
    if st.button("Get Response") and uploaded_file is not None and user_question:
        with st.spinner('Getting response...'):
            response = get_model_response(uploaded_file, user_question)
        st.write(response)

   

if __name__ == "__main__":
    main()
