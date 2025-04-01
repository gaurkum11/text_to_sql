import os
import sqlite3
import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate




def get_sql_query_from_text(user_query):

    # groq_sys_prompt = ChatPromptTemplate.from_template("""
    #                                                     You are an expert in converting ENglish questions to SQL Query!
    #                                                    The SQL database has the name STUDENT and has following columns - NAME, COURSE, SECTION and MARKS. For example,
    #                                                    Example 1 - How many entries of record are present?
    #                                                    the SQL command will be something like this SELECT COUNT(*) FROM STUDENT;
    #                                                    Exmaple 2 - Tell me all students studying in Data science COURSE?
    #                                                    the SQL command will ve something like this SELECT * FROM STUDENT WHERE COURSE = "Data Science";
    #                                                    also the sql code should not have ``` in beginning or end and sql word in output.
    #                                                    Now convert the following question in English to avoid SQL Query : {user_query}.
    #                                                    No preamble, only valid SQL phrase.
    #                                                    """)
    
    groq_sys_prompt = ChatPromptTemplate.from_template("""
    You are an expert in converting English questions into SQL queries!
    The SQL database is named sale and has the following columns:
    ORDERNUMBER, QUANTITYORDERED, PRICEEACH, ORDERLINENUMBER, SALES, 
    ORDERDATE, STATUS, QTR_ID, MONTH_ID, YEAR_ID, PRODUCTLINE, MSRP, 
    PRODUCTCODE, CUSTOMERNAME, PHONE, ADDRESSLINE1, ADDRESSLINE2, CITY, 
    STATE, POSTALCODE, COUNTRY, TERRITORY, CONTACTLASTNAME, CONTACTFIRSTNAME, DEALSIZE.

    Example 1: 
    Q: How many orders are present?
    A: SELECT COUNT(*) FROM sale;

    Example 2: 
    Q: Show me all orders where the deal size is large.
    A: SELECT * FROM sale WHERE DEALSIZE = 'Large';

    The output should be a valid SQL query without any surrounding code blocks (```).
    Now convert the following question into a SQL query: {user_query}.
                                                       """)
    


    model = "llama3-8b-8192"
    llm = ChatGroq(
        groq_api_key = os.environ.get("GROQ_API_KEY"),
        model_name=model
    )

    chain = groq_sys_prompt | llm | StrOutputParser()
    sql_query = chain.invoke({"user_query" : user_query})
    return sql_query 


def get_data_from_database(sql_query):
    db = "sale.db"
    with sqlite3.connect(db) as conn:
        return conn.execute(sql_query).fetchall()
    



def main():
    st.set_page_config(page_title="TEXT TO SQL")
    st.header("Talk with your database")

    user_query=st.text_input("Input : ")
    submit = st.button("Enter")

    if submit:
        sql_query= get_sql_query_from_text(user_query)
        req_data = get_data_from_database(sql_query)
        #st.header("Hi I am you AI assistant!")
        st.header(f"Retrieving data from db with the query : [{sql_query}]")
        for row in req_data:
            st.header(row)

if __name__== '__main__':
    main()

