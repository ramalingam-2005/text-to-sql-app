# 🗄️ Text-to-SQL

An end-to-end **Text-to-SQL application** that allows users to query a
MySQL database using natural language.

Instead of writing SQL manually, users can ask questions such as:

> "Which customers placed orders?"

The application uses **Gemini** to generate SQL from the user's
question, validates the generated SQL, executes it against MySQL, and
displays the results through a simple **Streamlit** interface.

------------------------------------------------------------------------

## ✨ Features

-   🗣️ Ask database questions using natural language
-   🤖 Gemini-powered SQL generation
-   🔎 RAG-based database schema retrieval
-   🧩 Foreign-key relationship-aware schema retrieval
-   🧹 Cleans LLM-generated SQL Markdown code fences
-   🛡️ SQL validation that allows only read-only `SELECT` queries
-   🐬 MySQL database execution
-   ⚡ SQLAlchemy connection pooling
-   🚀 FastAPI backend
-   🎨 Simple Streamlit frontend
-   📊 Results displayed as an interactive table
-   🔐 API keys stored using environment variables
-   🔁 Retry handling for temporary Gemini `503 UNAVAILABLE` errors

------------------------------------------------------------------------

## 🏗️ Architecture

``` text
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │     Frontend        │
                    └──────────┬──────────┘
                               │
                               │ HTTP POST
                               ▼
                    ┌─────────────────────┐
                    │       FastAPI       │
                    │      Backend        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Schema Retriever  │
                    │      + RAG           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Prompt Builder    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Gemini        │
                    │     SQL Generator   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │    SQL Validator    │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   SQLAlchemy /      │
                    │       MySQL         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Result Formatter   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Streamlit      │
                    │       Results       │
                    └─────────────────────┘
```

------------------------------------------------------------------------

## 🔄 How It Works

### 1. User enters a question

Example:

``` text
Show all customers from Chennai.
```

### 2. Schema retrieval

The application retrieves the database schema, including:

-   Tables
-   Columns
-   Data types
-   Primary keys
-   Foreign keys
-   Table relationships

Example:

``` text
customers
    |
    | customer_id
    v
orders
    |
    | order_id
    v
order_items
    |
    | product_id
    v
products
```

### 3. Prompt construction

The relevant schema information is provided to Gemini together with the
user's question.

### 4. Gemini generates SQL

Example:

``` sql
SELECT *
FROM customers
WHERE city = 'Chennai';
```

### 5. SQL validation

The generated SQL is cleaned and validated before reaching the database.

The application blocks dangerous operations such as:

``` text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
RENAME
```

Only read-only `SELECT` queries are allowed.

### 6. SQL execution

The validated SQL is executed against MySQL using SQLAlchemy.

### 7. Results are formatted

Database rows are converted into JSON-friendly objects.

### 8. Streamlit displays the result

The frontend displays:

-   Generated SQL
-   Query results
-   Errors when something goes wrong

------------------------------------------------------------------------

## 🛠️ Tech Stack

  Technology   Purpose
  ------------ --------------------------------------
  Python       Core programming language
  Gemini API   Natural-language-to-SQL generation
  FastAPI      Backend REST API
  Streamlit    Frontend
  MySQL        Relational database
  SQLAlchemy   Database connectivity and inspection
  ChromaDB     Vector storage / schema retrieval
  Pydantic     API request/response validation
  PyMySQL      MySQL driver

------------------------------------------------------------------------

## 📁 Project Structure

``` text
TEXT-TO-SQL-APP/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── embeddings/
│   │   └── embedder.py
│   │
│   ├── schema/
│   │   ├── __init__.py
│   │   ├── inspector.py
│   │   └── formatter.py
│   │
│   ├── vectorstore/
│   │   ├── chroma_store.py
│   │   └── retriever.py
│   │
│   ├── llm/
│   │   ├── llm_client.py
│   │   └── prompt_builder.py
│   │
│   └── sql/
│       ├── validator.py
│       ├── executor.py
│       └── result_formatter.py
│
├── frontend/
│   └── app.py
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

> `models.py` is not required for the current Text-to-SQL flow because
> the application discovers the real database schema using SQLAlchemy's
> inspector rather than relying on manually defined ORM models.

------------------------------------------------------------------------

## ⚙️ Requirements

Make sure you have:

-   Python 3.11+
-   MySQL
-   A Gemini API key
-   Git

------------------------------------------------------------------------

## 🚀 Installation

### 1. Clone the repository

``` bash
git clone https://github.com/YOUR_USERNAME/TEXT-TO-SQL-APP.git
cd TEXT-TO-SQL-APP
```

### 2. Create a virtual environment

Windows:

``` bash
python -m venv .venv
```

Activate it:

``` bash
.venv\Scripts\activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 Environment Variables

Create a `.env` file in the project root:

``` env
GEMINI_API_KEY=your_gemini_api_key

DATABASE_URL=mysql+pymysql://username:password@localhost/database_name
```

Never commit `.env` to GitHub.

Your `.gitignore` should contain:

``` gitignore
.venv/
.env
__pycache__/
*.pyc
.chroma/
```

