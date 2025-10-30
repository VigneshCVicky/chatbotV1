import streamlit as st
import google.generativeai as genai

st.title("My Gemini Chatbot 🤖")

# --- Configure the API key (SAFE METHOD) ---
try:
    genai.configure(api_key="")
except KeyError:
    st.error("Gemini API key not found. Please add it to your .streamlit/secrets.toml file.")
    st.stop()
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()

# --- Initialize the Model and Chat ---
if "model" not in st.session_state:
    # Use a current, valid model name
    st.session_state.model = genai.GenerativeModel('gemini-2.5-flash') 

if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.model.start_chat(history=[])

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display Chat History ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- Handle New User Input ---
if prompt := st.chat_input("What is up?"):
    
    # 1. Add and display the user's message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Send prompt to Gemini and get a streaming response
    try:
        with st.chat_message("assistant"):
            # This placeholder will be updated as the stream comes in
            message_placeholder = st.empty()
            full_response = ""
            
            # Get the streaming response
            response_stream = st.session_state.chat.send_message(prompt, stream=True)
            
            # Iterate over the stream and build the full response
            for chunk in response_stream:
                # Check if the chunk has text content
                # (Some chunks might be empty or have other data)
                if part := chunk.parts:
                    full_response += part[0].text
                    # Update the placeholder with the new text + typing cursor
                    message_placeholder.markdown(full_response + "▌")
            
            # Display the final response without the cursor
            message_placeholder.markdown(full_response)
        
        # 3. Add the *string* of the full AI response to history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.session_state.messages.pop()
