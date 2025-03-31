import streamlit as st

def main():
    # Set the page configuration
    st.set_page_config(
        page_title="Landing Page",
        page_icon="🏠",
        layout="centered"
    )
    
    # Page Title
    st.title("Welcome to Georgia Tech's AI MakerSpace Chatbot")
    
    # Display an image
    st.image(
        "https://coe.gatech.edu/sites/default/files/raw-image/2024-04/Makerspace-aisle-header.jpg",
        use_container_width=True
    )
    
    # About Section
    st.write("""
        ### About the AI MakerSpace
        The AI MakerSpace at Georgia Tech is a collaborative environment where students can explore and develop innovative AI projects. Whether you're interested in machine learning, robotics, or data science, our resources and community are here to support your journey.
    """)
    
    # How to Use the Chatbot Section with Tiles
    st.write("""
        ### How to Use the Chatbot
    """)
    
    # Create three columns for the tiles
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🗨️ Ask Questions")
        st.write("Our AI assistant will provide you with detailed information about the AI MakerSpace.")
    
    with col2:
        st.markdown("#### 📚 Past Chats")
        st.write("Access your previous conversations to revisit important information or continue ongoing discussions.")
    
    with col3:
        st.markdown("#### 🔔 Stay Updated")
        st.write("Get the latest news and updates about the AI MakerSpace directly through the chatbot since it updates live.")
    
    # Get Started Section
    st.write("""
        ### Get Started
        Navigate to the **Chatbot** page using the sidebar to begin interacting with our AI assistant. If you're new, feel free to explore the information provided here or jump straight into asking questions!
    """)
    
    # Add a navigation button to the Chatbot page
    st.markdown(
        """
        <div style="text-align: center; margin-top: 30px;">
            <a href="/Chatbot" target="_self">
                <button style="
                    background-color: #4CAF50;
                    border: none;
                    color: white;
                    padding: 15px 30px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 16px;
                    border-radius: 8px;
                    cursor: pointer;
                    box-shadow: 2px 2px 12px rgba(0, 0, 0, 0.1);
                ">
                    Go to Chatbot
                </button>
            </a>
        </div>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
        main()
