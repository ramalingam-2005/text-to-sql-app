from sentence_transformers import SentenceTransformer

from app.schema.formatter import build_schema_documents


model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):
    return model.encode(text)


def embed_schema_documents():
    documents = build_schema_documents()

    embedded_documents = []

    for document in documents:
        embedding = generate_embedding(document["content"])

        embedded_documents.append({
            "table": document["table"],
            "content": document["content"],
            "embedding": embedding
        })

    return embedded_documents


if __name__ == "__main__":
    embedded_documents = embed_schema_documents()

    for document in embedded_documents:
        print("=" * 60)
        print("Table:", document["table"])
        print("Embedding dimension:", len(document["embedding"]))
        print("First 5 values:", document["embedding"][:5])