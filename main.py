import streamlit as st
from PIL import Image
import base64
import pandas as pd
import os
import time
import io

# Add these lines at the beginning of the script
if 'timer_count' not in st.session_state:
    st.session_state.timer_count = 0
if 'eliminated' not in st.session_state:
    st.session_state.eliminated = False

# Initialize variables
excel_file = None
df = None
user_number_column = None
password_column = None
uploaded_file = None
clue_column = None  # Add this line
image_column = None  # Add this line

def add_bg_from_image(image_file):
    with open(image_file, "rb") as file:
        encoded_string = base64.b64encode(file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def handle_sidebar_uploads(sidebar_password):
    changes = {
        'uploaded_file': None,
        'excel_file': None,
        'df': None,
        'user_number_column': None,
        'password_column': None,
        'clue_column': None,
        'image_column': None  # Add this line
    }

    entered_password = st.sidebar.text_input("Enter password to access sidebar", type="password")

    if entered_password == sidebar_password:
        with st.sidebar.expander("Upload Background Image", expanded=False):
            new_uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
            if new_uploaded_file is not None:
                changes['uploaded_file'] = new_uploaded_file

        with st.sidebar.expander("Upload User Data", expanded=False):
            new_excel_file = st.file_uploader("Upload Excel file with user data", type=["xlsx", "xls"])
            if new_excel_file is not None:
                changes['excel_file'] = new_excel_file
                df = pd.read_excel(new_excel_file)
                changes['df'] = df
                st.write("Columns in your Excel file:", df.columns.tolist())
                changes['user_number_column'] = st.selectbox("Select the column for User Number", df.columns)
                changes['password_column'] = st.selectbox("Select the column for Password", df.columns)
                changes['clue_column'] = st.selectbox("Select the column for Clue", df.columns)
                changes['image_column'] = st.selectbox("Select the column for Image Path", df.columns)  # Add this line
    else:
        if len(entered_password) > 0:
            st.sidebar.error("Incorrect password. Please enter the correct password to access the sidebar.")

    return changes

# Modify the countdown_timer function
def countdown_timer(duration):
    st.session_state.timer_count += 1
    if st.session_state.timer_count >= 5:
        st.session_state.eliminated = True
        st.rerun()
    
    placeholder = st.empty()
    for remaining in range(duration, 0, -1):
        placeholder.markdown(f"""
            <div style="
                position: fixed;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background-color: rgba(255, 0, 0, 0.8);
                padding: 20px;
                border-radius: 10px;
                text-align: center;
                z-index: 9999;
            ">
                <h2 style="color: white; font-size: 2em;">Time Freeze</h2>
                <p style="color: white; font-size: 1.5em;">Please wait {remaining} seconds</p>
                <p style="color: white; font-size: 1.2em;">Attempts left: {5 - st.session_state.timer_count}</p>
            </div>
        """, unsafe_allow_html=True)
        time.sleep(1)
    placeholder.empty()

# Add this function to display the elimination message
def show_elimination_message():
    st.markdown(f"""
        <div style="
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: rgba(255, 0, 0, 0.9);
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            z-index: 9999;
        ">
            <h1 style="color: white; font-size: 3em;">You are eliminated!</h1>
        </div>
    """, unsafe_allow_html=True)

# Main code
if st.session_state.eliminated:
    show_elimination_message()
else:
    sidebar_password = "22shrt2k24"
    uploaded_file = None
    excel_file = None
    df = None
    user_number_column = None
    password_column = None
    clue_column = None
    image_column = None

    # Call the function to handle sidebar uploads
    sidebar_changes = handle_sidebar_uploads(sidebar_password)

    # Update variables based on sidebar changes
    if sidebar_changes['uploaded_file'] == "remove":
        uploaded_file = None
        if os.path.exists("temp_bg.png"):
            os.remove("temp_bg.png")
    elif sidebar_changes['uploaded_file'] is not None:
        uploaded_file = sidebar_changes['uploaded_file']

    if sidebar_changes['excel_file'] == "remove":
        excel_file = None
        df = None
        user_number_column = None
        password_column = None
        clue_column = None  # Add this line
        image_column = None  # Add this line
    elif sidebar_changes['excel_file'] is not None:
        excel_file = sidebar_changes['excel_file']
        df = sidebar_changes['df']
        user_number_column = sidebar_changes['user_number_column']
        password_column = sidebar_changes['password_column']
        clue_column = sidebar_changes['clue_column']  # Add this line
        image_column = sidebar_changes['image_column']  # Add this line

    # User authentication form
    st.markdown("<h1 style='text-align: center; font-weight: bold; font-size: 2.5em;'>KEY TO TREASURE </h1>", unsafe_allow_html=True)

    # Custom HTML for input fields
    st.markdown("""
        <div style='font-size: 1.5em; font-weight: bold;'>
            <label for='user_number'>ENTER TEAM NUMBER</label>
        </div>
    """, unsafe_allow_html=True)
    user_number = st.text_input("", key="user_number")

    st.markdown("""
        <div style='font-size: 1.5em; font-weight: bold;'>
            <label for='password'>ENTER TEAM PASSCODE</label>
        </div>
    """, unsafe_allow_html=True)
    password = st.text_input("", type="password", key="password")

    submit_button = st.button("Submit")

    # Apply custom CSS to increase text size and make it bold for the submit button
    st.markdown("""
        <style>
        .stButton > button {
            font-size: 1.5em !important;
            font-weight: bold !important;
        }
        </style>
        """, unsafe_allow_html=True)

    if excel_file is not None and df is not None and user_number_column and password_column and clue_column and image_column:
        if submit_button:
            # Convert user_number to string and strip whitespace
            user_number = str(user_number).strip()
            
            # Convert the user number column to string and strip whitespace
            df[user_number_column] = df[user_number_column].astype(str).str.strip()
            
            # Check if user_number exists and password matches
            user_row = df[df[user_number_column] == user_number]
            if not user_row.empty:
                stored_password = str(user_row[password_column].values[0]).strip()
                if stored_password == password:
                    clue = user_row[clue_column].values[0]
                    image_path = user_row[image_column].values[0]
                    
                    # Display image and clue
                    st.markdown(f"""
                        <div style='
                            background-color: #f0f2f6;
                            padding: 20px;
                            border-radius: 10px;
                            border: 2px solid #FF0000;
                            text-align: center;
                        '>
                            <h2 style='color: #FF0000; font-weight: bold;'>Clue</h2>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Display image
                    if image_path and os.path.exists(image_path):
                        try:
                            with open(image_path, "rb") as image_file:
                                image_data = image_file.read()
                            image = Image.open(io.BytesIO(image_data))
                            st.image(image, use_column_width=True)
                        except Exception as e:
                            st.error(f"Error loading image: {e}")
                    else:
                        st.warning("Image not found or invalid path.")
                    
                    # Display clue text
                    st.markdown(f"""
                        <div style='
                            background-color: #f0f2f6;
                            padding: 20px;
                            border-radius: 10px;
                            text-align: center;
                        '>
                            <p style='font-size: 1.5em; font-weight: bold; color: #FF0000;'>{clue}</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Invalid password.")
                    countdown_timer(30)
            else:
                st.error(f"User number '{user_number}' not found.")
                countdown_timer(30)
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        
        # Save the uploaded image temporarily
        with open("temp_bg.png", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Set the background
        add_bg_from_image("temp_bg.png")

# Add this at the end of the script
if st.session_state.eliminated:
    # Remove files
    if os.path.exists("temp_bg.png"):
        os.remove("temp_bg.png")
    # Reset other variables as needed
    uploaded_file = None
    excel_file = None
    df = None
    user_number_column = None
    password_column = None
    clue_column = None
    image_column = None
