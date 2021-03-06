"""Role testing files using testinfra."""
import pytest


@pytest.mark.parametrize("name", [
    "pcsd",
    "corosync",
    "pacemaker"
])
def test_cluster_services(host, name):
    service = host.service(name)

    assert service.is_valid
    assert service.is_enabled
    assert service.is_running


def test_cluster_status(host):
    cmd = host.run("pcs status")

    assert "2 nodes configured" in cmd.stdout
    assert "Online: [ vm-1 vm-2 ]" in cmd.stdout


def test_resource_listening(host):
    socket = host.socket('tcp://0.0.0.0:8080')

    assert socket.is_listening
