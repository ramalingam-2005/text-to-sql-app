import os

from dotenv import load_dotenv
from google import genai
import os
import time


from app.vectorstore.retriever import retrieve_schema
from app.llm.prompt_builder import build_sql_prompt
from app.sql.executor import execute_sql

from app.sql.result_formatter import format_results

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY was not found in the .env file."
    )

client = genai.Client(api_key=api_key)


def generate_sql(prompt, max_retries=3):

    for attempt in range(max_retries):

        try:
            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            return response.text

        except Exception as error:

            if attempt == max_retries - 1:
                raise error

            wait_time = 2 ** attempt

            print(
                f"Gemini temporarily unavailable. "
                f"Retrying in {wait_time} seconds..."
            )

            time.sleep(wait_time)


def text_to_sql(question, top_k=5):

    results = retrieve_schema(
        question,
        top_k=top_k
    )

    schema_documents = []

    for document, metadata in zip(
        results["documents"][0],
        results["metadatas"][0]
    ):
        schema_documents.append({
            "table": metadata["table"],
            "content": document
        })

    prompt = build_sql_prompt(
        question,
        schema_documents
    )

    sql = generate_sql(prompt)

    return sql


def ask_database(question, top_k=5):

    sql = text_to_sql(
        question,
        top_k=top_k
    )

    print("\nGenerated SQL:")
    print(sql)

    rows = execute_sql(sql)

    results = format_results(rows)

    return {
        "sql": sql,
        "results": results
    }


if __name__ == "__main__":

    question = "Which customers placed orders?"

    results = ask_database(question)

    print("\nQuery Results:")

    for row in results:
        print(dict(row))