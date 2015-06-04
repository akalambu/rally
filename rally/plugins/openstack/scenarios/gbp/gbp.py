from rally.benchmark.scenarios import base
from rally.plugins.openstack.scenarios.gbp import utils
import time
from rally.common import utils as rutils
class GBPTests(utils.GBPScenario):
    """Bechmark scenarios for Group Based Policy"""

    @base.scenario()
    def test_gbp(self, gbp_args=None):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,"tcp", "80", "in")
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])
        # Now create a policy target group
        pt_group_name = rutils.generate_random_name(prefix="rally_group_")
        self._create_policy_target_group(pt_group_name)
        # Now update the policy target group
        self._update_policy_target_group(pt_group_name, provided_policy_rulesets=[ruleset_name])
        # Now create a policy target inside the group
        pt_name = rutils.generate_random_name(prefix="rally_target_web1")
        self._create_policy_target(pt_name,pt_group_name)
        # Delete all created resources
        self._delete_policy_target(pt_name)
        self._delete_policy_target_group(pt_group_name)
        self._delete_policy_rule_set(ruleset_name)
        self._delete_policy_rule(rule_name)
        self._delete_policy_classifier(classifier_name)
        self._delete_policy_action(name=action_name)
