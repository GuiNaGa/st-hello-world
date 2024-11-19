import streamlit as st
import pandas as pd
import plotly.express as px

# CSS Styles
def apply_css():
    st.markdown(
        """
        <style>
        /* General Styles */
        body {
            background-color: black;
            color: white;
            font-family: 'Arial', sans-serif;
        }
        h1, h2, h3 {
            color: red;
        }
        .stSelectbox, .stSlider, .stCheckbox {
            background-color: black;
            color: white;
        }
        .stButton button {
            background-color: red;
            color: white;
            border-radius: 5px;
            border: none;
        }
        .stButton button:hover {
            background-color: darkred;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# Apply CSS
apply_css()

# Menu
menu = ["Home", "Data Analysis","EDA", "Visualizations"]
choice = st.sidebar.selectbox("Menu", menu)

# Load data function with auto-refresh
@st.fragment(run_every=2)
def load_data():
    gsheetid = '1Rg6NLfs3cgC4dC5IBQOikYdLGuWsr7c5lcoO0OjDPx4'
    sheetname = '1282294220'
    url = f'https://docs.google.com/spreadsheets/d/{gsheetid}/export?format=csv&gid={sheetname}&format'
    return pd.read_csv(url)

df = load_data()

if choice == "Home":
    st.title("F1 Insights Application")
    st.subheader("Welcome to the F1 Data Analysis App")
    st.text(
        "Explore the performance trends of F1 drivers, analyze race statistics, and uncover patterns. "
        "Use the navigation menu to explore different sections of the app."
    )
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/F1.svg/1200px-F1.svg.png", use_container_width=True)
    st.caption("Developed by :red[Guillermo Navarro] 😎👽")

elif choice == "Data Analysis":
    st.title("Data Overview and Filters")
    nationality_filter = st.selectbox("Select Nationality:", options=df["Nationality"].unique())
    filtered_df = df[df["Nationality"] == nationality_filter]

    race_entry_min = int(df["Race_Entries"].min())
    race_entry_max = int(df["Race_Entries"].max())
    race_entry_range = st.slider(
        "Select Range for Race Entries:",
        min_value=race_entry_min,
        max_value=race_entry_max,
        value=(race_entry_min, race_entry_max),
    )
    filtered_df = filtered_df[
        (filtered_df["Race_Entries"] >= race_entry_range[0]) & (filtered_df["Race_Entries"] <= race_entry_range[1])
    ]

    show_podiums = st.checkbox("Show Podiums Column")
    if not show_podiums:
        filtered_df = filtered_df.drop(columns=["Podiums"])

    st.write("### Filtered Dataset")
    st.dataframe(filtered_df)
elif choice == "EDA":
    st.title("Exploratory Data Analysis")
    st.write("### Dataset Summary")
    st.write(df.describe())

elif choice == "Visualizations":
    st.title("Visualizations")
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    # Histogram of Race Entries
    with col1:
        st.write("### Histogram of Race Entries")
        fig_histogram = px.histogram(df, x="Race_Entries", title="Race Entries Distribution")
        st.plotly_chart(fig_histogram)

    # Bar Chart of Podiums by Nationality
    with col2:
        st.write("### Podiums by Nationality")
        fig_bar = px.bar(df, x="Nationality", y="Podiums", title="Podiums by Nationality")
        st.plotly_chart(fig_bar)

    # Scatter Plot of Race Entries vs Podiums
    with col3:
        st.write("### Race Entries vs Podiums")
        fig_scatter = px.scatter(df, x="Race_Entries", y="Podiums", title="Race Entries vs Podiums")
        st.plotly_chart(fig_scatter)

    # Bar plot with race entries over time
    with col4:
        st.write("### Race Entries Over Time")
        fig_bar_time = px.bar(df, x="Decade", y="Race_Entries", title="Race Entries Over Time")
        st.plotly_chart(fig_bar_time)

