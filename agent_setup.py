# agent_setup.py
from langchain_openai import ChatOpenAI
from langchain.agents import create_sql_agent, AgentType
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

def init_agent(db):
    """Initialize the SQL Agent with OpenAI LLM and return executor."""
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=False,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    )
    return llm, agent_executor
