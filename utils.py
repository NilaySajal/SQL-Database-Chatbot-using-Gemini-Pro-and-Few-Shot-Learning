from langchain.chains import LLMChain
from langchain_community.utilities.sql_database import SQLDatabase
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import PromptTemplate
from langchain_google_vertexai import VertexAI


load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/nilaypatel/Downloads/gen-lang-client-0005124514-22c8bed7cf64.json"

genai.configure(api_key=google_api_key)

def initialize_db_connection():
    # Connect to the SQL database
    # if you are using MySQL
    mysql_uri = 'mysql+mysqlconnector://root:Sqluser@localhost:3306/atliq_tshirts'
    db = SQLDatabase.from_uri(mysql_uri)

    return db

def get_schema_db(db):
    # Schema of the db
    schema = db.get_table_info()
    return schema


def build_few_shots_prompt(db):
    # Get schema
    db_schema = get_schema_db(db)

    few_shots = [
    {
        "input" : "How many t-shirts do we have left for Levi's in XS size and white color?",
        "query" : "SELECT SUM(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND size = 'XS' AND color = 'White';"},
    
    {
        "input" : "How much is the total price of the inventory for all S-size t-shirts?",
        "query" : "SELECT SUM(price*stock_quantity) FROM t_shirts WHERE size = 'S';"
    },
    {
        "input" : "If we have to sell all the Levi’s T-shirts today with discounts applied. How much revenue  our store will generate (post discounts)?",
        "query" : """SELECT sum(a.total_amount * ((100-COALESCE(discounts.pct_discount,0))/100)) as total_revenue from
(select sum(price*stock_quantity) as total_amount, t_shirt_id from t_shirts where brand = 'Levi'
group by t_shirt_id) a left join discounts on a.t_shirt_id = discounts.t_shirt_id;
 """
    },
    {
        "input" : "If we have to sell all the Levi’s T-shirts today. How much revenue our store will generate without discount?",
        "query" : "SELECT SUM(price * stock_quantity) FROM t_shirts WHERE brand = 'Levi';"
    },
    {
        "input" : "How many white color Levi's shirt I have?",
        "query" : "SELECT sum(stock_quantity) FROM t_shirts WHERE brand = 'Levi' AND color = 'White';"
    }
    ]

    prompt = [
    f"""
    You are an expert in converting English questions to SQL query!
    The SQL database has 2 tables, and these are the schemas: {db_schema}.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    Also the sql code should not have ``` in beginning or end and sql word in output.
    You must double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    Do not make any DML statements (INSERT, UPDATE , DELETE, DROP etc.) to the database.

    If the question does not seem related to the databse, just return "I don't Know" as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:

    """,
    ]

    # Append each example to the prompt
    for sql_example in few_shots:
        prompt.append(
            f"\nExample - {sql_example['input']}, the SQL command will be something like this {sql_example['query']}")

    # Join prompt sections into a single string
    formatted_prompt = [''.join(prompt)]

    return formatted_prompt


def generate_sql_query(prompt, user_question):
    # Model to generate SQL query
    model = genai.GenerativeModel('gemini-pro')
    # Generate SQL query
    sql_query = model.generate_content([prompt[0], user_question])

    return sql_query.text

def run_query(db, sql_query):
    # Run sql query
    return db.run(sql_query)


def get_vertexai_llm():
    # LLM
    llm = VertexAI(model_name = "gemini-pro")
    return llm


def chain_query(llm, sql_response, user_question):
    # Template
    template = """
                Based on the user question and sql response, write an intuitive answer:

                User Question: {user_question}
                
                SQL response: {sql_response}
                """
    # Prompt template
    prompt_template = PromptTemplate(template=template, input_variables=['user_question','sql_response'])

    # Chain
    chain = LLMChain(llm = llm, prompt = prompt_template)

    # Answer
    answer = chain.run(user_question=user_question, sql_response=sql_response)  # Pass arguments as keyword args

    return answer