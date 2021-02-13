"""Role testing files using testinfra."""
import pytest


def test_cluster_group(host):
    group = host.group("pcs_cluster")

    assert group.exists


def test_cluster_user(host):
    user = host.user("pcs_cluster")

    assert user.exists
    assert user.group == "pcs_cluster"


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
    assert "Online: [ centos7-1 centos7-2 ]" in cmd.stdout
