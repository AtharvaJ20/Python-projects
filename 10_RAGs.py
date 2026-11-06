from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import chromadb

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()
client = genai.Client()
db = chromadb.PersistentClient(path="chroma_db")

facts = [
    "Refunds are accepted within 7 days of delivery.",
    "Delivery takes 3 to 5 working days in Pune.",
    "Damaged items are replaced free of charge.",
    "Support is available 10 AM to 6 PM, Monday to Saturday.",
    "Free delivery for purchase above Rs. 500",
    "Prefer online payment over cash on delivery",
    "Use credit points for discount",
    "Free coupons for referring to friends and families",
]

def embed(texts):
    try:
        response = client.models.embed_content(
            model = "gemini-embedding-001",
            contents = texts,
        )
        return [e.values for e in response.embeddings]
    except Exception as e:
        print(f"Error: {e}")
        return None

collection = db.get_or_create_collection(
    name = "shop",
    metadata={"hnsw:space":"cosine"},
)

if collection.count()==0:
    vector = embed(facts)
    if vector is None:
        sys.exit("Could not embed the facts")
    collection.add(
        ids=[str(i+1) for i in range(len(facts))],
        documents=facts,
        embeddings=vector,
    )
    print(f"Added {collection.count()} facts")
else:
    print(f"Already {collection.count()} stored")

def search(query,n=2):
    result = embed([query])
    if result is None:
        return []
    res = collection.query(query_embeddings=result,n_results=n)
    docs = res["documents"][0]
    dists = res["distances"][0]
    return [(1-d,doc) for d,doc in zip(dists,docs)]

MIN_SCORE = 0.6

def answer(question):
    hits = [(s,t) for s,t in search(question,n=3) if s>=MIN_SCORE]            #retrieve

    if not hits:
        return "I dont know. This is'nt covered in our documents"

    context = "\n".join(text for score,text in hits)

    prompt = (                                              # AUGMENT
        
        f"Context:\n{context}\n\n"
        f"Question: {question}"
    )

    try:
        response = client.models.generate_content(        #Generate
            model = "gemini-3.5-flash-lite",
            contents = prompt,
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None

while True:
    question = input("You : ")
    if question == "quit":
        break
    print("Bot:", answer(question))

