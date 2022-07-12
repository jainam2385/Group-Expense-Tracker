from __init__ import *

class Expense(Resource):
    @api.marshal_with(response_model)
    # Add Expense to the Group
    def post(self,groupId):
        if groupId not in groups:
            abort("Group Id not found")
        args=expensePostArguments.parse_args()
        for i in range(len(groups[groupId]['expenses'])):
            if groups[groupId]['expenses'][i]['name']==args['name']:
                abort("Give a different name")
        groups[groupId]['expenses'].append(args)

        # Check for members not in the group and adding them
        n=len(groups[groupId]['expenses'])
        e=groups[groupId]['expenses'][n-1]['paid_by'][0]
        paid_by = convertTodic(e)
        groups[groupId]=addMembers(groups,paid_by,groupId)
        e=groups[groupId]['expenses'][n-1]['paid_for'][0]
        paid_for = convertTodic(e)
        groups[groupId]=addMembers(groups,paid_for,groupId)
        
        # Updating the Balance for the group (Only Paid_by)
        for member in paid_by:
                for gmember in (balances[groupId].items()):
                    if member[1:-1]==gmember[0]:
                        gmember[1]['balance']+=int(paid_by[member])
        return groups[groupId]
    
    # Updating details of an Expense in a Group
    def put(self,groupId,name):
        f=True
        for i in range(len(groups[groupId]['expenses'])):
            if groups[groupId]['expenses'][i]['name']==name:
                f=False
                break
        if f:
            abort("Enter valid name")
        e=groups[groupId]['expenses'][i]['paid_by'][0]
        paid_by = convertTodic(e)
        for member in paid_by:
            for gmember in (balances[groupId].items()):
                if member[1:-1]==gmember[0]:
                    gmember[1]['balance']-=int(paid_by[member])
        
        args=expensePostArguments.parse_args()

        # Check for members not in the group and adding them
        n=len(groups[groupId]['expenses'][i]['paid_by'])
        groups[groupId]['expenses'][i]=args
        e=groups[groupId]['expenses'][i]['paid_by'][n-1]
        paid_by = convertTodic(e)
        groups[groupId]=addMembers(groups,paid_by,groupId)
        e=groups[groupId]['expenses'][i]['paid_for'][n-1]
        paid_for = convertTodic(e)
        groups[groupId]=addMembers(groups,paid_for,groupId)
        for member in paid_by:
                for gmember in (balances[groupId].items()):
                    if member[1:-1]==gmember[0]:
                        gmember[1]['balance']+=int(paid_by[member])

        return groups[groupId]

    # Deleting the group and updating the balance (Only Paid_by)
    def delete(self,groupId,name):
        for i in range(len(groups[groupId]['expenses'])):
            if groups[groupId]['expenses'][i]['name']==name:
                e=groups[groupId]['expenses'][i]['paid_by'][0]
                paid_by = convertTodic(e)
                for member in paid_by:
                    for gmember in (balances[groupId].items()):
                        if member[1:-1]==gmember[0]:
                            gmember[1]['balance']-=int(paid_by[member])
                groups[groupId]['expenses'].pop(i)
                break
        return groups[groupId]
