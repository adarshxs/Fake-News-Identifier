from newsapi import NewsApiClient
from langchain import PromptTemplate
from langchain.llms import OpenAI
import openai
import os
from dotenv import load_dotenv
from urllib.request import urlopen
import json

load_dotenv()

openai_api_key = os.getenv("api_key")

llm = OpenAI(temperature=0.9)

api = NewsApiClient(api_key='09341d67f5a041f29391e40faa88d9a6')



target1 = "Stunned that the CentralGovernment requires linking of Aadhar & PAN card and charges ₹1000 for it! If the government requires linking any official documents, it should be done free of cost, not by adding to the heavy burdens of the already squeezed middle-class."

template = """
    You are given below a target (news article/tweet):\n{target}\nUsing this, generate a query parameter to be passed into 
    an API url to fetch news related to the target.\nYou should build the query that is as short as possible, while still getting the necessary information to answer the question.
    query should be of format: keyword1+keyword2+keyword3. only 3 most important keywords!
"""

prompt = PromptTemplate(
    input_variables=["target"],
    template=template,
)
query = llm(prompt.format(target=target1)).strip('", \n')


print(query)

all_articles = api.get_everything(q=query)


#print(all_articles)

url = f"https://newsapi.org/v2/everything?q={query}&totalResults=20&apiKey=09341d67f5a041f29391e40faa88d9a6"

print(url)

response = urlopen(url)

data_json = json.loads(response.read())
  
#print(data_json)
# print the json response


for article in all_articles['articles']:
    content = article['content']
    description = article['description']

print(description)

#print(reference)