------------------------------------------------------------------------

## 🗃️ Database

The demo database contains four related tables:

``` text
customers
products
orders
order_items
```

### Customers

``` text
id
name
email
city
```

### Products

``` text
id
name
category
price
```

### Orders

``` text
id
customer_id
order_date
status
```

### Order Items

``` text
id
order_id
product_id
quantity
unit_price
```

The foreign-key relationships allow the application to generate queries
involving multiple tables.

------------------------------------------------------------------------

## ▶️ Running the Application

The project has two parts:

1.  FastAPI backend
2.  Streamlit frontend

### Terminal 1 --- Start FastAPI

``` bash
uvicorn app.main:app --reload
```

The backend runs at:

``` text
http://127.0.0.1:8000
```

API documentation:

``` text
http://127.0.0.1:8000/docs
```

### Terminal 2 --- Start Streamlit

``` bash
streamlit run frontend/app.py
```

The frontend normally runs at:

``` text
http://localhost:8501
```

------------------------------------------------------------------------

## 🧪 Example Questions

Try questions such as:

``` text
Show all customers.
```

``` text
Show customers who live in Chennai.
```

``` text
How many customers are there?
```

``` text
Which customers placed orders?
```

``` text
Show all products.
```

``` text
Show products with price greater than 1000.
```

``` text
Show the products ordered by each customer.
```

The application converts these questions into SQL and executes the
generated query.

------------------------------------------------------------------------

## 📡 API

### `POST /query`

Request:

``` json
{
  "question": "Which customers placed orders?"
}
```

Example response:

``` json
{
  "question": "Which customers placed orders?",
  "sql": "SELECT DISTINCT c.name FROM customers c JOIN orders o ON c.id = o.customer_id;",
  "results": [
    {
      "name": "Ramalingam"
    }
  ]
}
```

------------------------------------------------------------------------

## 🖥️ Screenshots



``` markdown
![Text-to-SQL Interface](docs/home.png)

![Query Results](docs/results.png)
```

------------------------------------------------------------------------

## ⚡ Performance Considerations

The application is designed so that non-LLM latency can be reduced
independently of Gemini generation time.

Potential optimizations include:

-   Cache database schema
-   Cache formatted schema documents
-   Cache the foreign-key relationship graph
-   Avoid unnecessary vector searches
-   Reuse SQLAlchemy connection pools
-   Limit very large result sets
-   Measure retrieval, SQL execution, and formatting latency separately
-   Use in-memory schema access when the database schema is small

Example latency instrumentation:

``` python
import time

start = time.perf_counter()

# operation

elapsed = time.perf_counter() - start

print(f"Operation took {elapsed:.4f}s")
```

------------------------------------------------------------------------

## 🔒 Security

This project is designed as a read-only Text-to-SQL application.

The SQL validation layer blocks write/destructive operations such as:

``` text
INSERT
UPDATE
DELETE
DROP
ALTER
TRUNCATE
CREATE
RENAME
```

However, SQL validation alone should **not** be considered a complete
production security boundary.

For production deployments, use:

-   A dedicated database user
-   Read-only database permissions
-   Query timeouts
-   Row/result limits
-   Authentication and authorization
-   Input/request rate limiting
-   Logging and monitoring
-   Additional SQL parsing/validation

------------------------------------------------------------------------

## 🧠 What I Learned From This Project

This project demonstrates several important concepts:

-   Natural Language Processing
-   Large Language Models
-   Text-to-SQL
-   Retrieval-Augmented Generation (RAG)
-   Embeddings
-   Vector databases
-   Database schema inspection
-   Foreign-key relationship reasoning
-   Prompt engineering
-   SQL validation
-   SQLAlchemy
-   MySQL
-   FastAPI
-   REST APIs
-   Streamlit
-   Error handling
-   Latency optimization

------------------------------------------------------------------------

## 🔮 Future Improvements

-   [ ] Natural-language explanation of query results
-   [ ] Conversational follow-up questions
-   [ ] Query history
-   [ ] Better SQL parsing and validation
-   [ ] Automatic query correction after SQL errors
-   [ ] Result visualization and charts
-   [ ] Schema caching
-   [ ] Advanced relationship-aware retrieval
-   [ ] Authentication
-   [ ] Docker deployment
-   [ ] Automated tests
-   [ ] Production monitoring
-   [ ] Multi-database support

------------------------------------------------------------------------

## 🎯 Project Goal

The goal of this project is to build a practical system that allows
users to interact with relational databases using natural language while
maintaining a clear separation between:

``` text
Natural Language
       ↓
LLM
       ↓
SQL
       ↓
Validation
       ↓
Database
       ↓
Results
```

This project was built as a learning-focused implementation of an
end-to-end AI application rather than simply calling an LLM and
executing its output directly.

------------------------------------------------------------------------

## 👨‍💻 Author

**Ramalingam**

Built as a practical project to learn:

**Machine Learning + LLMs + RAG + SQL + Backend Development**

------------------------------------------------------------------------

## ⭐ If you find this project useful

Give the repository a ⭐ and feel free to explore, improve, and extend
the project.
