import json
import boto3

class GetCredentials:
    def __init__(self, file_path):
        self.file_path = file_path
        with open(file_path, "r") as f:
            self.data = json.load(f)

    def windlogincreds(self):
        wind_login_creds = self.data["WinLoginCreds"]
        sec_type = wind_login_creds["SecType"]
        if sec_type == "Secretmanager":
            client = boto3.client("secretsmanager")
            secret_name = wind_login_creds["Winloginid"]
            response = client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        else:
            raise Exception("Invalid security type")

    def linlogincreds(self):
        lin_login_creds = self.data["LinloginCreds"]
        sec_type = lin_login_creds["SecType"]
        if sec_type == "Secretmanager":
            client = boto3.client("secretsmanager")
            secret_name = lin_login_creds["Linloginid"]
            response = client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        else:
            raise Exception("Invalid security type")

    def Lindbcreds(self):
        lin_db_creds = self.data["LinDbCreds"]
        sec_type = lin_db_creds["SecType"]
        if sec_type == "Secretmanager":
            client = boto3.client("secretsmanager")
            secret_name = lin_db_creds["LinDbid"]
            response = client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        else:
            raise Exception("Invalid security type")

    def Windbcreds(self):
        win_db_creds = self.data["WinDbCreds"]
        sec_type = win_db_creds["SecType"]
        if sec_type == "Secretmanager":
            client = boto3.client("secretsmanager")
            secret_name = win_db_creds["WinDbid"]
            response = client.get_secret_value(SecretId=secret_name)
            return response["SecretString"]
        else:
            raise Exception("Invalid security type")

    def etlcreds(self):
        etl_creds = self.data["EtlCreds"]
        sec_type = etl_creds["SecType"]
        if sec_type == "PAM":
            # Run the os command to retrieve credentials from EPV
            return "Credentials retrieved from EPV"
        else:
            raise Exception("Invalid security type")

def default(self, json_data):
    account = json_data["account"]
    secret_id = json_data["secretid"]
    client = boto3.client("secretsmanager")
    response = client.get_secret_value(SecretId=secret_id)
    return response["SecretString"]





## how to use

# Initialize the class with the file path
creds = GetCredentials("C:/temp/env.json")

# Call the desired method to retrieve the credentials
win_login_creds = creds.windlogincreds()
lin_login_creds = creds.linlogincreds()
lin_db_creds = creds.Lindbcreds()
win_db_creds = creds.Windbcreds()
etl_creds = creds.etlcreds()

# Use the default method to retrieve credentials for a given account and secret id
json_data = {"account": "accountid", "secretid": "secretid"}
default_creds = creds.default(json_data)

# The credentials are now stored in the respective variables and can be used as needed

