import pytest


@pytest.fixture()
def CephNode(Ansible, Interface, request):
    vars = Ansible.get_variables()
    node_type = vars["group_names"][0]
    if not request.node.get_marker(node_type):
        pytest.skip("Not a valid test for node type")

    # I can assume eth1 because I know all the vagrant
    # boxes we test with use that interface
    address = Interface("eth1").addresses[0]
    subnet = ".".join(vars["public_network"].split(".")[0:-1])
    data = dict(
        address=address,
        subnet=subnet,
        vars=vars,
    )
    return data


def pytest_collection_modifyitems(session, config, items):
    for item in items:
        test_path = item.location[0]
        if "mon" in test_path:
            item.add_marker(pytest.mark.mons)
        elif "osd" in test_path:
            item.add_marker(pytest.mark.osds)
        elif "mds" in test_path:
            item.add_marker(pytest.mark.mdss)
        elif "rgw" in test_path:
            item.add_marker(pytest.mark.rgws)
        else:
            item.add_marker(pytest.mark.all)
