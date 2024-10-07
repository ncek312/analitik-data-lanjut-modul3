import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import mysql.connector

# Function to establish connection to MySQL
def get_connection():
    connection = mysql.connector.connect(
        host='localhost',  # e.g., "localhost"
        user='root',
        password='',
        database='db_dal'
    )
    return connection

# Function to fetch data from the database
def get_data_from_db():
    conn = get_connection()
    query = "SELECT * FROM pddikti_examples"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Title of the app
st.title('Streamlit Simple App')

# Adding sidebar navigation
page = st.sidebar.radio("Pilih halaman", ["Dataset", "Visualisasi", "Form Input"])

# Dataset Page
if page == "Dataset":
    st.header("Halaman Dataset")
    
    # Fetch data from the database
    data = get_data_from_db()

    # Display data in Streamlit
    st.write(data)

# Visualization Page
elif page == "Visualisasi":
    st.header("Halaman Visualisasi")
    
    # Fetch data from the database
    data = pd.read_csv("pddikti_examples.csv")

    # Filter by university
    selected_university = st.selectbox('Pilih Universitas', data['universitas'].unique())
    filtered_data = data[data['universitas'] == selected_university]

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(12, 6))

    for prog_studi in filtered_data['program_studi'].unique():
        subset = filtered_data[filtered_data['program_studi'] == prog_studi]
        subset = subset.sort_values(by='id', ascending=False)
        ax.plot(subset['semester'], subset['jumlah'], label=prog_studi)

    # Set plot titles and labels
    ax.set_title(f"Visualisasi Data untuk {selected_university}")
    ax.set_xlabel('Semester')
    ax.set_ylabel('Jumlah')
    ax.legend()
    plt.xticks(rotation=90)  # Rotate x-axis labels vertically

    # Display figure in Streamlit
    st.pyplot(fig)

# Form Input Page
elif page == "Form Input":
    st.header("Halaman Form Input")
    
    # Input form
    with st.form(key='input_form'):
        input_semester = st.text_input('Semester')
        input_jumlah = st.number_input('Jumlah', min_value=0, format='%d')
        input_program_studi = st.text_input('Program Studi')
        input_universitas = st.text_input('Universitas')
        submit_button = st.form_submit_button(label='Submit Data')

    # On form submit, insert data into the database
    if submit_button:
        conn = get_connection()
        cursor = conn.cursor()
        query = """
        INSERT INTO pddikti_examples(semester, jumlah, program_studi, universitas)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (input_semester, input_jumlah, input_program_studi, input_universitas))
        conn.commit()
        conn.close()
        st.success("Data successfully submitted to the database!")
