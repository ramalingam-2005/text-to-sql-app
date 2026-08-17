import chromadb

from app.embeddings.embedder import generate_embedding


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="schema"
)


def retrieve_schema(question, top_k=3):

    question_embedding = generate_embedding(question)

    results = collection.query(
        query_embeddings=[
            question_embedding.tolist()
        ],
        n_results=top_k
    )

    return results


if __name__ == "__main__":

    question = "Which customers placed orders?"

    results = retrieve_schema(question)

    print("Retrieved schema:")
    print()

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        print("=" * 60)
        print("Table:", metadata["table"])
        print(document)