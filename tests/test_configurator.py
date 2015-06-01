import pytest
from pyidxp.configurator import configuration


class TestConfigurator:
    @pytest.fixture()
    def mock_consul(self, monkeypatch):
        def mock(arg1):
            return True
        monkeypatch.setattr('pyidxp.configurator.which', mock)
        monkeypatch.setattr('pyidxp.configurator.Consul', FakeConsul)

    @pytest.fixture()
    def mock_open(self, monkeypatch):
        def mock(*args):
            class Mock:
                def read(self):
                    return "{}"
            return Mock()
        monkeypatch.setattr('builtins.open', mock)

    def test_return_decoded_json_from_config_file(self, mock_open):
        assert configuration('anykey').__class__ == dict

    def test_return_from_consul(self, mock_consul):
        assert configuration('anykey') == {'consul': True}


class FakeConsul:
    def __init__(self):
        self.kv = self

    def get(self, name):
        return [None, {'Value': b'{"consul":true}'}]
