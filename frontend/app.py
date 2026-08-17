import requests
import streamlit as st


API_URL = "http://127.0.0.1:8000/query"


st.set_page_config(
    page_title="Text-to-SQL",
    page_icon="🗄️",
    layout="centered"
)


st.title("🗄️ Text-to-SQL")
st.write(
    "Ask a question about your database using natural language."
)


question = st.text_input(
    "Enter your question",
    placeholder="Example: Which customers placed orders?"
)


if st.button("Run Query"):

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating SQL and querying database..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": question
                    },
                    timeout=60
                )

                if response.status_code == 200:

                    data = response.json()

                    st.success("Query executed successfully!")

                    st.subheader("Generated SQL")

                    st.code(
                        data["sql"],
                        language="sql"
                    )

                    st.subheader("Results")

                    if data["results"]:

                        st.dataframe(
                            data["results"],
                            use_container_width=True
                        )

                    else:

                        st.info(
                            "The query returned no results."
                        )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    st.code(response.text)

            except requests.exceptions.ConnectionError:

                st.error(
                    "Could not connect to the FastAPI server."
                )

                st.info(
                    "Make sure FastAPI is running on "
                    "http://127.0.0.1:8000"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "The request took too long."
                )

            except Exception as error:

                st.error(
                    f"Unexpected error: {error}"
                )