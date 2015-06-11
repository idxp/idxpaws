import pytest
from pyidxp.aws.dynamodb import DynamoDB


class TestDynamoDB:
    def get_configs(self):
        return {
            'aws': {
                'dynamodb_local': False,
                'region': 'region',
                'access_key': 'access_key',
                'secret_key': 'secret_key',
            }
        }

    @pytest.fixture(autouse=True)
    def mock_real_connection(self, monkeypatch):
        monkeypatch.setattr('pyidxp.aws.dynamodb.dynamo_connect_to_region',
                            FakeDynamoConnection)

    @pytest.fixture()
    def mock_fake_connection(self, monkeypatch):
        def mock(aws_access_key_id=None, aws_secret_access_key=None,
                 is_secure=None, port=None, host=None):
            return FakeDynamoConnection('localhost')
        monkeypatch.setattr('pyidxp.aws.dynamodb.DynamoDBConnection', mock)

    @pytest.fixture()
    def mock_get_table(self, monkeypatch):
        def mock(name, connection=None):
            return [t for t in connection.tables if t.name == name][0]
        monkeypatch.setattr('pyidxp.aws.dynamodb.Table', mock)

    @pytest.fixture()
    def mock_create_table(self, monkeypatch):
        def mock_create(name, connection=None, schema=None, throughput=None):
            table = FakeTable(name, throughput=throughput)
            connection.tables.append(table)
            return table
        monkeypatch.setattr('pyidxp.aws.dynamodb.Table.create', mock_create)

    def test_connect_to_real_dynamo(self):
        configs = self.get_configs()
        assert DynamoDB(configs).conn.__class__ == FakeDynamoConnection

    def test_connection_params_to_real_dynamo(self):
        configs = self.get_configs()
        DynamoDB(configs)
        params = FakeDynamoConnection.__ref__.conn_params
        assert params['region'] == configs['aws']['region']
        assert params['access_key'] == configs['aws']['access_key']
        assert params['secret_key'] == configs['aws']['secret_key']

    def test_connect_to_fake_dynamo(self, mock_fake_connection):
        configs = self.get_configs()
        configs['aws']['dynamodb_local'] = True
        configs['aws']['region'] = 'localhost'
        assert DynamoDB(configs).conn.conn_params['region'] == 'localhost'

    def test_get_table_that_exists(self, mock_get_table):
        table = DynamoDB(self.get_configs()).get_table('table1')
        assert table.name == 'table1'

    def test_create_table_that_does_not_exist(self, mock_create_table):
        table = DynamoDB(self.get_configs()).get_table('asdasd')
        assert table.__class__ == FakeTable

    def test_update_table(self, mock_create_table):
        dynamo = DynamoDB(self.get_configs())
        table = dynamo.get_table('table2')
        dynamo.update_table(table, {'write': 10, 'read': 10})
        assert table.throughput == {'write': 10, 'read': 10}
        dynamo.conn.host = 'localhost'
        dynamo.update_table(table, {'write': 20, 'read': 20})
        assert table.throughput == {'write': 10, 'read': 10}


class FakeDynamoConnection:
    __ref__ = None

    def __init__(self, region, aws_access_key_id=None,
                 aws_secret_access_key=None, calling_format=None):
        self.__class__.__ref__ = self
        self.conn_params = {
            'region': region,
            'access_key': aws_access_key_id,
            'secret_key': aws_secret_access_key,
        }
        self.tables = [FakeTable('table1')]
        self.host = 'somehost'

    def list_tables(self):
        return {'TableNames': [t.name for t in self.tables]}


class FakeTable:
    def __init__(self, name, throughput={}):
        self.name = name
        self.statuses = ['ACTIVE', 'UPDATING'] * 10
        self.throughput = throughput

    def describe(self):
        return {'Table': {'TableStatus': self.statuses.pop()}}

    def update(self, throughput):
        self.throughput = throughput
