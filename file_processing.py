import os
import zipfile
import pandas as pd
import streamlit as st

def process_uploaded_files(uploaded_files):
    dataframes = []
    uploaded_file_names = []
    for uploaded_file in uploaded_files:
        file_extension = os.path.splitext(uploaded_file.name)[1]
        if file_extension.lower() == ".zip":
            # Create a temporary directory to extract the contents of the .zip file
            temp_dir = "temp_zip_extract"
            os.makedirs(temp_dir, exist_ok=True)
            
            # Extract the contents of the .zip file to the temporary directory
            with zipfile.ZipFile(uploaded_file, "r") as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Process each extracted file
            for filename in os.listdir(temp_dir):
                filepath = os.path.join(temp_dir, filename)
                if filename.endswith(".csv"):
                    dataframe = pd.read_csv(filepath)
                elif filename.endswith((".xls", ".xlsx", "xlsm", ".xlsb")):
                    dataframe = pd.read_excel(filepath)
                elif filename.endswith(".txt"):
                    # Check the second line of the file to determine the delimiter
                    with open(filepath, 'r') as f:
                        # Skip the first line
                        next(f)
                        second_line = f.readline().strip()
                        delimiter = "|" if "|" in second_line else "\t"  # Assume "|" delimiter for .psv, "\t" for .tsv

                        # Reset file pointer to the beginning of the file
                        f.seek(0)

                        # Read the file using pandas read_csv
                        dataframe = pd.read_csv(f, delimiter=delimiter)
                else:
                    st.warning(f"Unsupported file format: {filename}")
                    continue
                dataframes.append(dataframe)
                uploaded_file_names.append(filename)
            
            # Remove the temporary directory and its contents
            if os.path.exists(temp_dir):
                for root, dirs, files in os.walk(temp_dir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(temp_dir)
            
        elif file_extension.lower() in [".csv", ".xls", ".xlsx", "xlsm", ".xlsb", ".txt"]:
            # Process single file uploads as usual
            if file_extension.lower() == ".csv":
                dataframe = pd.read_csv(uploaded_file)
            elif file_extension.lower() in [".xls", ".xlsx", "xlsm", ".xlsb"]:
                dataframe = pd.read_excel(uploaded_file)
            elif file_extension.lower() == ".txt":
                # Check the second line of the file to determine the delimiter
                with uploaded_file as f:
                    # Skip the first line
                    next(f)
                    second_line = f.readline().decode().strip()  # decode bytes to string
                    delimiter = "|" if "|" in second_line else "\t"  # Assume "|" delimiter for .psv, "\t" for .tsv

                    # Reset file pointer to the beginning of the file
                    f.seek(0)

                    # Read the file using pandas read_csv
                    dataframe = pd.read_csv(f, delimiter=delimiter)
            dataframes.append(dataframe)
            uploaded_file_names.append(uploaded_file.name)
        else:
            st.warning(f"Unsupported file format: {file_extension}")
    return dataframes, uploaded_file_names


def display_processed_files(dataframes, uploaded_file_names):
    if dataframes:
        st.write("Processed Files:")
        for idx, dataframe in enumerate(dataframes):
            st.write(f"{idx + 1}.{uploaded_file_names[idx]}")
            st.write(dataframe)
