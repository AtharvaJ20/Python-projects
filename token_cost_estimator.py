import tiktoken
import sys
sys.stdout.reconfigure(encoding="utf-8")   # print using UTF-8, which supports Hindi

enc = tiktoken.get_encoding("cl100k_base")   # a real tokenizer used by OpenAI models

def count_tokens(text):
    ids = enc.encode(text)
    return len(ids)

def estimate_cost(text, price_per_million_tokens):
    tokens = count_tokens(text)
    return tokens/ 1_000_000 * price_per_million_tokens

texts = [
    "hi",
    "internationalization",
    "helllo",
    "I love Python",
    "मुझे पायथन पसंद है",
]

for text in texts:
    chars = len(text)
    tokens = count_tokens(text)
    cost = estimate_cost(text,3) # made-up price: 3 per million tokens
    print(f"{text!r:25} tokens = {tokens:2} chars = {chars:2} tokens/char = {tokens/chars:.2f} cost = {cost:.8f}")

