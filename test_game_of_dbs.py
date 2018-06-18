from datetime import datetime

import implement_me
import pytest
import datasets
from db_handler import recreate_all_tables
from interface import Entry
import ipaddr


@pytest.fixture()
def setup_data():
    recreate_all_tables()


def test_get_device_histogram(setup_data):
    ip_addr = '10.10.20.20'
    protocol = 'HTTPS'
    data = []
    for i in range(10):
        timestamp = datetime.now()
        data.append(Entry(str(ipaddr.IPAddress(ip_addr)), protocol=protocol, timestamp=timestamp))

    implement_me.index(data)
    histogram = implement_me.get_device_histogram(ip_addr, 10)
    assert len(histogram) == 10
    assert histogram[-1]['timestamp'] == data[0].timestamp
    assert histogram[0]['protocol'] == protocol


def test_adding_and_fetching_s1wide(setup_data):
    data = datasets.s1wide()
    check_data(data, 128)


def check_data(data, count):
    implement_me.index(data)
    histogram = implement_me.get_device_histogram('72.126.116.190', 10)
    assert len(histogram) == 10
    status = implement_me.get_devices_status()
    assert len(status) == count


def test_adding_and_fetching_s1narrow(setup_data):
    data = datasets.s1narrow()
    check_data(data, 16)


def test_adding_and_fetching_l1wide(setup_data):
    data = datasets.l1wide()
    check_data(data, 16384)


def test_adding_and_fetching_l1narrow(setup_data):
    data = datasets.l1narrow()
    check_data(data, 128)
