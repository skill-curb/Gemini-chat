import streamlit as st
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
from utils import *


# Main app
def main():
    st.title("Chat with CSV using Gemini Pro")

    # File uploader
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

    # Fetching path of the uploaded file

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
            print(tmp_file_path)

            # Initializing CSV_Loader
            csv_loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
                'delimiter': ','})

            # Load data into csv loader
            data = csv_loader.load()

            # Initialize chat Interface
            user_input = st.text_input("Your Message:")
            print(user_input)
            print(data)

            if user_input:

                response = get_model_response(data, user_input)
                st.write(response)



if __name__ == "__main__":
    main()

