from rally.benchmark.scenarios import base
from rally.plugins.openstack.scenarios.gbp import utils
import time
class GBPTests(utils.GBPScenario):
    """Bechmark scenarios for Group Based Policy"""

    @base.scenario()
    def test_gbp(self, gbp_args=None):
        self._create_policy_action()
        # Create a policy classifier
        self._create_policy_classifier("web-traffic","tcp", "80", "in")
        time.sleep(120)
        self._delete_policy_classifier("web-traffic")
        self._delete_policy_action()
