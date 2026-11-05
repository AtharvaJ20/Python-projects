from google import genai
from dotenv import load_dotenv
import sys

load_dotenv()
client = genai.Client()
sys.stdout.reconfigure(encoding="utf-8")

sentences = [
    "I forgot my password",
    "How do I reset my login?",
    "Best pizza places in Pune",
    "My order arrived damaged",
    "The delivery was very late",
    "Where can I eat good Italian food?",
]

def embed(texts):
    """Turn a list of texts into a list of vectors (one list of numbers per text)."""
    try:
        response = client.models.embed_content(
            model = "gemini-embedding-001",
            contents = texts,
        )
        return [e.values for e in response.embeddings]
    except Exception as e:
        print(f"Error: {e}")
        return None

def cosine_similarity(a,b):
    dot = sum(x * y for x,y in zip(a,b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    return dot/(norm_a * norm_b)

sentence_vector = embed(sentences)      # ONE call, done once, reused by every search
if sentence_vector is None:
    sys.exit("Could not embed the sentence")

def search(query):
    result = embed([query])     # [query] because embed expects a list
    if result is None:
        return []
    query_vector = result[0]

    scored = [
        (cosine_similarity(query_vector, vec), sentence)
        for sentence, vec in zip(sentences, sentence_vector)
    ]
    scored.sort(reverse=True)
    return [(score, s) for score, s in scored[:2] if score >= 0.65]

for q in ["cannot sign in", "hungry for pasta", "package was broken"]:
    print(f"\nquery: {q!r}")
    for score,sentence in search(q):
        print(f" {score:.2f}  {sentence}")




    



