from retrieval.intent_router import detect_section


queries = [

    "Show me your projects",

    "What programming languages do you know?",

    "Where did you study?",

    "What is your phone number?",

    "Tell me about yourself",

    "What machine learning experience do you have?"
]

for query in queries:

    print(query)

    print("->", detect_section(query).value)

    print()