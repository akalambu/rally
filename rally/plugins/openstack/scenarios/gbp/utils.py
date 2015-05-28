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
       policy_id = self._find_policy_actions(name)
       if policy_id:
           self.clients("gbp").delete_policy_action(policy_id)
       else:
           print "Policy action not found *********"

   def _find_policy_actions(self,name):
       """
       Find a policy action given its name
       """
       actions = self.clients("gbp").list_policy_actions()
       for policy in actions['policy_actions']:
           if policy['name'] == name:
               return policy['id']
       return None
    
