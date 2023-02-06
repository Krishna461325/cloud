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
