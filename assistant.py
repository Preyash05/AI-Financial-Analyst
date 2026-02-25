from typing import List, Dict, Optional, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class Assistant:
    def __init__(
        self, 
        system_prompt: str, 
        llm: Any, 
        message_history: Optional[List[Dict]] = None, 
        vector_store: Optional[Any] = None, 
        employee_information: Optional[Dict] = None
    ):
        self.system_prompt = system_prompt
        self.llm = llm
        self.messages = message_history if message_history is not None else []
        self.vector_store = vector_store
        self.employee_info = employee_information
        
        self.chain = self._build_chain()

    def _build_chain(self):
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder("conversation_history"),
            ("human", "{user_input}"),
        ])

        parser = StrOutputParser()

        if self.vector_store:
            retriever = self.vector_store.as_retriever()
            return (
                {
                    "retrieved_policy_information": retriever, 
                    "employee_information": lambda _: str(self.employee_info),
                    "user_input": RunnablePassthrough(),
                    "conversation_history": lambda _: self.messages
                }
                | prompt 
                | self.llm 
                | parser
            )
        
        return (
            {
                "user_input": RunnablePassthrough(),
                "conversation_history": lambda _: self.messages
            } 
            | prompt 
            | self.llm 
            | parser
        )

    def get_response(self, user_input: str) -> str:
        return self.chain.invoke(user_input)