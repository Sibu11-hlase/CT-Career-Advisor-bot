import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment variables from the .env file
load_dotenv()  # This will load variables from the .env file into the environment

# Retrieve the API key from the environment
api_key = os.getenv("GROQ_API_KEY")

# Ensure the API key is loaded
if not api_key:
    raise ValueError("API key not found. Please make sure the .env file contains 'GROQ_API_KEY'.")

# Create Groq client with the API key
client = Groq(api_key=api_key)

# Function to get growing industries and their growth estimates dynamically
def get_growing_industries():
    # This is a sample of dynamic data (could be fetched from an API or database)
    industries = [
        {"industry": "Technology", "growth_estimate": "5-10% annually"},
        {"industry": "Healthcare", "growth_estimate": "7-10% annually"},
        {"industry": "Renewable Energy", "growth_estimate": "8-12% annually"},
        {"industry": "E-commerce", "growth_estimate": "6-9% annually"},
        {"industry": "Finance & Fintech", "growth_estimate": "6-8% annually"},
        {"industry": "Education Technology (EdTech)", "growth_estimate": "15% annually"},
        {"industry": "Logistics & Supply Chain", "growth_estimate": "4-8% annually"},
    ]
    return industries

# Initialize the conversation history with dynamic data
industries = get_growing_industries()
industries_message = "Here are 7 growing industries along with their estimated growth:\n\n"

for idx, industry in enumerate(industries):
    industries_message += f"{idx + 1}. **{industry['industry']}** - Estimated Growth: {industry['growth_estimate']}\n"

conversation_history = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "assistant",
        "content": industries_message
    }
]

# Streamlit application
def chatbot_interface():
    """
    Streamlit interface for the chatbot.
    """
    st.set_page_config(page_title="Career Advisor ChatBot", layout="wide")

    # Set title with color
    st.markdown("<h1 style='color: #4CAF50;'>Career Path Adviser ChatBot</h1>", unsafe_allow_html=True)

    # Set description with dynamic content (growing industries)
    industries_description = "<p style='color: #3f51b5; font-size: 18px;'>Welcome to the Career Adviser ChatBot! Ask me anything about career paths, job recommendations, or industry trends. Type your queries below🫡.</p>"

    # Add growing industries dynamically in cards
    st.markdown(industries_description, unsafe_allow_html=True)

    # Add custom CSS for uniform card sizes
    st.markdown(
        """
        <style>
        .industry-card {
            border: 1px solid #ddd;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            height: 250px; /* Fixed height for all cards */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #f9f9f9;
        }
        .industry-card h3 {
            margin-bottom: 10px;
            font-size: 18px;
        }
        .industry-card p {
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Create a card layout for each industry with fixed height and width
    col1, col2, col3 = st.columns(3)
    with col1:
        for idx, industry in enumerate(industries[:3]):  # First three industries
            st.markdown(
                f"""
                <div class='industry-card'>
                    <h3>{industry['industry']}</h3>
                    <p><strong>Growth Estimate:</strong> {industry['growth_estimate']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col2:
        for idx, industry in enumerate(industries[3:5]):  # Next two industries
            st.markdown(
                f"""
                <div class='industry-card'>
                    <h3>{industry['industry']}</h3>
                    <p><strong>Growth Estimate:</strong> {industry['growth_estimate']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    with col3:
        for idx, industry in enumerate(industries[5:]):  # Last two industries
            st.markdown(
                f"""
                <div class='industry-card'>
                    <h3>{industry['industry']}</h3>
                    <p><strong>Growth Estimate:</strong> {industry['growth_estimate']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

    # Initialize session state for context and messages
    if "conversation_history" not in st.session_state:
        # Initialize with initial assistant message
        st.session_state.conversation_history = conversation_history.copy()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "sidebar_visible" not in st.session_state:
        st.session_state.sidebar_visible = True

    # Sidebar toggler
    with st.sidebar:
        # Dynamic sidebar content
        if st.session_state.sidebar_visible:
            with st.sidebar:
                # Apply custom styles for icons and hover effect
                st.markdown(
            """
            <style>
            /* Change the sidebar background color */
            [data-testid="stSidebar"] {
                background-color: #6C63FF; /* Light purple */
            }
            .nav-item {
                font-size: 16px;
                margin: 10px 0;
                display: flex;
                align-items: center;
            }
            .nav-item a {
                text-decoration: none;
                color: black;
                display: flex;
                align-items: center;
                padding: 5px 10px;
                border-radius: 5px;
            }
            .nav-item a:hover {
                background-color: #9C29B0;
            }
            .nav-item i {
                margin-right: 10px;
                font-size: 18px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        # Navigation header
        st.header("llama-3.3-70b-versatile")

        # Navigation items with icons and links
        st.markdown(
            """
            <div class="nav-item">
               <i>🏠</i> <a href="/app" target="_self">Home</a>
            </div>
            
            """,
            unsafe_allow_html=True,
        )

    # Display chat history (including initial assistant message)
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input field
    if user_input := st.chat_input("Type your message here..."):
        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Add user input to conversation history
        st.session_state.conversation_history.append({"role": "user", "content": user_input})

        # Create chat completion with the conversation history
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=st.session_state.conversation_history,
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=True,
            stop=None
        )

        # Collect the chunks and combine them into a single response
        assistant_reply = ""
        for chunk in completion:
            assistant_reply += chunk.choices[0].delta.content or ""

        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": assistant_reply})
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        with st.chat_message("assistant"):
            st.markdown(assistant_reply)

# Run the chatbot interface
if __name__ == "__main__":
    chatbot_interface()
