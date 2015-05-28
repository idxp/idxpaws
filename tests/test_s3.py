import pytest
from pyidxp.aws.s3 import S3
from boto.s3.connection import OrdinaryCallingFormat


class FakeS3Connection:
    __ref__ = None

    def __init__(self, region, aws_access_key_id=None,
                 aws_secret_access_key=None, calling_format=None):
        self.__class__.__ref__ = self
        self.conn_params = {
            'region': region,
            'access_key': aws_access_key_id,
            'secret_key': aws_secret_access_key,
            'calling_format': calling_format,
        }

    def get_all_buckets(self):
        class B:
            def __init__(self, name):
                self.name = name
        return [B('bucket1'), B('bucket2')]

    def get_bucket(self, name):
        return 'Get ' + name

    def create_bucket(self, name):
        return 'Created ' + name


class TestS3:
    def get_configs(self):
        return {
            'aws': {
                'fakes3': False,
                'region': 'region',
                'access_key': 'access_key',
                'secret_key': 'secret_key',
            }
        }

    @pytest.fixture(autouse=True)
    def mock_real_connection(self, monkeypatch):
        monkeypatch.setattr('pyidxp.aws.s3.s3_connect_to_region',
                            FakeS3Connection)

    @pytest.fixture()
    def mock_fake_connection(self, monkeypatch):
        def mock(access_key, secret_key, is_secure=None, port=None, host=None,
                 calling_format=None):
            self.fake_conn_params = {
                'calling_format': calling_format,
            }
            return 's3_fake_conn'
        monkeypatch.setattr('pyidxp.aws.s3.S3Connection', mock)

    def test_connect_to_real_s3(self):
        configs = self.get_configs()
        assert S3(configs).conn.__class__ == FakeS3Connection

    def test_connection_params_to_real_s3(self):
        configs = self.get_configs()
        S3(configs)
        params = FakeS3Connection.__ref__.conn_params
        assert params['region'] == configs['aws']['region']
        assert params['access_key'] == configs['aws']['access_key']
        assert params['secret_key'] == configs['aws']['secret_key']
        assert params['calling_format'].__class__ == OrdinaryCallingFormat

    def test_connect_to_fake_s3(self, mock_fake_connection):
        configs = self.get_configs()
        configs['aws']['fakes3'] = True
        assert S3(configs).conn == 's3_fake_conn'

    def test_connection_params_to_fake_s3(self, mock_fake_connection):
        configs = self.get_configs()
        configs['aws']['fakes3'] = True
        S3(configs)
        params = self.fake_conn_params
        assert params['calling_format'].__class__ == OrdinaryCallingFormat

    def test_get_bucket_that_exists(self):
        assert S3(self.get_configs()).get_bucket('bucket1') == 'Get bucket1'

    def test_create_bucket_that_does_not_exist(self):
        assert S3(self.get_configs()).get_bucket('asdasd') == 'Created asdasd'
