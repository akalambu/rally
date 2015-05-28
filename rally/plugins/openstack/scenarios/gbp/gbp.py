from rally.benchmark.scenarios import base
from rally.plugins.openstack.scenarios.gbp import utils

class GBPTests(utils.GBPScenario):
    """Bechmark scenarios for Group Based Policy"""

    @base.scenario()
    def create_policy_action(self, gbp_args=None):
        self._create_policy_action()
        self._delete_policy_action()
