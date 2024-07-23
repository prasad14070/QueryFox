import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel("gemini-pro")
    return model

def generate_sql_query(model, input_prompt):
    template = """
        Create a SQL query snippet using the below text:

        ```
        {text_input}
        ```  
        i just want a Sql query         
    """
    formatted_template = template.format(text_input=input_prompt)
    response = model.generate_content(formatted_template)
    sql_query = response.text.strip().lstrip("```sql").rstrip("```")
    return sql_query

def generate_expected_output(model, sql_query):
    expected_output = """
        What would be the expected response of this SQL query snippet:

        ```
        {sql_query}
        ```  
        Provide sample table response with no explanation        
    """
    expected_output_formatted = expected_output.format(sql_query=sql_query)
    response = model.generate_content(expected_output_formatted)
    return response.text

def generate_explanation(model, sql_query):
    explanation = """
        Explain this SQL query:

        ```
        {sql_query}
        ```  
        Please provide the simplest explanation:       
    """
    explanation_formatted = explanation.format(sql_query=sql_query)
    response = model.generate_content(explanation_formatted)
    return response.text

def sql_formatter(model, sql_code):
    template = """
        Format this SQL code block:

        ```
        {sql_code}
        ```  
        Format this SQL code        
    """
    formatted_template = template.format(sql_code=sql_code)
    response = model.generate_content(formatted_template)
    formatted_sql = response.text.strip().lstrip("```sql").rstrip("```")
    return formatted_sql

def query_explainer(model, sql_syntax):
    explanation = """
        Explain each part of this SQL query:

        ```
        {sql_syntax}
        ```  
        Please break down the query and explain each important concept or word:      
    """
    explanation_formatted = explanation.format(sql_syntax=sql_syntax)
    response = model.generate_content(explanation_formatted)
    return response.text

def main():
    model = configure()
    st.set_page_config(page_title="QueryFox", page_icon="robot:")

    st.sidebar.title('Navigation')
    pages = st.sidebar.radio("Go to", ['About', 'SQL Query Generator', 'SQL Formatter', 'Query Explainer'])

    if pages == 'About':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>QueryFox 🤖</h1>
            <h3>Your Personal SQL Query Assistant</h3>
            <p> Welcome to QueryFox! Our project is your personal SQL query assistant powered by Google's Generative AI tools. 
            With QueryFox, you can effortlessly generate SQL queries and receive detailed explanations, and also format your for readability and consistency. Let's simplifying your data retrieval process!</p>           
            </div>
            """,
            unsafe_allow_html=True,
        )

    elif pages == 'SQL Query Generator':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>SQL Query Generator 📝</h1>
            <p>Use the SQL Query Generator to create SQL queries from natural language prompts.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        text_input = st.text_area("Type your desired query below to unlock the power of SQL Query Genie! 💬")
        submit = st.button("Generate SQL Query")

        if submit:
            with st.spinner("Generating SQL Query.."):
                sql_query = generate_sql_query(model, text_input)
                eoutput = generate_expected_output(model, sql_query)
                explanation = generate_explanation(model, sql_query)
                with st.container():
                    st.success("Your SQL query has been successfully generated. Feel free to copy and paste it into your database management system to retrieve the requested records.")
                    st.code(sql_query, language="sql")

                    st.markdown(
                        """
                        <div style="background-color: #d4edda; padding: 10px; border-radius: 5px;">
                            Expected output of this SQL Query.<br>
                            If the structure of the query isn't displayed, please click again on the 'Generate SQL Query' button.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(eoutput)

                    st.success("Explanation of SQL Query")
                    st.markdown(explanation)

    elif pages == 'SQL Formatter':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>SQL Formatter 📋</h1>
            <p>Use the SQL formatter to format your SQL queries for readability and consistency.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sql_input = st.text_area("Paste your SQL code here:")
        format_button = st.button("Format SQL")

        if format_button:
            if sql_input:
                formatted_sql = sql_formatter(model, sql_input)
                st.code(formatted_sql, language='sql')

    elif pages == 'Query Explainer':
        st.markdown(
            """
            <div style="text-align:center;">
            <h1>Query Explainer 📢</h1>
            <p>Understand each part of your SQL query with explanations.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        sql_syntax = st.text_area("Paste your SQL syntax here:")
        explain_button = st.button("Explain Query")

        if explain_button:
            if sql_syntax:
                explanation = query_explainer(model, sql_syntax)
                st.markdown(explanation)

if __name__ == "__main__":
    main()
