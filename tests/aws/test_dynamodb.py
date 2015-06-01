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
            return 'dynamo_fake_conn'
        monkeypatch.setattr('pyidxp.aws.dynamodb.DynamoDBConnection', mock)

    @pytest.fixture()
    def mock_get_table(self, monkeypatch):
        def mock(name, connection=None):
            return 'Get ' + name
        monkeypatch.setattr('pyidxp.aws.dynamodb.Table', mock)

    @pytest.fixture()
    def mock_created_table(self, monkeypatch):
        def mock(name, connection=None, schema=None, throughput=None):
            connection.tables.append(name)
            return 'Created ' + name
        monkeypatch.setattr('pyidxp.aws.dynamodb.Table.create', mock)

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
        assert DynamoDB(configs).conn == 'dynamo_fake_conn'

    def test_get_table_that_exists(self, mock_get_table):
        table = DynamoDB(self.get_configs()).get_table('table1')
        assert table == 'Get table1'

    def test_create_table_that_does_not_exist(self, mock_created_table):
        table = DynamoDB(self.get_configs()).get_table('asdasd')
        assert table == 'Created asdasd'


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
        self.tables = ['table1', 'table2']

    def list_tables(self):
        return {'TableNames': self.tables}
