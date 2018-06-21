from datetime import datetime

import implement_me
import pytest
import datasets
from db_handler import create_all_tables, delete_all_tables
from interface import Entry
import ipaddr


@pytest.fixture()
def setup_data():
    create_all_tables()
    yield
    delete_all_tables()


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


def test_get_device_status(setup_data):
    ip_addr_base = '10.10.20.'
    protocol = 'HTTPS'
    data = []
    num_of_ips = 10
    num_of_timestamps = 3
    for i in range(num_of_ips):
        ip_addr = ip_addr_base + str(i)
        for j in range(num_of_timestamps):
            timestamp = datetime.now()
            data.append(Entry(str(ipaddr.IPAddress(ip_addr)), protocol=protocol, timestamp=timestamp))

    implement_me.index(data)
    status = implement_me.get_devices_status()
    assert len(status) == num_of_ips
    # Check last inserted ip and timestamp
    last_inserted_ip_and_timestamp_returned = status[-1]
    last_inserted_ip_and_timestamp = data[-1]
    assert last_inserted_ip_and_timestamp_returned[0] == last_inserted_ip_and_timestamp.ip
    assert last_inserted_ip_and_timestamp_returned[1] == last_inserted_ip_and_timestamp.timestamp
    
    # Check last inserted timestamp for first ip
    first_inserted_ip_returned_status = status[0]
    first_inserted_ip_data = data[num_of_timestamps - 1]
    assert first_inserted_ip_returned_status[0] == first_inserted_ip_data.ip
    assert first_inserted_ip_returned_status[1] == first_inserted_ip_data.timestamp


def test_adding_and_fetching_s1wide(setup_data):
    data = datasets.s1wide()
    check_data(data, 128)


def check_data(data, count):
    implement_me.index(data)
    status = implement_me.get_devices_status()
    assert len(status) == count
    num_of_timestamps = 10
    histogram = implement_me.get_device_histogram(status[0][0], num_of_timestamps)
    assert len(histogram) == num_of_timestamps


def test_adding_and_fetching_s1narrow(setup_data):
    data = datasets.s1narrow()
    check_data(data, 16)


def test_adding_and_fetching_l1wide(setup_data):
    data = datasets.l1wide()
    check_data(data, 16384)


def test_adding_and_fetching_l1narrow(setup_data):
    data = datasets.l1narrow()
    check_data(data, 128)
