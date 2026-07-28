import os
import dotenv

from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

from configs.logger import get_logger

from configs.configurations import MODEL_NAME 

logger = get_logger("LLM-agent")

dotenv.load_dotenv()

class LLMAgent:
    
    def __init__(self, tools,model_name=MODEL_NAME):
        
        try:
            
            GROQ_API = os.getenv("groq_api")
            
            if not model_name:
                raise ValueError("Model name is empty")
            
            if not GROQ_API:
                raise ValueError("GROQ_API_KEY is missing from environment")
            
            
            if not tools:
                raise ValueError("tools list is missing or empty")
            
            self.llm = ChatGroq(
                model=model_name,
                temperature=0.5,
                api_key=GROQ_API,
            )
            
            
            logger.info(f"{model_name} model initiated")
            
            checkpointer = InMemorySaver()
            
            self.config = {
                "configurable": {
                    "thread_id": "conversational_id"
                }
            }
            
            self.llm_agent =  create_agent(
                model=self.llm,
                checkpointer=checkpointer,
                tools=tools,
                system_prompt="""
                            You are a useful AI agent.
                            You have access to the tools that provided.
                            Use the relevant tools if needed when answering the user questions.
                """
            )
            
            logger.info("react agent initiated")
            
        except ValueError as e:
            print(f"Value error: {e}")
            raise
            
        except Exception as e:
            print(f"Error in llm agent init: {e}")
            raise
        
    
    async def get_response(self, question):
        
        try:
          
            if not question:
                raise ValueError("question is empty")
            
            response = await self.llm_agent.ainvoke({
                "messages":[ {
                    "role": "user",
                    "content": question
                }
                            ]
            }, config=self.config)
            
            logger.info("Reponse is fetched")
            return response  
            
            
        except ValueError as e:
            print(f"Value error: {e}")
            raise
            
        except Exception as e:
            print(f"Error in get response: {e}")
            raise