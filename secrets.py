import boto3

class SecretManager:
    def __init__(self, account, secret_name):
        self.client = boto3.client('secretsmanager')
        self.account = account
        self.secret_name = secret_name

    def get_credentials(self):
        # retrieve secrets from AWS Secrets Manager
        response = self.client.get_secret_value(SecretId=self.secret_name)
        secret = response['SecretString']
        # parse the secret string and return username and password
        return {
            "username": secret['username'],
            "password": secret['password']
        }

# sample program to call the class
secret_manager = SecretManager("my_account", "my_secret_name")
credentials = secret_manager.get_credentials()
print(credentials)

