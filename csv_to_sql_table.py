# Dependencias
# pip install pandas mysql-connector-python

# Uso
#  Substitua your_username, your_password e your_database pelos detalhes apropriados de conexão com o banco de dados MySQL.
#  Este script define uma função chamada csv_to_sql_table, que recebe como parâmetros o nome do arquivo CSV, o nome da tabela e a configuração do banco de dados. A função lê o arquivo CSV usando a biblioteca pandas, conecta-se ao banco de dados MySQL, cria uma tabela se ela não existir e insere os dados do DataFrame na tabela.


import pandas as pd
import mysql.connector
from mysql.connector import Error


def csv_to_sql_table(csv_file, table_name, db_config):
    # Ler o arquivo CSV usando pandas
    df = pd.read_csv(csv_file)

    # Conectar ao banco de dados MySQL
    try:
        connection = mysql.connector.connect(**db_config)

        if connection.is_connected():
            cursor = connection.cursor()

            # Criar a tabela no banco de dados se não existir
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join([f'{col} TEXT' for col in df.columns])});")
            connection.commit()

            # Inserir dados do DataFrame na tabela
            for _, row in df.iterrows():
                sql_query = f"INSERT INTO {table_name} ({', '.join(df.columns)}) VALUES ({', '.join(['%s'] * len(df.columns))})"
                cursor.execute(sql_query, tuple(row))

            connection.commit()
            print(f"Os dados do arquivo {csv_file} foram inseridos na tabela {table_name} com sucesso.")
        else:
            print("Não foi possível conectar ao banco de dados.")

    except Error as e:
        print(f"Erro: {e}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("Conexão encerrada.")


if __name__ == "__main__":
    db_config = {
        "host": "localhost",
        "user": "your_username",
        "password": "your_password",
        "database": "your_database"
    }

    csv_file = "example.csv"
    table_name = "example_table"

    csv_to_sql_table(csv_file, table_name, db_config)

