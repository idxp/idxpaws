from boto.dynamodb2 import connect_to_region as dynamo_connect_to_region
from boto.dynamodb2.layer1 import DynamoDBConnection
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey

class DynamoDB:
    def __init__(self, configs):
        if configs['aws']['dynamodb_local']:
            self.connect_fake()
        else:
            self.connect_real(configs)


    def connect_fake(self):
        self.conn = DynamoDBConnection(
            aws_access_key_id='foo',
            aws_secret_access_key='bar',
            host='localhost',
            port=8000,
            is_secure=False)

    def connect_real(self, configs):
        self.conn = dynamo_connect_to_region(
            configs['aws']['region'],
            aws_access_key_id=configs['aws']['access_key'],
            aws_secret_access_key=configs['aws']['secret_key'])

    def get_table(self, table_name):
        if table_name in self.conn.list_tables()['TableNames']:
            return Table(table_name, connection=self.conn)
        return Table.create(
            table_name,
            schema=[HashKey('id'), RangeKey('timestamp')],
            throughput={'read': 5, 'write': 15},
            connection=self.conn)
