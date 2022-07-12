from __init__ import *
class Groups(Resource):
    @api.marshal_with(response_model)
    # Get details about a particular group
    def get(self, groupId):
        if groupId not in groups:
            abort("Group Id not found")
        return groups[groupId]
    
    # Add Details to a paricular group
    def post(self,groupId):
        args=groupPostArguments.parse_args()
        if groupId in groups:
            abort("Group Id is taken")
        groups[groupId]={'id':groupId,'name':args['name'],'members':args['members'],'expenses':[]}
        balances[groupId]={}
        for i in range(len(groups[groupId]['members'])):
            balances[groupId][groups[groupId]['members'][i]]={'balance':0,'owes_to':{},'owes_by':{}}
        return groups[groupId]
    
    # Delete a particular groups
    def delete(self,groupId):
        groups.pop(groupId)
        return groups