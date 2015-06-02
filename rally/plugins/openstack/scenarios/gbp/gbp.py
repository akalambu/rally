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
        # Now create a policy rule 
        self._create_policy_rule("web-policy-rule", "web-traffic", "allow")
        # Now create a policy rule set
        self._create_policy_rule_set("web-ruleset", ["web-policy-rule"])
        # Now create a policy target group
        self._create_policy_target_group("web")
        # Now update the policy target group
        self._update_policy_target_group("web", provided_policy_rulesets=["web-ruleset"])
        # Now create a policy target inside the group
        self._delete_policy_target_group("web")
        self._delete_policy_rule_set("web-ruleset")
        self._delete_policy_rule("web-policy-rule")
        self._delete_policy_classifier("web-traffic")
        self._delete_policy_action()
