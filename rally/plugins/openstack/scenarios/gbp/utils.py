from rally.benchmark.scenarios import base
from rally import osclients
import os
import time

@osclients.Clients.register("grouppolicy")
def grouppolicy(self):
	from gbpclient.v2_0 import client as gbpclient
	return gbpclient.Client(username=self.endpoint.username,
							password=self.endpoint.password,
							tenant_name=self.endpoint.tenant_name,
							auth_url=self.endpoint.auth_url)

class GBPScenario(base.Scenario):
	"""
	Base class for GBP scenarios
	"""
	@base.atomic_action_timer("gbp.create_policy_action")
	def _create_policy_action(self, name="allow", type="allow"):
		body = {
			"policy_action": {
			"name": name,
			"action_type": type
			}
		}
		self.clients("grouppolicy").create_policy_action(body)

	@base.atomic_action_timer("gbp.delete_policy_action")
	def _delete_policy_action(self, name="allow"):
		"""
		Delete a policy action
		Lookup the policy action using the name
		"""
		policy_id = self._find_policy_actions(name)
		if policy_id:
			self.clients("grouppolicy").delete_policy_action(policy_id)
			return
		print "Policy action %s not found" %(name)
		return

	def _find_policy_actions(self,name):
		"""
		Find a policy action given its name
		Lookup 10 second interval
		"""
		for i in range(10):
			actions = self.clients("grouppolicy").list_policy_actions()
			for policy in actions['policy_actions']:
				if policy['name'] == name:
					return policy['id']
			time.sleep(1)
		return None
	
	@base.atomic_action_timer("gbp.create_policy_classifier")
	def _create_policy_classifier(self, name, protocol, port_range, direction):
		body = {
			"policy_classifier": {
				"name": name,
				"protocol": protocol,
				"port_range": port_range,
				"direction": direction
			}
		}
		self.clients("grouppolicy").create_policy_classifier(body)

	@base.atomic_action_timer("gbp.delete_policy_classifier")
	def _delete_policy_classifier(self, name):
		classifier_id = self._find_policy_classifier(name)
		if classifier_id:
			self.clients("grouppolicy").delete_policy_classifier(classifier_id)
			return
		print "Policy classifier %s is not found" %(name)
		return

	def _find_policy_classifier(self, name):
		"""
		Find a policy classifier given its name
		"""
		for i in range(10):
			classifiers = self.clients("grouppolicy").list_policy_classifiers()
			for classifier in classifiers["policy_classifiers"]:
				if classifier['name'] == name:
					return classifier['id']
			time.sleep(1)
		return None

	@base.atomic_action_timer("gbp.create_policy_rule")
	def _create_policy_rule(self, policy_name, classifier_name, action_name):
		body = {
			"policy_rule": {
				"policy_actions": [self._find_policy_actions(action_name)],
				"policy_classifier_id": self._find_policy_classifier(classifier_name),
				"name": policy_name
			}
		}
		self.clients("grouppolicy").create_policy_rule(body)

	def _find_policy_rule(self, name):
		"""
		Find a policy rule given its name
		"""
		for i in range(10):
			rules = self.clients("grouppolicy").list_policy_rules()
			for rule in rules["policy_rules"]:
				if rule['name'] == name:
					return rule['id']
			time.sleep(1)
		return None

	@base.atomic_action_timer("gbp.delete_policy_rule")
	def _delete_policy_rule(self, name):
		policy_rule_id = self._find_policy_rule(name)
		if policy_rule_id:
			self.clients("grouppolicy").delete_policy_rule(policy_rule_id)
			return
		print "Policy rule %s not found" %(name)
		return
	
	@base.atomic_action_timer("gbp.create_policy_rule_set")
	def _create_policy_rule_set(self, ruleset_name, rules_list):
		ruleid_list = []
		for rule in rules_list:
			ruleid_list.append(self._find_policy_rule(rule))
		
		# Now create the policy rule set
		body = {
			"policy_rule_set": {
				"name": ruleset_name,
				"policy_rules": ruleid_list
			}
		}
		self.clients("grouppolicy").create_policy_rule_set(body)
	
	def _find_policy_rule_set(self, name):
		"""
		Find a policy rule set given its name
		"""
		for i in range(10):
			rule_set = self.clients("grouppolicy").list_policy_rule_sets()
			for ruleset in rule_set["policy_rule_sets"]:
				if ruleset['name'] == name:
					return ruleset['id']
			time.sleep(1)
		return None
	
	@base.atomic_action_timer("gbp.delete_policy_rule_set")
	def _delete_policy_rule_set(self, name):
		policy_ruleset_id = self._find_policy_rule_set(name)
		if policy_ruleset_id:
			self.clients("grouppolicy").delete_policy_rule_set(policy_ruleset_id)
			return
		print "Policy rule set %s not found" %(name)
		return
	
	@base.atomic_action_timer("gbp.create_policy_target_group")
	def _create_policy_target_group(self, name):
		body = {
			"policy_target_group": {
				"name": name
			}
		}
		self.clients("grouppolicy").create_policy_target_group(body)
		
	def _find_policy_target_group(self, name):
		"""
		Find a policy target group given the name
		"""
		for i in range(10):
			groups = self.clients("grouppolicy").list_policy_target_groups()
			for group in groups["policy_target_groups"]:
				if group['name'] == name:
					return group['id']
			time.sleep(1)
		return None
	
	@base.atomic_action_timer("gbp.delete_policy_target_group")
	def _delete_policy_target_group(self, name):
		group_id = self._find_policy_target_group(name)
		if group_id:
			self.clients("grouppolicy").delete_policy_target_group(group_id)
			return
		print "Policy target group %s not found" %(name)
		return
	
	@base.atomic_action_timer("gbp.update_policy_target_group")
	def _update_policy_target_group(self, group_name, consumed_policy_rulesets=None, provided_policy_rulesets=None):
		# Lookup the group id from the group name
		group_id =  self._find_policy_target_group(group_name)
		consumed_dict = {}
		provided_dict = {}
		if consumed_policy_rulesets:
			for ruleset in consumed_policy_rulesets:
				id = self._find_policy_rule_set(ruleset)
				consumed_dict[id] = "scope"
		if provided_policy_rulesets:
			for ruleset in provided_policy_rulesets:
				id = self._find_policy_rule_set(ruleset)
				provided_dict[id] = "scope"
		
		body = {
			"policy_target_group" : {
				"provided_policy_rule_sets" : provided_dict,
				"consumed_policy_rule_sets" : consumed_dict
			}
		}
		self.clients("grouppolicy").update_policy_target_group(group_id, body)
	
	@base.atomic_action_timer("gbp.create_policy_target")
	def _create_policy_target(self, name, group_name):
		# Lookup the group id first
		group_id = self._find_policy_target_group(group_name)
		body = {
			"policy_target": {
				"policy_target_group_id": group_id,
				"name": name
			}
		}
		self.clients("grouppolicy").create_policy_target(body)
	
	def _find_policy_target(self, name):
		for i in range(10):
			targets = self.clients("grouppolicy").list_policy_targets()
			for target in targets["policy_targets"]:
				if target['name'] == name:
					return target['id']
			time.sleep(1)
		return None
	
	@base.atomic_action_timer("gbp.delete_policy_target")
	def _delete_policy_target(self, name):
		target_id = self._find_policy_target(name)
		if target_id:
			self.clients("grouppolicy").delete_policy_target(target_id)
			return
		print "Policy target %s not found" %(name)
		return
