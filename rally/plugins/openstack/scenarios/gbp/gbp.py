from rally.benchmark.scenarios import base
from rally.plugins.openstack.scenarios.gbp import utils
import time
from rally.common import utils as rutils
class GBPTests(utils.GBPScenario):
    """Benchmark scenarios for Group Based Policy"""
    
    @base.scenario(context={"cleanup":["grouppolicy"]})
    def create_policy_action(self, action_type="allow"):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name, type=action_type)
        
    @base.scenario()
    def create_and_delete_policy_action(self, action_type="allow"):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name, type=action_type)
        self._delete_policy_action(name=action_name)
    
    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_policy_classifier(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_")
        self._create_policy_classifier(classifier_name, classifier_args['protocol'], classifier_args['port_range'],
                                      classifier_args['direction'])

    @base.scenario()
    def create_and_delete_policy_classifier(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_")
        self._create_policy_classifier(classifier_name, classifier_args['protocol'], classifier_args['port_range'],
                                      classifier_args['direction'])
        self._delete_policy_classifier(classifier_name)
        self._delete_policy_action(name=action_name)
    
    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_policy_rule(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol'], classifier_args['port_range'],
                                       classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
    
    
    @base.scenario()
    def create_and_delete_policy_rule(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol'], classifier_args['port_range'],
                                       classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        self._delete_policy_rule(rule_name)
        self._delete_policy_classifier(classifier_name)
        self._delete_policy_action(name=action_name)
    
    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_policy_rule_set(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol'],
                                       classifier_args['port_range'], classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])

    
    @base.scenario()
    def create_and_delete_policy_rule_set(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol'],
                                       classifier_args['port_range'], classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])
        self._delete_policy_rule_set(ruleset_name)
        self._delete_policy_rule(rule_name)
        self._delete_policy_classifier(classifier_name)
        self._delete_policy_action(name=action_name)
    
    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_policy_target_group(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol']
                                       , classifier_args['port_range'], classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])
        # Now create a policy target group
        pt_group_name = rutils.generate_random_name(prefix="rally_group_")
        self._create_policy_target_group(pt_group_name)
    
    @base.scenario()
    def create_and_delete_policy_target_group(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name,classifier_args['protocol']
                                       , classifier_args['port_range'], classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])
        # Now create a policy target group
        pt_group_name = rutils.generate_random_name(prefix="rally_group_")
        self._create_policy_target_group(pt_group_name)
        self._delete_policy_target_group(pt_group_name)
        self._delete_policy_rule_set(ruleset_name)
        self._delete_policy_rule(rule_name)
        self._delete_policy_classifier(classifier_name)
        self._delete_policy_action(name=action_name)
    
    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_and_update_policy_target_group(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name, classifier_args['protocol'],
                                       classifier_args['port_range'], classifier_args['direction'])
        # Now create a policy rule
        rule_name = rutils.generate_random_name(prefix="rally_rule_web_policy_")
        self._create_policy_rule(rule_name, classifier_name, action_name)
        # Now create a policy rule set
        ruleset_name = rutils.generate_random_name(prefix="rally_ruleset_web_")
        self._create_policy_rule_set(ruleset_name, [rule_name])
        # Now create a policy target group
        pt_group_name = rutils.generate_random_name(prefix="rally_group_")
        self._create_policy_target_group(pt_group_name)
        self._update_policy_target_group(pt_group_name, provided_policy_rulesets=[ruleset_name])


    @base.scenario(context={"cleanup": ["grouppolicy"]})
    def create_policy_target(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name, classifier_args['protocol'],
                                       classifier_args['port_range'], classifier_args['direction'])
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


    
    @base.scenario()
    def create_and_delete_policy_target(self, classifier_args={}):
        action_name = rutils.generate_random_name(prefix="rally_action_allow_")
        self._create_policy_action(name=action_name)
        # Create a policy classifier
        classifier_name = rutils.generate_random_name(prefix="rally_classifier_web_traffic_")
        self._create_policy_classifier(classifier_name, classifier_args['protocol'],
                                       classifier_args['port_range'], classifier_args['direction'])
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
