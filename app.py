import streamlit as st
import google.generativeai as genai
import datetime
import random
import pandas as pd
from io import BytesIO
import time
import re  
import os
from dotenv import load_dotenv
load_dotenv()

# Set page config at the top of the script
st.set_page_config(
    page_title="Growth Mindset App",
    page_icon="🌱",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Configure Gemini AI
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY")) 
    model = genai.GenerativeModel("gemini-2.0-flash")
except Exception as e:
    print(f"Error configuring Gemini AI: {str(e)}")

# Function to chat with Gemini
def chat_with_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to validate email
def validate_email(email):
    # Regex pattern for a valid email
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

# Light Theme and Text Color Adjustments
st.markdown("""
    <style>
    /* Main background and text color */
    .main {
        background-color: #FFFFFF;  /* Light background */
        color: #333333;  /* Dark grey text */
        padding: 20px;
        border-radius: 10px;
    }
    /* Headings color */
    h1, h2, h3 {
        color: #1565C0;  /* Blue for headings */
    }
    /* Button styling */
    .stButton>button {
        background-color: #FF0000;  /* Red button */
        color: white;  /* White text */
        border-radius: 10px;  /* Rounded corners */
        padding: 12px 24px;  /* Larger padding */
        border: none;  /* No border */
        font-size: 16px;  /* Larger font size */
        font-weight: bold;  /* Bold text */
        transition: background-color 0.3s ease, color 0.3s ease;  /* Smooth hover effect */
    }
    /* Button hover effect */
    .stButton>button:hover {
        background-color: white;  /* White background on hover */
        color: #FF0000;  /* Red text on hover */
    }
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background-color: #F5F5F5;  /* Light grey sidebar */
        color: #333333;  /* Dark grey text */
    }
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 10px;
        font-size: 0.9em;
        color: #666666;  /* Grey text */
    }
    </style>
    """, unsafe_allow_html=True)

# Motivational Quotes Function
def get_motivation():
    motivations = [
        "Believe you can and you're halfway there. - Theodore Roosevelt",
        "The only limit to our realization of tomorrow is our doubts of today. - Franklin D. Roosevelt",
        "It always seems impossible until it's done. - Nelson Mandela",
        "Success is not final, failure is not fatal: It is the courage to continue that counts. - Winston Churchill",
        "The only way to do great work is to love what you do. - Steve Jobs"
    ]
    return random.choice(motivations)

# Task Manager App
def task_manager_app():
    st.title("✅ Task Manager")
    st.write("Organize your tasks and stay productive! 🚀")

    task = st.text_input("📝 Add a new task:")
    priority = st.selectbox("🔝 Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("📅 Due Date", datetime.date.today())
    category = st.selectbox("📂 Category", ["Work", "Personal", "Study", "Other"])

    if st.button("Add Task"):
        if task:
            if 'tasks' not in st.session_state:
                st.session_state.tasks = []
            st.session_state.tasks.append({
                "task": task,
                "priority": priority,
                "due_date": due_date,
                "category": category,
                "completed": False
            })
            st.success("Task added successfully!  ")
        else:
            st.warning("Please enter a task!")

    if 'tasks' in st.session_state and st.session_state.tasks:
        st.subheader("📋 Your Tasks:")
        for i, task in enumerate(st.session_state.tasks, 1):
            st.write(f"{i}. {task['task']} - Priority: {task['priority']} - Due: {task['due_date']} - Category: {task['category']}")
            if st.button(f"Complete Task {i}"):
                st.session_state.tasks[i-1]['completed'] = True
                st.success("Task marked as completed! 🎉")
            if st.button(f"Delete Task {i}"):
                st.session_state.tasks.pop(i-1)
                st.success("Task deleted successfully! 🗑")
    else:
        st.info("No tasks added yet. Add some tasks to get started! 🌟")

# Growth Mindset App
def growth_mindset_app():
    st.title("🌱 Growth Mindset Challenge")

    st.header("Welcome to the Growth Mindset Challenge!  ")
    st.write(
        "A growth mindset is the belief that abilities can be developed through dedication and hard work. "
        "This web app is designed to help you track your progress, stay motivated, and cultivate a positive learning attitude. "
        "Remember, every challenge is an opportunity for growth! 🌟"
    )

    st.subheader("📅 Daily Reflection")
    date = st.date_input("Select Date", datetime.date.today())
    reflection = st.text_area("📝 What did you learn today?")
    challenges = st.text_area("💡 What challenges did you face, and how did you overcome them?")
    next_goal = st.text_area("🎯 What is your next goal for improvement?")

    if st.button("✅ Submit Reflection"):
        st.success("Reflection Saved! Keep Growing! 🚀")

    st.header("💡 Growth Mindset Tips")
    st.write("✔ Embrace challenges as learning opportunities. 💪")
    st.write("✔ Learn from mistakes instead of fearing them. 🔄")
    st.write("✔ Celebrate effort and progress over perfection. 🎉")
    st.write("✔ Stay positive and keep pushing forward! 😊")
    st.write("✔ Seek feedback and use it as a tool for improvement. 🔧")
    st.write("✔ Visualize success and take small steps toward your goals. 🌈")
    st.write("✔ Surround yourself with positive and supportive people. 🤝")
    st.write("✔ Practice gratitude to stay motivated and focused. 🙏")

    if st.button("💖 Get Inspired"):
        st.success(get_motivation())

    st.header("📌 Track Your Progress")
    st.write("🗂 Keep a journal of your reflections and review your progress over time!")
    st.write("📊 Set weekly or monthly growth goals to measure your improvement.")
    st.write("🔄 Stay consistent and celebrate small wins!")

    progress = st.slider("📈 How motivated do you feel today?", 0, 100, 50)
    if progress >= 75:
        st.success("🔥 Amazing! Keep up the great work!")
    elif progress >= 50:
        st.info("💪 You're doing great! Keep pushing forward!")
    else:
        st.warning("🌟 Keep going! Every small effort matters!")

    st.header("🎯 Weekly Goal Setting")
    weekly_goal = st.text_area("What is your goal for this week?")
    if st.button("Set Weekly Goal"):
        st.success("Weekly goal set! Let's achieve it together! 🚀")

    st.header("📅 Monthly Reflection")
    monthly_reflection = st.text_area("Reflect on your progress this month. What went well? What could be improved?")
    if st.button("Submit Monthly Reflection"):
        st.success("Monthly reflection saved! Keep growing! 🌱")

    st.header("🙏 Gratitude Journal")
    gratitude_entry = st.text_area("What are you grateful for today?")
    if st.button("Submit Gratitude Entry"):
        st.success("Gratitude entry saved! Practicing gratitude boosts positivity! 🌟")

    st.header("📚 Resources for Growth")
    st.write("Here are some resources to help you on your growth journey:")
    st.write("- Books: 'Mindset' by Carol Dweck, 'Atomic Habits' by James Clear")
    st.write("- Podcasts: 'The Growth Mindset Podcast', 'The Tim Ferriss Show'")
    st.write("- Videos: TED Talks on growth mindset and personal development")
    st.write("- Courses: Online courses on Coursera, Udemy, or LinkedIn Learning")

    st.header("🤝 Join the Community")
    st.write("Connect with like-minded individuals and share your growth journey!")
    st.write("- Forums: Reddit communities like r/GetMotivated, r/PersonalDevelopment")
    st.write("- Social Media: Follow hashtags like #GrowthMindset, #PersonalGrowth")
    st.write("- Local Meetups: Join local groups focused on self-improvement and growth")

    st.write("---")
    st.write("Built with ❤ by Areesha Abdul Sattar | Stay motivated and keep growing! 🌱")
    st.write("📧 Contact: areesha21314@gmail.com")

# Data Sweeper App
def data_sweeper_app():
    st.title("📊 Data Sweeper")
    st.write("✨ Transform your files between CSV and Excel formats with built-in data cleaning and visualization  📈")

    uploaded_files = st.file_uploader("📂 Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

    if uploaded_files:
        for file in uploaded_files:
            file_ext = os.path.splitext(file.name)[-1].lower()

            if file_ext == ".csv":
                df = pd.read_csv(file)
            elif file_ext == ".xlsx":
                df = pd.read_excel(file)
            else:
                st.error(f"❌ Unsupported file type: {file_ext}")
                continue  

            st.write(f"📄 File Name: {file.name}")
            st.write(f"📏 File Size: {file.size / 1024:.2f} KB")

            st.write("👀 Preview the Head of the Dataframe")
            st.dataframe(df.head())

            st.subheader("🧹 Data Cleaning Options")
            if st.checkbox(f"🧽 Clean Data for {file.name}"):
                col1, col2 = st.columns(2)

                with col1:
                    if st.button(f"🚫 Remove Duplicates from {file.name}"):
                        df.drop_duplicates(inplace=True)
                        st.write("✅ Duplicates Removed!")

                with col2:
                    if st.button(f"🪣 Fill Missing Values for {file.name}"):
                        numeric_cols = df.select_dtypes(include=["number"]).columns
                        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                        st.write("✅ Missing Values have been Filled!")
              
            st.subheader("🔍 Select Columns to Convert")
            columns = st.multiselect(f"📌 Choose Columns for {file.name}", df.columns, default=df.columns)
            df = df[columns]

            st.subheader("📊 Data Visualization")
            if st.checkbox(f"📈 Show visualization for {file.name}"):
                numeric_data = df.select_dtypes(include="number")
                st.write("📊 Numeric Data Preview:", numeric_data)

                if not numeric_data.empty and numeric_data.shape[1] >= 1:
                    st.bar_chart(numeric_data)
                else:
                    st.warning(f"⚠ No numeric columns found in {file.name} for visualization!")

            st.subheader("🔄 Conversion Options")
            conversion_type = st.radio(f"🔧 Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
            if st.button(f"🔃 Convert {file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

                buffer.seek(0)
                st.download_button(
                    label=f"⬇ Download {file.name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )

    st.success("🎉 All files processed!")

# Quizzes App
def quizzes_app():
    st.title("🧠 Quizzes")
    st.write("Test your knowledge and learn something new!")

    if 'quizzes' not in st.session_state:
        st.session_state.quizzes = {
            "General": [
                {
                    "question": "What is the capital of France? 🇫🇷",
                    "options": ["Paris", "London", "Berlin", "Madrid"],
                    "answer": "Paris"
                },
                {
                    "question": "Which planet is known as the Red Planet? 🪐",
                    "options": ["Earth", "Mars", "Jupiter", "Saturn"],
                    "answer": "Mars"
                },
                {
                    "question": "Who wrote 'To Kill a Mockingbird'? 📚",
                    "options": ["Harper Lee", "Mark Twain", "J.K. Rowling", "Stephen King"],
                    "answer": "Harper Lee"
                }
            ],
            "Software Engineer": [
                {
                    "question": "What does HTML stand for? 🌐",
                    "options": ["Hyper Text Markup Language", "High-Level Text Machine Language", "Hyperlink and Text Markup Language", "Home Tool Markup Language"],
                    "answer": "Hyper Text Markup Language"
                },
                {
                    "question": "Which language is used for Android development? 📱",
                    "options": ["Java", "Python", "Swift", "C#"],
                    "answer": "Java"
                },
                {
                    "question": "What is the main use of Docker? 🐳",
                    "options": ["Virtualization", "Containerization", "Networking", "Data Storage"],
                    "answer": "Containerization"
                }
            ],
            "Doctor": [
                {
                    "question": "What is the largest organ in the human body? 🩺",
                    "options": ["Heart", "Skin", "Liver", "Brain"],
                    "answer": "Skin"
                },
                {
                    "question": "Which vitamin is produced by the human body when exposed to sunlight? ☀",
                    "options": ["Vitamin A", "Vitamin C", "Vitamin D", "Vitamin E"],
                    "answer": "Vitamin D"
                },
                {
                    "question": "What is the normal resting heart rate for adults? 💓",
                    "options": ["60-100 bpm", "40-60 bpm", "100-120 bpm", "120-140 bpm"],
                    "answer": "60-100 bpm"
                }
            ]
        }

    if 'current_quiz' not in st.session_state:
        st.session_state.current_quiz = 0

    quiz_category = "General"
    quizzes = st.session_state.quizzes[quiz_category]

    if st.session_state.current_quiz < len(quizzes):
        quiz = quizzes[st.session_state.current_quiz]
        st.subheader(f"Question {st.session_state.current_quiz + 1}")
        st.write(quiz["question"])
        user_answer = st.radio("Options", quiz["options"])
        if st.button("Submit Answer"):
            if user_answer == quiz["answer"]:
                st.success("Correct! 🎉")
            else:
                st.error(f"Wrong! The correct answer is {quiz['answer']}.")
            st.session_state.current_quiz += 1
    else:
        st.success("You have completed all the quizzes! 🎉")
        if st.button("Restart Quizzes"):
            st.session_state.current_quiz = 0

# Profile App with Proper Email Validation
def profile_app():
    st.title("👤 Profile")
    st.write("Update your profile information.")

    if 'name' not in st.session_state:
        st.session_state.name = ""
    if 'email' not in st.session_state:
        st.session_state.email = ""
    if 'profile_image' not in st.session_state:
        st.session_state.profile_image = None

    name = st.text_input("Name", st.session_state.name)
    email = st.text_input("Email", st.session_state.email)
    profile_image = st.file_uploader("Upload Profile Image", type=["jpg", "jpeg", "png"])

    if st.button("Update Profile"):
        if not name:
            st.warning("Please enter your name.")
        elif not email:
            st.warning("Please enter your email.")
        elif not validate_email(email):  # Validate email format
            st.warning("Please enter a valid email address (e.g., example@domain.com).")
        else:
            st.session_state.name = name
            st.session_state.email = email
            if profile_image is not None:
                st.session_state.profile_image = profile_image
            st.success("Profile updated successfully! 🎉")

    if st.session_state.profile_image is not None:
        st.image(st.session_state.profile_image, caption="Your Profile Image", width=150)

# Settings App
def settings_app():
    st.title("⚙ Settings")
    st.write("Customize your app settings.")

    theme = st.selectbox("Theme", ["Light"])
    notifications = st.checkbox("Enable Notifications", True)

    if st.button("Save Settings"):
        st.success("Settings saved successfully! 🎉")

# Chatbot App
def chatbot_app():
    st.title("🤖 Chatbot")
    st.write("Chat with our AI-powered chatbot in real-time!")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.chat_input("You: ")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f"*You:* {user_input}")

        with st.spinner("Thinking..."):
            bot_response = chat_with_gemini(user_input)

        st.session_state.chat_history.append({"role": "assistant", "content": bot_response})
        with st.chat_message("assistant"):
            st.markdown(f"*Assistant:* {bot_response}")

    if st.session_state.chat_history:
        st.subheader("Chat History:")
        for message in st.session_state.chat_history:
            with st.chat_message(message["role"]):
                st.markdown(f"{message['role'].capitalize()}:** {message['content']}")

# Dashboard App
def dashboard_app():
    st.title("📊 Dashboard")
    st.write("Track your progress and activity!")

    if 'tasks' in st.session_state:
        completed_tasks = sum(1 for task in st.session_state.tasks if task['completed'])
        total_tasks = len(st.session_state.tasks)
        st.write(f"✅ Completed Tasks: {completed_tasks}/{total_tasks}")

    if 'quizzes' in st.session_state:
        st.write(f"🧠 Quizzes Taken: {st.session_state.current_quiz}")

    if 'files_processed' not in st.session_state:
        st.session_state.files_processed = 0
    st.write(f"📂 Files Processed: {st.session_state.files_processed}")

    st.subheader("📈 Activity Over Time")
    activity_data = pd.DataFrame({
        "Date": [datetime.date.today() - datetime.timedelta(days=i) for i in range(7)],
        "Tasks Completed": [random.randint(1, 5) for _ in range(7)],
        "Quizzes Taken": [random.randint(1, 3) for _ in range(7)]
    })
    st.line_chart(activity_data.set_index("Date"))

# Pomodoro Timer App
def pomodoro_timer_app():
    st.title("⏳ Pomodoro Timer")
    st.write("Stay focused and productive with the Pomodoro technique!")

    work_time = st.number_input("Work Time (minutes):", min_value=1, value=25)
    break_time = st.number_input("Break Time (minutes):", min_value=1, value=5)

    if st.button("Start Timer"):
        with st.empty():
            for _ in range(work_time * 60):
                st.write(f"⏳ Working... {work_time}:{_ % 60:02}")
                time.sleep(1)
            st.success("Time for a break! 🎉")
            for _ in range(break_time * 60):
                st.write(f"☕ Break Time... {break_time}:{_ % 60:02}")
                time.sleep(1)
            st.success("Break over! Back to work! 💪")

# Habit Tracker App
def habit_tracker_app():
    st.title("📅 Habit Tracker")
    st.write("Track your daily habits and build a better routine!")

    if 'habits' not in st.session_state:
        st.session_state.habits = {}

    habit = st.text_input("Add a new habit:")
    if st.button("Add Habit"):
        if habit:
            st.session_state.habits[habit] = []
            st.success(f"Habit '{habit}' added!")

    for habit, dates in st.session_state.habits.items():
        st.subheader(habit)
        if st.checkbox(f"Mark {habit} as completed today"):
            if datetime.date.today() not in dates:
                dates.append(datetime.date.today())
                st.success(f"{habit} marked as completed for today! 🎉")
        st.write(f"Completed on: {', '.join(map(str, dates))}")

# Daily Journal App
def daily_journal_app():
    st.title("📔 Daily Journal")
    st.write("Write about your day and reflect on your thoughts.")

    journal_entry = st.text_area("Write your journal entry here:")
    if st.button("Save Entry"):
        if 'journal_entries' not in st.session_state:
            st.session_state.journal_entries = []
        st.session_state.journal_entries.append({
            "date": datetime.date.today(),
            "entry": journal_entry
        })
        st.success("Journal entry saved! 🎉")

    if 'journal_entries' in st.session_state:
        st.subheader("Past Entries")
        for entry in st.session_state.journal_entries:
            st.write(f"📅 {entry['date']}: {entry['entry']}")

# Goal Tracker App
def goal_tracker_app():
    st.title("🎯 Goal Tracker")
    st.write("Set and track your long-term goals!")

    if 'goals' not in st.session_state:
        st.session_state.goals = []

    goal = st.text_input("Add a new goal:")
    deadline = st.date_input("Deadline:", datetime.date.today())
    if st.button("Add Goal"):
        if goal:
            st.session_state.goals.append({
                "goal": goal,
                "deadline": deadline,
                "completed": False
            })
            st.success(f"Goal '{goal}' added!")

    for i, goal in enumerate(st.session_state.goals, 1):
        st.write(f"{i}. {goal['goal']} - Deadline: {goal['deadline']}")
        if st.button(f"Mark as Completed {i}"):
            st.session_state.goals[i-1]['completed'] = True
            st.success(f"Goal '{goal['goal']}' marked as completed! 🎉")

# Random Fact Generator App
def random_fact_generator_app():
    st.title("🤔 Random Fact Generator")
    st.write("Learn something new every day!")

    if st.button("Generate a Random Fact"):
        facts = [
            "Honey never spoils. Archaeologists have found pots of honey in ancient Egyptian tombs that are over 3,000 years old and still edible!",
            "Octopuses have three hearts. Two pump blood to the gills, and one pumps it to the rest of the body.",
            "Bananas are berries, but strawberries aren't."
        ]
        st.info(random.choice(facts))

# Feedback Form App
def feedback_form_app():
    st.title("📝 Feedback Form")
    st.write("We'd love to hear your feedback!")

    feedback = st.text_area("Share your thoughts:")
    rating = st.slider("Rate your experience (1-5):", 1, 5, 3)
    if st.button("Submit Feedback"):
        st.success("Thank you for your feedback! 🎉")

# Main Function
def main():
    # Sidebar for Navigation
    st.sidebar.title("🌱 Navigation")
    app_choice = st.sidebar.radio(
        "Choose an App:", 
        [
            "📊 Data Sweeper", 
            "✅ Task Manager", 
            "🤖 Chatbot", 
            "🌱 Growth Mindset Challenge", 
            "🧠 Quizzes", 
            "👤 Profile", 
            "⚙ Settings", 
            "📊 Dashboard", 
            "⏳ Pomodoro Timer", 
            "📅 Habit Tracker", 
            "📔 Daily Journal", 
            "🎯 Goal Tracker", 
            "🤔 Random Fact Generator", 
            "📝 Feedback Form"
        ]
    )

    # Display Welcome Message if no app is selected
    if app_choice is None:
        st.title("🌟 Welcome to the Growth Mindset App! 🌟")
        st.write("""
            **🚀 Get ready to embark on a journey of self-improvement and productivity!**

            This app is designed to help you:
            - **Organize your tasks** with the Task Manager.
            - **Reflect and grow** with the Growth Mindset Challenge.
            - **Test your knowledge** with interactive quizzes.
            - **Stay focused** with the Pomodoro Timer.
            - **Track your habits** and build a better routine.
            - **Set and achieve your goals** with the Goal Tracker.
            - **Chat with an AI-powered chatbot** for real-time assistance.
            - **Clean and visualize your data** with the Data Sweeper.
            - **And much more!**

            **👉 Select an app from the sidebar to get started!**
        """)
        st.image("https://via.placeholder.com/800x400.png?text=Welcome+UI+Placeholder", use_column_width=True)
    else:
        # Display the selected app
        if app_choice == "📊 Data Sweeper":
            data_sweeper_app()
        elif app_choice == "✅ Task Manager":
            task_manager_app()
        elif app_choice == "🤖 Chatbot":
            chatbot_app()
        elif app_choice == "🌱 Growth Mindset Challenge":
            growth_mindset_app()
        elif app_choice == "🧠 Quizzes":
            quizzes_app()
        elif app_choice == "👤 Profile":
            profile_app()
        elif app_choice == "⚙ Settings":
            settings_app()
        elif app_choice == "📊 Dashboard":
            dashboard_app()
        elif app_choice == "⏳ Pomodoro Timer":
            pomodoro_timer_app()
        elif app_choice == "📅 Habit Tracker":
            habit_tracker_app()
        elif app_choice == "📔 Daily Journal":
            daily_journal_app()
        elif app_choice == "🎯 Goal Tracker":
            goal_tracker_app()
        elif app_choice == "🤔 Random Fact Generator":
            random_fact_generator_app()
        elif app_choice == "📝 Feedback Form":
            feedback_form_app()

if __name__ == "__main__":
    main()