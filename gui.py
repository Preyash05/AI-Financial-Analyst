import streamlit as st

class AssistantGUI:
    def __init__(self, assistant):
        self.assistant = assistant
        
        if "messages" not in st.session_state:
            st.session_state.messages = []
            
        self.messages = st.session_state.messages

    def render_messages(self):
        for message in self.messages:
            role = message["role"]
            content = message["content"]
            
            with st.chat_message(role):
                st.markdown(content)

    def render_user_input(self):
        user_input = st.chat_input("Type your question here...")
        
        if user_input:
            with st.chat_message("user"):
                st.markdown(user_input)
            
            self.messages.append({"role": "user", "content": user_input})
            
            with st.spinner("Thinking..."):
                response = self.assistant.get_response(user_input)
            
            with st.chat_message("ai"):
                st.markdown(response)
            
            self.messages.append({"role": "ai", "content": response})
            st.session_state.messages = self.messages

    def render(self):
        self.render_messages()
        self.render_user_input()