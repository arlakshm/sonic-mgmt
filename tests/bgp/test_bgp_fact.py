import pytest
import logging
#from tests.common.devices import get_asic_ids 
logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.topology('any'),
    pytest.mark.device_type('vs')
]

#@pytest.mark.parametrize("asic_id",get_asic_ids())
def test_bgp_facts(duthosts, dut_index, asic_index):
    """compare the bgp facts between observed states and target state"""

    duthost = duthosts[dut_index]
    logging.info("hostname {}".format(duthost.hostname))
    logging.info("dut_index = {} asic_id {}".format(dut_index, asic_index))
    
    bgp_facts = duthost.get_bgp_facts()
    
    config_facts = duthost.get_config_facts()

    for k, v in bgp_facts['bgp_neighbors'].items():
        # Verify bgp sessions are established
        assert v['state'] == 'established'
        # Verify locat ASNs in bgp sessions
        assert v['local AS'] == int(config_facts['DEVICE_METADATA']['localhost']['bgp_asn'].decode("utf-8"))

    for k, v in config_facts['BGP_NEIGHBOR'].items():
        # Compare the bgp neighbors name with minigraph bgp neigbhors name
        assert v['name'] == bgp_facts['bgp_neighbors'][k]['description']
        # Compare the bgp neighbors ASN with minigraph
        assert int(v['asn'].decode("utf-8")) == bgp_facts['bgp_neighbors'][k]['remote AS']
