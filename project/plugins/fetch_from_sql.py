from taskweaver.plugin import Plugin, register_plugin
try:
    import pandas as pd
    import pymysql
except ImportError:
    raise ImportError("Please install necessary packages before running the plugin")

@register_plugin
class SQLQueryPlugin(Plugin):
    def __call__(self, host, user, password, db, query):
        """SQL query plugin implementation."""
        # Establish a connection to the MySQL database using pymysql
        conn = pymysql.connect(host=host, user=user, password=password, db=db)
        
        # Create a cursor object to execute the SQL query
        cur = conn.cursor()
        
        # Execute the SQL query using the cursor
        cur.execute(query)
        
        # Fetch all the rows from the query result
        rows = cur.fetchall()
        
        # Get the column names from the cursor description
        columns = [desc[0] for desc in cur.description]
        
        # Create a pandas DataFrame from the query result
        df = pd.DataFrame(rows, columns=columns)
        
        # Close the cursor and connection
        cur.close()
        conn.close()
        
        # Return the query result as a pandas DataFrame
        return df.to_dict('records')
