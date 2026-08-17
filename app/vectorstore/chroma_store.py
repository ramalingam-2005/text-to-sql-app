import chromadb

from app.embeddings.embedder import embed_schema_documents


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="schema"
)


def store_schema_documents():
    documents = embed_schema_documents()

    for document in documents:
        collection.upsert(
            ids=[document["table"]],
            documents=[document["content"]],
            embeddings=[document["embedding"].tolist()],
            metadatas=[
                {
                    "table": document["table"]
                }
            ]
        )

    return len(documents)


if __name__ == "__main__":
    count = store_schema_documents()

    print(f"Stored {count} schema documents.")
    print(f"Collection count: {collection.count()}")