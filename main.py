from typing import Any, List, Mapping, Optional
from langchain.llms.base import LLM
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from langchain.document_loaders import UnstructuredFileLoader
from langchain.chains.summarize import load_summarize_chain
from langchain.chains.question_answering import load_qa_chain
from selenium.webdriver.common.by import By 
from langchain import OpenAI, PromptTemplate, LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.mapreduce import MapReduceChain
from langchain.prompts import PromptTemplate

from langchain.docstore.document import Document
import nltk
import ssl

from transformers.utils.hub import requests





class CustomLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(
        self,
        prompt: str,
        stop: Optional[List[str]] = None,
    ) -> str:
        if stop is not None:
            raise ValueError("stop kwargs are not permitted.")
        return requests.post(url='http://127.0.0.1:5000/chatgpt',json={"prompt":prompt}).json()["message"] 
    
    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """Get the identifying parameters."""
        return {"model" : "falcon-40b"}

llm = CustomLLM()


text_splitter = CharacterTextSplitter()


with open("main.txt" , "r") as f:
    state_of_the_union = f.read()

texts = text_splitter.split_text(state_of_the_union)

docs = [Document(page_content=t) for t in texts[:3]]


from langchain.chains.summarize import load_summarize_chain
chain = load_summarize_chain(llm, chain_type="map_reduce" , verbose=True)
print(chain.run(docs))
# print(llm)
# print(llm("Explain me qunatam mechains"))
# print(llm("so what is bose speakers"))

