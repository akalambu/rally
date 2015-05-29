from rally.benchmark.scenarios import base
from rally import osclients
import os
@osclients.Clients.register("gbp")
def gbp(self):
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
       self.clients("gbp").create_policy_action(body)

   @base.atomic_action_timer("gbp.delete_policy_action")
   def _delete_policy_action(self, name="allow"):
       """
       Delete a policy action
       Lookup the policy action using the name
       """
       for i in range(10):
           policy_id = self._find_policy_actions(name)
           if policy_id:
               print "Deleting policy action %s" %(policy_id)
               self.clients("gbp").delete_policy_action(policy_id)
               return
       print "Policy action %s not found" %(name)
       return

   def _find_policy_actions(self,name):
       """
       Find a policy action given its name
       """
       actions = self.clients("gbp").list_policy_actions()
       for policy in actions['policy_actions']:
           if policy['name'] == name:
               return policy['id']
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
       self.clients("gbp").create_policy_classifier(body)

   @base.atomic_action_timer("gbp.delete_policy_classifier")
   def _delete_policy_classifier(self, name):
       for i in range(10):
           classifier_id = self._find_policy_classifier(name)
           if classifier_id:
               print "Deleting classifier id %s" %(classifier_id)
               self.clients("gbp").delete_policy_classifier(classifier_id)
      	       return
       print "Policy classifier %s is not found" %(name)
       return
 
   def _find_policy_classifier(self, name):
       """
       Find a policy classifier given its name
       """
       classifiers = self.clients("gbp").list_policy_classifiers()
       for classifier in classifiers["policy_classifiers"]:
           if classifier['name'] == name:
               return classifier['id']
       return None
