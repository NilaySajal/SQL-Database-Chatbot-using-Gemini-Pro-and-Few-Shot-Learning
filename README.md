# RAG SQL Reader Application

This project is a Retrieval-Augmented Generation (RAG) application aimed at optimizing interactions with an SQL database. It leverages few-shot learning techniques to tailor a Large Language Model (LLM) to the database's structure. For this, it utilizes Gemini-Pro, a language model developed by Google. The front end is built with Streamlit, offering a user-friendly interface for effortless database interaction.

# Features

- SQL Query Generation: The application can automatically generate SQL queries based on user input in natural language. Users can enter their queries or questions, and the system utilizes an LLM to create SQL queries tailored to the specific database schema.

- Few-Shot Learning: The application employs few-shot learning techniques to fine-tune the LLM for the given database schema. By using a limited set of example-query pairs and leveraging schema details, the model learns to generalize and generate precise SQL queries for diverse user inputs.

- Schema Adaptation: The system dynamically adjusts to changes in the database schema. By analyzing the schema structure, the LLM modifies its query generation approach to accommodate updates or alterations, ensuring consistent and reliable performance.

- Streamlit Interface: The front end is built using Streamlit, a framework designed for developing interactive web applications. This interface offers an intuitive and responsive platform, enabling users to effortlessly interact with the SQL database, create queries, and explore data.

# Database

AtliQ Tees is a T-shirt store where they maintain their inventory, sales and discounts data in MySQL database. They sell Adidas, Nike, Van Heusen and Levi's t shirts. The entire information regarding the database and its schemas is present in the atliq_tshirts_inventory.sql file. 

