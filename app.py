import streamlit as st
from file_processing import process_uploaded_files, display_processed_files
from data_analysis import perform_data_analysis
from chatbox import chatbox_functionality

def main():
    st.set_page_config(page_title="Data Analysis and Chatbot", page_icon=":robot_face:")

    st.title("Data Analysis and Chatbot")

    # Allow user to upload file(s)
    uploaded_files = st.file_uploader("Upload File(s):", accept_multiple_files=True)

    # Process the uploaded files
    if uploaded_files:
        dataframes, uploaded_file_names = process_uploaded_files(uploaded_files)
        display_processed_files(dataframes, uploaded_file_names)

        # Allow user to select mode
        mode = st.radio("Select Mode:", ("Data Analysis", "Chatbox"))

        # Based on the selected mode, perform corresponding functionality
        if mode == "Data Analysis":
            perform_data_analysis(dataframes, uploaded_file_names)
        elif mode == "Chatbox":
            chatbox_functionality(dataframes, uploaded_file_names)

if __name__ == "__main__":
    main()
