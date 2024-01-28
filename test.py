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

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file:
        temp_dir = tempfile.mkdtemp()
        path = os.path.join(temp_dir, uploaded_file.name)
        with open(path, "wb") as f:
            f.write(uploaded_file.getvalue())
    if uploaded_file is not None:
        # use tempfile because CSVLoader only accepts a file_path
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name

        csv_loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
            'delimiter': ','})
        # Initialize chat history
        chat_history = ""
        user_input = st.text_input("Your Message:")
        print(user_input)
        #    try:
        data = csv_loader.load()
        if user_input:
            response = get_model_response(data, user_input)
            st.write(response)
            # Update chat history
            chat_history += f"User: {user_input}\nBot: {response}\n"
    #        print(data)
    # Chat interface

    #    except Exception as e:
    #      print(f"Error processing CSV file: {e}")


if __name__ == "__main__":
    main()
