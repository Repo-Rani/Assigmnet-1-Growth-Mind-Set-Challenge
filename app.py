import streamlit as st
import pandas as pd
import os
from io import BytesIO
import plotly.express as px

# Configure the Streamlit app's appearance and layout
st.set_page_config(page_title="Growth Mindset DataForge Pro", layout="wide")

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
        /* Sidebar styling */
        .sidebar .sidebar-content {
            padding: 2rem 1rem;
        }
        .sidebar .sidebar-content .stMarkdown h1 {
            font-size: 1.5rem;
            margin-bottom: 1rem;
        }
        .sidebar .sidebar-content .stMarkdown h2 {
            font-size: 1.2rem;
            margin-top: 1.5rem;
            margin-bottom: 0.5rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for navigation and theme toggle
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Visualization options
    st.markdown("### 📊 Visualization Options")
    visualization_type = st.selectbox(
        "Choose Visualization Type", 
        ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Pie Chart", "Box Plot", "Heatmap"]
    )
    
    # Additional sidebar options
    st.markdown("---")
    st.markdown("### 🔧 Additional Options")
    show_summary = st.checkbox("📝 Show Data Summary")
    show_correlation = st.checkbox("📈 Show Correlation Matrix")
    show_missing_values = st.checkbox("🔍 Show Missing Values Analysis")
    show_outliers = st.checkbox("📊 Show Outliers Analysis")

# Apply the dark theme
st.markdown('<div data-theme="dark">', unsafe_allow_html=True)

# Main app title and introductory text
st.title("🚀 Growth Mindset DataForge Pro")
st.write("**Empower your learning journey with data and a growth mindset.**")

# Growth Mindset Section
st.subheader("🌱 What is a Growth Mindset?")
st.write("""
A growth mindset is the belief that your abilities and intelligence can be developed through hard work, perseverance, and learning from your mistakes. Here are some tips to help you adopt a growth mindset:
- **Embrace Challenges**: View obstacles as opportunities to learn.
- **Learn from Mistakes**: Understand that making mistakes is a natural part of learning.
- **Persist Through Difficulties**: Stay determined, even when things get tough.
- **Celebrate Effort**: Recognize and reward the effort you put into learning.
""")

# Initialize session state for reflections and goals
if "reflections" not in st.session_state:
    st.session_state.reflections = []

if "goals" not in st.session_state:
    st.session_state.goals = []

# Reflection Journal
st.subheader("📝 Reflection Journal")
reflection = st.text_area("Write about a challenge you faced, what you learned, and how you plan to improve:")
if st.button("Save Reflection"):
    if reflection:
        st.session_state.reflections.append(reflection)
        st.success("Reflection saved! Keep up the great work.")
    else:
        st.warning("Please write something before saving.")

# Display saved reflections
if st.session_state.reflections:
    st.subheader("📝 Saved Reflections")
    for i, reflection in enumerate(st.session_state.reflections, 1):
        st.write(f"{i}. {reflection}")

# Progress Tracker
st.subheader("📊 Progress Tracker")
tasks_completed = st.slider("Number of tasks completed:", 0, 10)
reflections_written = st.slider("Number of reflections written:", 0, 10)
st.write(f"**Tasks Completed:** {tasks_completed}")
st.write(f"**Reflections Written:** {reflections_written}")

# Visualize Progress
if tasks_completed > 0 or reflections_written > 0:
    progress_data = pd.DataFrame({
        "Category": ["Tasks Completed", "Reflections Written"],
        "Count": [tasks_completed, reflections_written]
    })
    fig = px.bar(progress_data, x="Category", y="Count", title="Your Progress")
    st.plotly_chart(fig)

# Learning Goals
st.subheader("🎯 Learning Goals")
goal = st.text_input("Set a learning goal (e.g., 'Learn how to clean data effectively'):")
if st.button("Add Goal"):
    if goal:
        st.session_state.goals.append(goal)
        st.success(f"Goal added: {goal}")
    else:
        st.warning("Please enter a goal before adding.")

# Display saved goals
if st.session_state.goals:
    st.subheader("🎯 Saved Goals")
    for i, goal in enumerate(st.session_state.goals, 1):
        st.write(f"{i}. {goal}")

# Data Learning Tools
st.subheader("📚 Data Learning Tools")
st.write("Use the tools below to learn data skills and apply a growth mindset to your work.")

# File uploader widget
uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

# Processing logic for uploaded files
if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()
        
        try:
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
            with st.expander("🛠️ Data Cleaning Options"):
                if st.checkbox(f"Clean Data for {file.name}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button(f"🧹 Remove Duplicates from {file.name}"):
                            df.drop_duplicates(inplace=True)
                            st.write("Duplicates Removed!")
                        if st.button(f"🗑️ Drop Columns from {file.name}"):
                            columns_to_drop = st.multiselect("Select columns to drop", df.columns)
                            df.drop(columns=columns_to_drop, inplace=True)
                            st.write(f"Dropped columns: {columns_to_drop}")
                    with col2:
                        if st.button(f"🔢 Fill Missing Values for {file.name}"):
                            numeric_cols = df.select_dtypes(include=['number']).columns
                            cols_to_fill = st.multiselect("Select numeric columns to fill", numeric_cols)
                            if cols_to_fill:
                                df[cols_to_fill] = df[cols_to_fill].fillna(df[cols_to_fill].mean())
                                st.write(f"Missing values filled for: {cols_to_fill}")
                        if st.button(f"🔤 Handle Categorical Data for {file.name}"):
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
                if visualization_type == "Pie Chart":
                    st.write("**Pie Chart requires one categorical and one numeric column.**")
                    name_col = st.selectbox("Select column for names", df.columns)
                    value_col = st.selectbox("Select column for values", numeric_cols)
                    if name_col and value_col:
                        fig = px.pie(df, names=name_col, values=value_col, title="Pie Chart")
                        st.plotly_chart(fig)
                elif visualization_type == "Heatmap":
                    if len(numeric_cols) >= 2:
                        corr = df[numeric_cols].corr()
                        fig = px.imshow(corr, text_auto=True, title="Heatmap")
                        st.plotly_chart(fig)
                    else:
                        st.warning("At least two numeric columns are required for a heatmap.")
                elif visualization_type in ["Bar Chart", "Line Chart", "Scatter Plot", "Histogram", "Box Plot"]:
                    if len(numeric_cols) >= 2:
                        if visualization_type == "Bar Chart":
                            x_axis = st.selectbox("Select X-axis", df.columns)
                            y_axis = st.selectbox("Select Y-axis", numeric_cols)
                            fig = px.bar(df, x=x_axis, y=y_axis, title="Bar Chart")
                        elif visualization_type == "Line Chart":
                            x_axis = st.selectbox("Select X-axis", df.columns)
                            y_axis = st.selectbox("Select Y-axis", numeric_cols)
                            fig = px.line(df, x=x_axis, y=y_axis, title="Line Chart")
                        elif visualization_type == "Scatter Plot":
                            x_axis = st.selectbox("Select X-axis", numeric_cols)
                            y_axis = st.selectbox("Select Y-axis", numeric_cols)
                            fig = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
                        elif visualization_type == "Histogram":
                            x_axis = st.selectbox("Select X-axis", numeric_cols)
                            fig = px.histogram(df, x=x_axis, title="Histogram")
                        elif visualization_type == "Box Plot":
                            fig = px.box(df, y=numeric_cols, title="Box Plot")
                        st.plotly_chart(fig)
                    else:
                        st.warning("At least two numeric columns are required for this visualization.")

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
                    json_format = st.selectbox("Select JSON format", ["records", "split", "index", "columns", "values"])
                    df.to_json(buffer, orient=json_format)
                    file_name = file.name.replace(file_extension, ".json")
                    mime_type = "application/json"
                buffer.seek(0)
                
                st.download_button(
                    label=f"⬇️ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

        except Exception as e:
            st.error(f"Error processing file {file.name}: {e}")

st.success("🎉 All files processed successfully!")
st.markdown("</div>", unsafe_allow_html=True)