import streamlit as st
import pandas as pd
import os
from io import BytesIO
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Data Sweeper", layout="wide")

# Custom CSS for styling the app with dark mode aesthetics
st.markdown(
    """
    <style>
        /* Dark mode styles */
        [data-theme="dark"] {
            background-color: #121212;
            color: white;
        }
        [data-theme="dark"] .stButton>button {
            background-color: #0078D7;
            color: white;
        }
        [data-theme="dark"] .stButton>button:hover {
            background-color: #005a9e;
        }
        [data-theme="dark"] .stRadio>label, [data-theme="dark"] .stCheckbox>label {
            color: white;
        }
        [data-theme="dark"] .stDataFrame, [data-theme="dark"] .stTable {
            background-color: #1e1e1e;
            color: white;
        }
        /* Enhanced visualization styling */
        .stPlotlyChart, .stPyplot {
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
            padding: 1rem;
            background-color: transparent;
        }
        .stPlotlyChart {
            background-color: transparent;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation and theme toggle
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Visualization options
    st.write("**📊 Visualization Options**")
    visualization_type = st.selectbox("Choose Visualization Type", ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart", "Box Plot", "Heatmap"])
    
    # Additional sidebar options
    st.markdown("---")
    st.write("**🔧 Additional Options**")
    show_summary = st.checkbox("Show Data Summary")
    show_correlation = st.checkbox("Show Correlation Matrix")
    show_missing_values = st.checkbox("Show Missing Values Analysis")
    show_outliers = st.checkbox("Show Outliers Analysis")

# Apply the dark theme
st.markdown('<div data-theme="dark">', unsafe_allow_html=True)

# Main app title and introductory text
st.title("Advanced Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization.")

# File uploader widget
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Processing logic for uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_extension}")
            continue
        
        st.write(f"**📄 File Name:** {file.name}")
        st.write(f"**📏 File Size:** {file.size / 1024:.2f} KB")

        st.write("🔍 Preview of the Uploaded File:")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")
                if st.button(f"Drop Columns from {file.name}"):
                    columns_to_drop = st.multiselect("Select columns to drop", df.columns)
                    df.drop(columns=columns_to_drop, inplace=True)
                    st.write(f"Dropped columns: {columns_to_drop}")
            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing Values in Numeric Columns Filled with Column Means!")
                if st.button(f"Handle Categorical Data for {file.name}"):
                    categorical_cols = df.select_dtypes(include=['object']).columns
                    df[categorical_cols] = df[categorical_cols].fillna("Unknown")
                    st.write("Categorical Data Handled!")

        # Column selection for conversion
        st.subheader("🎯 Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Data visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            numeric_cols = df.select_dtypes(include='number').columns
            if len(numeric_cols) >= 2:
                if visualization_type == "Bar Chart":
                    fig = px.bar(df, x=numeric_cols[0], y=numeric_cols[1], title="Bar Chart")
                    st.plotly_chart(fig)
                elif visualization_type == "Line Chart":
                    fig = px.line(df, x=numeric_cols[0], y=numeric_cols[1], title="Line Chart")
                    st.plotly_chart(fig)
                elif visualization_type == "Scatter Plot":
                    fig = px.scatter(df, x=numeric_cols[0], y=numeric_cols[1], title="Scatter Plot")
                    st.plotly_chart(fig)
                elif visualization_type == "Histogram":
                    fig = px.histogram(df, x=numeric_cols[0], title="Histogram")
                    st.plotly_chart(fig)
                elif visualization_type == "Pie Chart":
                    fig = px.pie(df, names=df.columns[0], values=df[numeric_cols[0]], title="Pie Chart")
                    st.plotly_chart(fig)
                elif visualization_type == "Box Plot":
                    fig = px.box(df, y=numeric_cols, title="Box Plot")
                    st.plotly_chart(fig)
                elif visualization_type == "Heatmap":
                    corr = df[numeric_cols].corr()
                    fig = px.imshow(corr, text_auto=True, title="Heatmap")
                    st.plotly_chart(fig)
            else:
                st.warning("Not enough numeric columns for visualization.")

        # Additional options
        if show_summary:
            st.subheader("📝 Data Summary")
            st.write(df.describe())

        if show_correlation:
            st.subheader("📈 Correlation Matrix")
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                corr = numeric_df.corr()
                fig = px.imshow(corr, text_auto=True, title="Correlation Matrix")
                st.plotly_chart(fig)
            else:
                st.warning("No numeric columns available for correlation matrix.")

        if show_missing_values:
            st.subheader("🔍 Missing Values Analysis")
            missing_values = df.isnull().sum()
            st.write(missing_values)

        if show_outliers:
            st.subheader("📊 Outliers Analysis")
            numeric_df = df.select_dtypes(include=['number'])
            if not numeric_df.empty:
                fig = px.box(numeric_df, title="Outliers Analysis")
                st.plotly_chart(fig)
            else:
                st.warning("No numeric columns available for outliers analysis.")

        # File conversion options
        st.subheader("🔄 Conversion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel", "JSON"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_extension, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine='openpyxl')
                file_name = file.name.replace(file_extension, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            elif conversion_type == "JSON":
                df.to_json(buffer, orient='records', lines=True)
                file_name = file.name.replace(file_extension, ".json")
                mime_type = "application/json"
            buffer.seek(0)
            
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

st.success("🎉 All files processed successfully!")
st.markdown("</div>", unsafe_allow_html=True)