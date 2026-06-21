from search import search_engine

while True:

    query = input("\nAsk: ")

    result = search_engine.search(query)

    print("\nAnswer:")
    print(result["answer"])

    print("\nMatched:")
    print(result["matched_question"])

    print("\nConfidence:")
    print(result["confidence"])