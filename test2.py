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
        {"industry": "Technology", "growth_estimate": "5-10% annually", "icon": "💻"},
        {"industry": "Healthcare", "growth_estimate": "7-10% annually", "icon": "🏥"},
        {"industry": "Renewable Energy", "growth_estimate": "8-12% annually", "icon": "🌱"},
        {"industry": "E-commerce", "growth_estimate": "6-9% annually", "icon": "🛒"},
        {"industry": "Finance & Fintech", "growth_estimate": "6-8% annually", "icon": "💰"},
        {"industry": "Education Technology (EdTech)", "growth_estimate": "15% annually", "icon": "🎓"},
        {"industry": "Logistics & Supply Chain", "growth_estimate": "4-8% annually", "icon": "🚚"},
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

    # Set title with color and center alignment
    st.markdown("<h1 style='color: #D8BFD8; text-align: center;'>Career Path Adviser ChatBot</h1>", unsafe_allow_html=True)

    # Set description with dynamic content (growing industries) and center alignment
    industries_description = "<p style='color: #3f51b5; font-size: 18px; text-align: center;'>Welcome to the Career Adviser ChatBot! Ask me anything about career paths, job recommendations, or industry trends. Type your queries below🫡.</p>"

    # Add growing industries dynamically in cards
    st.markdown(industries_description, unsafe_allow_html=True)

    # Add custom CSS for uniform card sizes
    st.markdown(
        """
        <style>
        .industry-card {
            border: 1px solid #B57EDC;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            height: 200px; /* Fixed height for all cards */
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            background-color: #f9fafb;
        }
        .industry-card h3 {
            margin-bottom: 10px;
            font-size: 18px;
        }
        .industry-card p {
            font-size: 14px;
        }
        .industry-card .icon {
            font-size: 30px; /* Icon size */
            margin-bottom: 10px;
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
                    <div class='icon'>{industry['icon']}</div>
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
                    <div class='icon'>{industry['icon']}</div>
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
                    <div class='icon'>{industry['icon']}</div>
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
            # Apply custom styles for sidebar and nav items
            st.markdown(
                """
                <style>
                /* Change the sidebar background color */
                [data-testid="stSidebar"] {
                    background-color: #f9fafb; /* Light purple */
                    padding-top: 0;  /* Remove any padding at the top */
                }

                /* Make the nav items align to the top left */
                .nav-item {
                    font-size: 16px;
                    margin: 5px 0;  /* Adjusted margins to ensure spacing */
                    display: flex;
                    align-items: center;
                    justify-content: flex-start;  /* Align items to the left */
                }

                /* Style for the link */
                .nav-item a {
                    text-decoration: none;
                    color: black;
                    display: flex;
                    align-items: center;
                    padding: 5px 10px;
                    border-radius: 5px;
                    width: 100%;  /* Ensure the item takes the full width of the sidebar */
                }

                /* Hover effect */
                .nav-item a:hover {
                    background-color: #9C29B0;
                }

                /* Icon styling */
                .nav-item i {
                    margin-right: 10px;  /* Space between icon and text */
                    font-size: 18px;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )
        
        # Navigation header
        #st.header("llama-3.3-70b-versatile")

        # Add Font Awesome CDN for icons and custom CSS for the spinning effect and positioning
        st.markdown(
            """
            <style>
            /* Add Font Awesome CDN */
            @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css');

            /* Define the spin animation */
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }

            /* Make the Exit link appear at the top left of the sidebar */
            .nav-item {
                display: flex;
                align-items: center;
                margin-bottom: 20px; /* Optional: space between items */
                padding-left: 10px;
            }

            /* Exit link style */
            .nav-item a {
                text-decoration: none;
                color: #B57EDC;
                display: flex;
                align-items: center;
                font-size: 18px;
            }

            /* Icon style */
            .nav-item i {
                margin-right: 10px;
                font-size: 20px; /* Adjust the size of the icon */
            }

            /* Apply spin effect on hover */
            .nav-item a:hover i {
                animation: spin 1s linear infinite;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # Navigation item with the exit icon that spins on hover
        st.sidebar.markdown(
            """
            <div class="nav-item">
                <a href="https://career-chat-ai.vercel.app" target="_self">
                    <i class="fas fa-sign-out-alt"></i> Exit
                </a>
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
