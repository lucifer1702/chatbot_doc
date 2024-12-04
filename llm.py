## this file contains the code for the llm and the corresponding rag system development 
import asyncio
##necessary imports 
from prompts import *
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.memory import (ChatMessageHistory, ConversationBufferMemory,
                              ConversationSummaryMemory,
                              ConversationKGMemory)
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os 
import dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from ingester import vectorStoreCreator, dataLoader, dataSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain

dotenv.load_dotenv()

##necessary for tracing
os.environ['LANGCHAIN_TRACING_V2']='true'
os.environ['LANGCHAIN_API_KEY']=os.getenv('LANGCHAIN_API_KEY')
os.environ['LANGCHAIN_ENDPOINT']='https://api.smith.langchain.com'

## the llm which is about to be used 
llm = ChatOpenAI(
  model='gpt-4o',
  api_key=os.getenv('OPENAI_API_KEY'),
  temperature=0.2,
  max_tokens= 2048
)

chat_history=[]
## chatbot
async def chatbotLLM(query, path):

  chatprompt = ChatPromptTemplate.from_messages([
    ("system", question_prompt),
     ("human", "{input}")
      ])
  dloader = await dataLoader(path)
  dsplitter = await dataSplitter(dloader)
  vstore = await  vectorStoreCreator(dsplitter)

  ret_prompt = (
     "given a chat history and the latest user question, which might be in refernce to the history"
     " formulate a standalone question using the both of them, which can be understood without the chat history"
     "DO NOT ANSWER THE QUESTION JUST REFORMULATE IT INTO A CONTEXT AWARE QUESTION"
  )
  
  cont_ret_prompt= ChatPromptTemplate.from_messages([
    ("system",ret_prompt),
    ("human", "{input}")]
  )
  history_aware_chain = create_history_aware_retriever(llm, vstore.as_retriever(), cont_ret_prompt)
  qa_chain = create_stuff_documents_chain(llm, chatprompt)
  rag_chain = create_retrieval_chain(history_aware_chain, qa_chain)
  output = rag_chain.invoke({
    "input":f"{query}",
    "chat_history":chat_history
  })
  return output["answer"]
  





#debugging
# async def main():
#    path = 'input.pdf'
#    query = 'Who is the president of india'
#    output = await chatbotLLM(query, path)
#    print(output)

# if __name__=='__main__':
#    asyncio.run(main())
