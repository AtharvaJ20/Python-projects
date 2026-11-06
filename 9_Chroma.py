from google import genai
from dotenv import load_dotenv
import sys
import chromadb

load_dotenv()
sys.stdout.reconfigure(encoding="utf-8")
client = genai.Client()

db = chromadb.PersistentClient(path="chroma_db")

sentences = [
    "I forgot my password",
    "How do I reset my login?",
    "Best pizza places in Pune",
    "My order arrived damaged",
    "The delivery was very late",
    "Where can I eat good Italian food?",
]

def embed(texts):
    try:
        response = client.models.embed_content(
            model = "gemini-embedding-001",
            contents = texts,
        )
        return [e.values for e in response.embeddings]
    except Exception as e:
        print(f"Error : {e}")
        return None

# Step 3: the collection (like a table), measuring closeness with cosine
collection = db.get_or_create_collection(
    name = "support",
    metadata = {"hnsw:space":"cosine"}
)
print(collection.metadata)

# Step 4: add the sentences ONCE. On a rerun, count() is 6, so we skip this block.
if collection.count() == 0:
    vectors = embed(sentences)
    if vectors is None:
        sys.exit("Could not embed the sentences")
    collection.add(
        ids=[str(i+1) for i in range(len(sentences))],
        documents = sentences,
        embeddings = vectors,
    )
    print(f"Added {collection.count()} sentences.")
else:
    print(f"Already stored {collection.count()} sentences. No embedding needed")

# Step 5: search
def search(query,n=2):
    result = embed([query])   # list of one text -> list of one vector
    if result is None:
        return []
    res = collection.query(
        query_embeddings = result,
        n_results = n,
    )
    docs = res["documents"][0]      # [0] = results for our one query
    dists = res["distances"][0]
    return [(1-d, doc) for d,doc in zip(dists,docs)]    # distance -> similarity

# Step 6 : test
for q in ["cannot sign in", "hungry for pasta", "package was broken"]:
    print(f"Query : {q!r}")
    for score,text in search(q):
        print(f" {score:.2f} {text}")