from __init__ import *
from groups import Groups
from expenses import Expense
from balances import Balance

# Get details about all the groups


class GroupsList(Resource):
    def get(self):
        return groups


api.add_resource(Groups, '/groups/<int:groupId>')
api.add_resource(GroupsList, '/groups')
api.add_resource(Expense, '/addexpense/<int:groupId>')
api.add_resource(Expense, '/deleteexpense/<int:groupId>/<string:name>')
api.add_resource(Expense, '/updateexpense/<int:groupId>/<string:name>')
api.add_resource(Balance, '/balance/<int:groupId>')

if __name__ == '__main__':
    app.run(debug=True)
