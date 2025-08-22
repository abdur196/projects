from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain_community.document_loaders import TextLoader

from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.memory import ConversationBufferMemory
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_core.documents import Document

import os
import re




##loading files from a folder
docs_path = "C:\\Users\\abdur\\Documents\\employee chatbot\\data"
all_files = [f for f in os.listdir(docs_path) if f.endswith(".txt")]

# Load documents
all_documents = []
for file in all_files:
    loader = TextLoader(os.path.join(docs_path, file))
    documents = loader.load()
    all_documents.extend(documents)



def clean_dashes(text):
    return re.sub(r"[–—−]", "-", text)


for doc in documents:
    doc.page_content = clean_dashes(doc.page_content)


def fix_garbled_characters(text):
   
    replacements = {
        "â€“": "-",   
        "â€”": "-",   
        "â€˜": "'",   
        "â€™": "'",   
        "â€œ": '"',  
        "â€�": '"',   
        "â€¢": "•",   
        "Â": "",     
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)
    return text


for doc in all_documents:
    doc.page_content = clean_dashes(doc.page_content)


for doc in all_documents:
    text = doc.page_content
    text = fix_garbled_characters(text)
    doc.page_content = text


# Split into chunks using RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,   # characters per chunk
    chunk_overlap=100, # overlap between chunks
)


chunked_documents = text_splitter.split_documents(all_documents)


# Create embeddings
embeddings = OllamaEmbeddings(model="mistral")


from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chains.question_answering import load_qa_chain
# Common casual responses
casual_responses = {
    "hi": "Hello! How can I help you today?",
    "hello": "Hi there! Feel free to ask anything about the company.",
    "hey": "Hey! What would you like to know?",
    "thank you": "You're welcome! Let me know if you need anything else.",
    "thanks": "Glad I could help!",
    "who are you": "I'm your HR assistant chatbot. I'm here to help with company-related questions.",
    "what can you do": "I can help you with HR policies, leave information, training, and more based on our internal documents."
}

# Create prompt
prompt_template = PromptTemplate.from_template("""
You are an HR assistant answering questions using internal company documents.

Always respond confidently and factually based on the information provided. Avoid using uncertain phrases like "appears to be" or "it seems."

If the answer is partially missing, do your best to shape a helpful response using the available context — without mentioning that you’re using context or that information is missing.

Never say "I don't know", "I'm not sure", or "I don’t have enough context." If no useful information is available, respond with: "Please contact HR for further assistance."

                    

Context:
{context}

Question: {question}
Answer:
""")

# Create vector store
vector_store = FAISS.from_documents(chunked_documents, embeddings)

# Create retriever
retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 8}
)

# Create LLM
llm = OllamaLLM(
    model="mistral",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

# Create custom QA chain using "stuff" type (which supports custom prompt easily)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    chain_type_kwargs={"prompt": prompt_template},
    return_source_documents=True
)


if __name__ == "__main__":
    while True:
        query = input("\nAsk your question (or type 'exit' to quit): ")
        if query.lower().strip() in ["exit", "quit"]:
            break

        # Normalize query
        normalized_query = query.lower().strip()

        # Casual responses
        if normalized_query in casual_responses:
            print("\n📎 Answer:")
            print(casual_responses[normalized_query])
            continue

        # Use "query" because RetrievalQA expects it
        result = qa_chain.invoke({"query": query})
        print("\n📎 Answer:")
        print(result["result"])








#memory = ConversationBufferMemory()

#conversation = ConversationChain(
    #lm=llm,
    #memory=memory,
    #verbose=False
#)

#while True:
    ## if user_input.lower() in ["exit", "quit"]:
      # break
    #print("Bot: ", end="")
    #conversation.predict(input=user_input)
