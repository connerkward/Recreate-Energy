import time

import Constant


class DatabaseManagement:
    def __init__(self, client):
        self.client = client

    def create_database(self):
        print("Creating Database")
        try:
            self.client.create_database(DatabaseName=Constant.DATABASE_NAME)
            print(
                "Database [%s] created successfully." % Constant.DATABASE_NAME
            )
        except self.client.exceptions.ConflictException:
            print(
                "Database [%s] exists. Skipping database creation"
                % Constant.DATABASE_NAME
            )
        except Exception as err:
            print("Create database failed:", err)

    def describe_database(self):
        print("Describing Database")

    def update_database(self, kms_id):
        print("Updating database")
        try:
            result = self.client.update_database(
                DatabaseName=Constant.DATABASE_NAME, KmsKeyId=kms_id
            )
            print(
                "Database [%s] was updated to use kms [%s] successfully"
                % (Constant.DATABASE_NAME, result['Database']['KmsKeyId'])
            )
        except self.client.exceptions.ResourceNotFoundException:
            print("Database doesn't exist")
        except Exception as err:
            print("Update database failed:", err)
