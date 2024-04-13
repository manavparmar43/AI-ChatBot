from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.pgembedding import PGEmbedding 
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from config.config_template import OPENAI_KEY,PGADMIN_URL

import time
import uuid

import tiktoken


embedding_funcation=OpenAIEmbeddings(openai_api_key=OPENAI_KEY)
# collection_name = "python_informations"


def fetch_docs_text(file_path):
    loader = PyPDFLoader(file_path)
    pages = loader.load_and_split()
    return pages


def text_spliters(file_path):
   text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
   docs = text_splitter.split_documents(fetch_docs_text(file_path))
   return docs


def create_retrieve_database(file_path,collection_id):

   try:

        db = PGEmbedding.from_documents(
            embedding=embedding_funcation,
            documents=text_spliters(file_path),
            collection_name=collection_id,
            connection_string=PGADMIN_URL,
            pre_delete_collection=False,
        )
        return db
   except Exception as e:
      print(f"Error: {e}")
      db = None
      return db



# db=create_database()








# def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613"):
    # """Return the number of tokens used by a list of messages."""
    # try:
    #     encoding = tiktoken.encoding_for_model(model)
    # except KeyError:
    #     print("Warning: model not found. Using cl100k_base encoding.")
    #     encoding = tiktoken.get_encoding("cl100k_base")
    # if model in {
    #     "gpt-3.5-turbo-0613",
    #     "gpt-3.5-turbo-16k-0613",
    #     "gpt-4-0314",
    #     "gpt-4-32k-0314",
    #     "gpt-4-0613",
    #     "gpt-4-32k-0613",
    # }:
    #     tokens_per_message = 3
    #     tokens_per_name = 1
    # elif model == "gpt-3.5-turbo-0301":
    #     tokens_per_message = (
    #         4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
    #     )
    #     tokens_per_name = -1  # if there's a name, the role is omitted
    # elif "gpt-3.5-turbo" in model:
    #     print(
    #         "Warning: gpt-3.5-turbo may update over time. Returning num tokens assuming gpt-3.5-turbo-0613."
    #     )
    #     return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0613")
    # elif "gpt-4" in model:
    #     print(
    #         "Warning: gpt-4 may update over time. Returning num tokens assuming gpt-4-0613."
    #     )
    #     return num_tokens_from_messages(messages, model="gpt-4-0613")
    # else:
    #     raise NotImplementedError(
    #         f"""num_tokens_from_messages() is not implemented for model {model}. See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
    #     )
    # num_tokens = 0
    # for message in messages:
    #     num_tokens += tokens_per_message
    #     for key, value in message.items():
    #         num_tokens += len(encoding.encode(value))
    #         if key == "name":
    #             num_tokens += tokens_per_name
    # num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    # return num_tokens



# while True:
#    if db is not None:
#       query = input("\nAsk Question: ")
#       humanprompt = HumanMessage(
#             content=augment_prompt(query)
#       )
#       messages.append(humanprompt)
#       res = chat(messages)
#       aiprompt=AIMessage(
#           content=str(res.content)
#       )
#       messages.append(aiprompt)
#       print("\nProcessing.... \n")
#       time.sleep(2)
#       print("AI: ",res.content) 
#    else:
#       create_database() 