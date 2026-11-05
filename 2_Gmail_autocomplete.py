"""
Goal: Build a tiny "Gmail autocomplete" that learns from examples
Time: ~15 minutes
Constraint: Only use lists, dictionaries, loops, and functions

Story: You give the program a few example sentences. It learns
which word usually follows which word, then guesses the next word. 
"""

sentences = [
    "thanks for email",
    "thanks for help",
    "thanks for time",
    "looking for to your reply"
]

def learn(sentences):
    follows={}

    for sentence in sentences:
        words = sentence.split()

        for i in range(len(words)-1):
            current = words[i]
            nxt = words[i+1]

            if current not in follows:
                follows[current]=[]

            follows[current].append(nxt)

    return follows

def predict_next(follows, word):
    if word not in follows:
        return "I don't know"

    candidates = follows[word]
    return max(candidates, key=candidates.count)

follows = learn(sentences)
print(predict_next(follows,"your"))