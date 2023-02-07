import boto3
import pandas as pd

class AWSOracleConnection:
    def __init__(self, database_config):
        self.client = boto3.client('rds-data', 
                                  aws_access_key_id=database_config['aws_access_key_id'], 
                                  aws_secret_access_key=database_config['aws_secret_access_key'], 
                                  region_name=database_config['region_name'])
        self.database = database_config['database']
        self.arn = database_config['arn']
        self.secret_arn = database_config['secret_arn']
        self.exec_type = None
        self.query = None
        self.return_type = None

    def select_query(self):
        response = self.client.execute_statement(
            resourceArn=self.arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=self.query
        )
        records = response['records']
        df = pd.DataFrame.from_records(records)
        return df

    def insert_query(self):
        response = self.client.execute_statement(
            resourceArn=self.arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=self.query
        )
        return response

    def update_query(self):
        response = self.client.execute_statement(
            resourceArn=self.arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=self.query
        )
        return response

    def procedure(self):
        response = self.client.execute_statement(
            resourceArn=self.arn,
            secretArn=self.secret_arn,
            database=self.database,
            sql=self.query
        )
        return response

    def run_query(self, query_params):
        self.exec_type = query_params['ExecType']
        self.query = query_params['Query']
        self.return_type = query_params.get('returnType')

        if self.exec_type == 'select':
            df = self.select_query()
            if self.return_type and self.return_type['Type'] == 'file':
                df.to_csv(self.return_type['Details']['Filename'], sep=self.return_type['Details']['Delimeter'], index=False)
                return None
            return df
        elif self.exec_type == 'insert':
            return self.insert_query()
        elif self.exec_type == 'update':
            return self.update_query()
        elif self.exec_type == 'exec_proc':
            return self.procedure()
        else:
            raise Exception("Invalid exec_type")

# Example usage
database_config = {
    'aws_access_key_id': 'your_access_key',
    'aws_secret_

    
    
    
    
import boto3
import pandas as pd

class OracleAWS:
    def __init__(self, config):
        self.exec_type = config.get('ExecType')
        self.query = config.get('Query')
        self.return_type = config.get('returnType')
    
    def execute_query(self):
        # Connect to AWS Oracle instance using boto3
        # Code to execute query
        # Store the result of query execution
        
        result = None # Replace with result of query execution
        return result
    
    def write_to_file(self, result):
        filename = self.return_type['Details']['Filename']
        delimiter = self.return_type['Details']['Delimiter']
        
        # Convert result to pandas dataframe
        df = pd.DataFrame(result)
        
        # Write dataframe to file with specified filename and delimiter
        df.to_csv(filename, sep=delimiter, index=False)
    
    def return_dataframe(self, result):
        delimiter = self.return_type['Details']['Delimiter']
        
        # Convert result to pandas dataframe
        df = pd.DataFrame(result)
        return df
    
    def return_records(self, result):
        delimiter = self.return_type['Details']['Delimiter']
        
        # Convert result to list of records
        records = result.split(delimiter)
        return records
    
    def send_email(self, result):
        # Connect to email server
        # Code to send email with the result
        from_ = self.return_type['Details']['from']
        to = self.return_type['Details']['to']
        subject = self.return_type['Details']['subject']
        body = self.return_type['Details']['body']
        emailout = self.return_type['Details']['emailout']
        source = self.return_type['Details']['source']
        
        pass # Replace with code to send email
    
    def run(self):
        result = self.execute_query()
        if self.return_type['Type'] == 'file':
            self.write_to_file(result)
        elif self.return_type['Type'] == 'dataframe':
            df = self.return_dataframe(result)
        elif self.return_type['Type'] == 'records':
            records = self.return_records(result)
        elif self.return_type['Type'] == 'Email':
            self.send_email(result)
