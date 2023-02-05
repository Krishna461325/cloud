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

