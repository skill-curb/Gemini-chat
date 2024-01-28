from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import streamlit as st
from pypdf import PdfReader
import os
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI

genai.configure(api_key="AIzaSyBRkhTYu6Is6Q_Yvkrd_s8v_caZrcUK4nM")
os.environ["GOOGLE_API_KEY"] = "AIzaSyBRkhTYu6Is6Q_Yvkrd_s8v_caZrcUK4nM"

#Function to extract text from the pdf files
def get_text(files_pdf):
    text=""
    for pdf in files_pdf:
        pdf_reader= PdfReader(pdf)
        for page in pdf_reader.pages:
            text+= page.extract_text()

    print("Text Extracted")
    return text

# Function to get response from GEMINI PRO
def get_model_response(docs, query):

    #Extract text from pdf files
    text=get_text(docs)

    # Split the context text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=200)
    data_chunks = text_splitter.split_text(text)
    print(("Text Splitted"))

    #Initialize Model for embeddings
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    #Create vectors for chain using FAISS vectore store
    vectors = FAISS.from_texts(data_chunks, embeddings).as_retriever()

    print(("Vectors created"))


    model = ChatGoogleGenerativeAI(model="gemini-pro",temperature=0.9, convert_system_message_to_human=True)


    history = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

    chain = ConversationalRetrievalChain.from_llm(llm=model, retriever=vectors, memory=history)
    response=chain.run(query)
    print(response)
    return response



# Main app
def main():
    st.title("💬Chat With Your PDFs")

    # File uploader
    docs = st.sidebar.file_uploader("Upload your files", accept_multiple_files=True, type="pdf")

    if docs:
        # Chat interface
        user_input = st.text_input("Your Question:")
        submit = st.button("Fetch Answer")

        print(user_input)

        if user_input:
            if submit:
                with st.spinner("Processing"):
                    response =get_model_response(docs,user_input)
                    st.write(response)


if __name__ == "__main__":
    main()