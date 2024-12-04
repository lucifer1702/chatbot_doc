from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
import os 
import dotenv
import asyncio

dotenv.load_dotenv()

async def dataLoader(path):
  ## used to load the documents 
  pdf = PyPDFLoader(path)
  docs = pdf.load()
  return docs 

async def dataSplitter(docs):
  splitter = RecursiveCharacterTextSplitter(chunk_size = 1500, chunk_overlap = 1500)
  docs = splitter.split_documents(docs)
  return docs 

async def vectorStoreCreator(docs):
  embeddings = OpenAIEmbeddings(api_key=os.getenv('OPENAI_API_KEY'))
  vectorstore = FAISS.from_documents(documents=docs , embedding= embeddings)
  return vectorstore


'''The below code was used to check for debugging package dependancies 
pertaining to vector stores'''
# path = 'input.pdf'
# async def printfn(path):
#   docs = await dataLoader(path)
#   splitdata= await dataSplitter(docs)
#   vstore= await vectorStoreCreator(docs)
#   print(vstore)

# async def main():
#   await printfn(path)

# if __name__=="__main__":
#   asyncio.run(main())
