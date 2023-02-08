import cx_Oracle

def execute_stored_proc(procname, input_params=None, output_params=None):
    # Connect to the Oracle database
    conn = cx_Oracle.connect("user/password@oracle_sid")
    cursor = conn.cursor()

    # Prepare the input parameters for the stored procedure
    if input_params:
        input_params = ",".join(str(x) for x in input_params)
    else:
        input_params = ""

    # Prepare the output parameters for the stored procedure
    if output_params:
        output_params = ",".join(":" + x for x in output_params)
    else:
        output_params = ""

    # Execute the stored procedure
    cursor.callproc(procname, [input_params, output_params])

    # Fetch the output parameters if they were specified
    if output_params:
        results = cursor.fetchall()
        return results

# Example usage:
# Scenario 1: Execute stored procedure with input parameters
input_params = [1, 2, 3]
execute_stored_proc("procname", input_params)

# Scenario 2: Execute stored procedure with input and output parameters
input_params = [1, 2, 3]
output_params = ["out1", "out2"]
results = execute_stored_proc("procname", input_params, output_params)

# Scenario 3: Execute stored procedure 




import cx_Oracle

class Oracle:
    def __init__(self, connection_string):
        self.conn = cx_Oracle.connect(connection_string)
        self.cursor = self.conn.cursor()

    def query(self, query_string):
        try:
            self.cursor.execute(query_string)
            return self.cursor.fetchall()
        except cx_Oracle.DatabaseError as e:
            print("An error occurred while querying the database:", e)

    def insert(self, insert_string):
        try:
            self.cursor.execute(insert_string)
            self.conn.commit()
        except cx_Oracle.DatabaseError as e:
            print("An error occurred while inserting data into the database:", e)
            self.conn.rollback()

    def update(self, update_string):
        try:
            self.cursor.execute(update_string)
            self.conn.commit()
        except cx_Oracle.DatabaseError as e:
            print("An error occurred while updating data in the database:", e)
            self.conn.rollback()

    def delete(self, delete_string):
        try:
            self.cursor.execute(delete_string)
            self.conn.commit()
        except cx_Oracle.DatabaseError as e:
            print("An error occurred while deleting data from the database:", e)
            self.conn.rollback()

    def execute_proc(self, proc_name, *args):
        try:
            self.cursor.callproc(proc_name, args)
            self.conn.commit()
        except cx_Oracle.DatabaseError as e:
            print("An error occurred while executing the stored procedure:", e)
            self.conn.rollback()

    def close(self):
        self.cursor.close()
        self.conn.close()

