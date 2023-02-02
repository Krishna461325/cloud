import boto3

class SecretManager:
    def __init__(self, account):
        self.account = account
        self.client = boto3.client("secretsmanager")

    def get_credentials(self):
        secret_name = self.account + "_credentials"
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
        except self.client.exceptions.ResourceNotFoundException as e:
            print("Error: The requested secret " + secret_name + " was not found")
            return None
        except self.client.exceptions.InvalidRequestException as e:
            print("Error: The request was invalid due to:", e)
            return None
        except self.client.exceptions.InvalidParameterException as e:
            print("Error: The request had invalid params:", e)
            return None
        else:
            # Decrypts secret using the associated KMS CMK.
            # Depending on whether the secret is a string or binary, one of these fields will be populated.
            if "SecretString" in response:
                secret = response["SecretString"]
            else:
                secret = response["SecretBinary"]
            return eval(secret)
