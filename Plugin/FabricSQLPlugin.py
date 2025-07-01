import os  
import struct  
import urllib.parse  
  
import pandas as pd  
from azure import identity  
from sqlalchemy import create_engine  
from typing import Annotated  
from semantic_kernel.functions.kernel_function_decorator import kernel_function  
from dotenv import load_dotenv  
  
class FabricSQLPlugin:  
    """  
    A plugin that retrieves data from a SQL database.  
    """  
  
    SQL_COPT_SS_ACCESS_TOKEN = 1256  # Microsoft constant  
  
    def __init__(self):  
        """  
        Initializes the FabricSQLPlugin3.  
        """  
        pass  
  
    def _get_azure_sql_access_token(self) -> bytes:  
        """  
        Acquire an access token for Azure SQL and return it as expected by ODBC.  
        """  
        credential = identity.DefaultAzureCredential(exclude_interactive_browser_credential=False)  
        token = credential.get_token("https://database.windows.net/.default").token  
        token_bytes = token.encode("UTF-16-LE")  
        token_struct = struct.pack(f"<I{len(token_bytes)}s", len(token_bytes), token_bytes)  
        return token_struct  
  
    def _get_sql_engine(self, connection_string: str, driver: str, token_struct: bytes):  
        """  
        Create a SQLAlchemy engine using Azure AD access token authentication.  
        """  
        odbc_str = (  
            f"Driver={{{driver}}};"  
            f"Server=tcp:{connection_string},1433;"  
            "Encrypt=yes;"  
            "TrustServerCertificate=no;"  
            "Connection Timeout=30;"  
        )  
        quoted_odbc_str = urllib.parse.quote_plus(odbc_str)  
        engine = create_engine(  
            f"mssql+pyodbc:///?odbc_connect={quoted_odbc_str}",  
            connect_args={"attrs_before": {self.SQL_COPT_SS_ACCESS_TOKEN: token_struct}},  
        )  
        return engine  
  
    @kernel_function(name="get_warehouse",  description="Get the names of the fabric warehouse")  
    def get_warehouse(self) -> Annotated[str, "The output is string, to be used in SQL queries"]:  
        load_dotenv(override=True)
        warehouse: str = os.environ.get("FABRIC_WAREHOUSE", "NONE")
        return warehouse

    @kernel_function(name="get_table_names",  description="Get the names of all tables in the database")  
    def get_table_names(self) -> Annotated[str, "The output is an HTML table"]:  
        try:  
            load_dotenv(override=True)  
  
            fabric_connection_string = os.environ.get("FABRIC_CONNECTION_STRING")  
            driver = "ODBC Driver 18 for SQL Server"  
            warehouse = os.environ.get("FABRIC_WAREHOUSE", "NONE")  
  
            # Build the SQL query  
            query = f"""  
                SELECT *   
                FROM [{warehouse}].INFORMATION_SCHEMA.TABLES  
                WHERE TABLE_TYPE = 'BASE TABLE';  
            """  
            print(f"Executing query: {query}")  
  
            # Get Azure token and SQL engine  
            token_struct = self._get_azure_sql_access_token()  
            engine = self._get_sql_engine(fabric_connection_string, driver, token_struct)  
  
            # Query and render as HTML  
            df = pd.read_sql(query, con=engine)  
            html_table = df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')  
            print(html_table)  
            return html_table  
  
        except Exception as e:  
            return f"Error retrieving table names: {e}"  
        
    @kernel_function(name="get_table_schema", description="Get schema for a table to assist in writing SQL queries")
    def get_table_schema(self, table_name: str) -> Annotated[str, "The output is an HTML table"]:
        try:
            load_dotenv(override=True)  
  
            fabric_connection_string = os.environ.get("FABRIC_CONNECTION_STRING")  
            driver = "ODBC Driver 18 for SQL Server"  
            warehouse = os.environ.get("FABRIC_WAREHOUSE", "NONE")  
            query = """
            SELECT COLUMN_NAME, DATA_TYPE, CHARACTER_MAXIMUM_LENGTH, IS_NULLABLE
                FROM [{warehouse}].INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """.format(warehouse=warehouse, table_name=table_name)
            token_struct = self._get_azure_sql_access_token()  
            engine = self._get_sql_engine(fabric_connection_string, driver, token_struct) 
            df = pd.read_sql(query, engine)
            return df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')
        except Exception as e:
            print("Error:", e)
            return f"Error retrieving schema for table '{table_name}': {e}"
        
    @kernel_function(name="execute_sql", description="""
                     With a SELECT statement using fully qualified name: database.dbo.table,  
                     An Example query woudl be: 'SELECT TOP 10 PostalCode FROM [warehouse].[dbo].[dimension_customer];'
                     query the database, and return the results as an HTML table
                     """)
    def execute_sql(self, warehouse: str, sql_query: str) -> Annotated[str, "The output is an HTML table"]:
        try:
            load_dotenv(override=True)  

            fabric_connection_string = os.environ.get("FABRIC_CONNECTION_STRING")  
            driver = "ODBC Driver 18 for SQL Server"  

            print(warehouse)
            print(sql_query)
            
            token_struct = self._get_azure_sql_access_token()  
            engine = self._get_sql_engine(fabric_connection_string, driver, token_struct) 
            df = pd.read_sql(sql_query, engine)
            return df.to_html(index=False, border=0, justify='center', classes='table table-striped table-bordered')
        except Exception as e:
            print("Error:", e)
            return f"Error executing SQL query: {e}"

