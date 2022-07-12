from __init__ import *

class Balance(Resource):
    """
    Method:
    1) Create a deepcopy of the balances dictionary (new_balances)
    2) Create a dictionary which stores the total expenditure for each member in the mentioned group (paid_for_final)
    3) Subtract that total expenditure from the new_balances dictionary and update paid_for_final[member] to abs(new_balances[member]) 
       if new_balances[member]<0 else paid_for_final[member]=0
    4) Traverse the dictionary and subtract the balance if balance of a member greater than 0. Update owes_by
    5) Traverse the dictionary again to update owes_to
    6) Lastly update the total balance for each member by adding owes_to and owes_by 
    """

    def get(self,groupId):
        # Step 1
        # print(balances)
        new_balances=copy.deepcopy(balances)
        n=len(groups[groupId]['expenses'])
        paid_for_final={}

        # Step 2
        for i in range(n):
            e=groups[groupId]['expenses'][i]['paid_for'][0]
            paid_for = convertTodic(e)
            for member in paid_for:
                if member[1:-1] not in paid_for_final:
                    paid_for_final[member[1:-1]]=int(paid_for[member])
                else:
                    paid_for_final[member[1:-1]]+=int(paid_for[member])

        # Step 3
        for member in paid_for_final:
            for gmember in (new_balances[groupId].items()):
                if member==gmember[0]:
                    gmember[1]['balance']-=paid_for_final[member]
                    if gmember[1]['balance']>=0:
                        paid_for_final[member]=0
                        continue
                    paid_for_final[member]=abs(gmember[1]['balance'])

        # Step 4
        for member in paid_for_final:
            if paid_for_final[member]!=0:
                for gmember in (new_balances[groupId].items()):
                    if gmember[1]['balance']>=0:
                        if gmember[1]['balance']>=paid_for_final[member]:
                            gmember[1]['balance']-=paid_for_final[member]
                            gmember[1]['owes_by'][member]=paid_for_final[member]
                            paid_for_final[member]=0
                            break
                        else:
                            gmember[1]['owes_by'][member]=gmember[1]['balance']
                            paid_for_final[member]-=gmember[1]['balance']
                            gmember[1]['balance']=0

        # Step 5
        for gmember in (new_balances[groupId].items()):
            for borrower in (gmember[1]['owes_by'].items()):
                for member in (new_balances[groupId].items()):
                    if borrower[0]==member[0]:
                        member[1]['owes_to'][gmember[0]]=-borrower[1]

        # Step 6
        for gmember in (new_balances[groupId].items()):
            total=0
            for member in (gmember[1]['owes_by'].items()):
                total+=member[1]
            
            for member in (gmember[1]['owes_to'].items()):
                total+=member[1]
            
            gmember[1]['balance']=total

        return new_balances[groupId]
