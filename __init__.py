from array import array
from ast import Delete
from importlib.metadata import files
from typing import List
from attr import field
from flask import Flask,jsonify,json
from flask_restx import Resource, Api, reqparse, abort,marshal,fields,Namespace
import collections
import copy

app=Flask(__name__)
api=Api(app)

# Dictionaries where all the details will be stored
expense={}
balances={}
groups={}


# Expense Model for storing the details about the Expenses
expense['name']=fields.String(attribute='name')
expense['value'] = fields.Integer(attribute='value')
expense['paid_by']=fields.Raw()
expense['paid_for']=fields.Raw()
expenses = api.model("expense", expense)


# Group model which stores the details about the groups and extends the expense model
response_model = api.model('response',{
    'id':fields.Integer(),
    'name': fields.String(),
    'members':fields.List(fields.String()),
    'expenses': fields.List(fields.Nested(expenses)),
})

# Take the JSON data sent from the user    
groupPostArguments= reqparse.RequestParser()
groupPostArguments.add_argument("name",type=str,help="Name is required",required=True)
groupPostArguments.add_argument("members", action='append')

expensePostArguments=reqparse.RequestParser()
expensePostArguments.add_argument("name",type=str,required=True,help="Enter a name")
expensePostArguments.add_argument("value",type=int,required=True,help="Enter the amount")
expensePostArguments.add_argument("paid_by",action='append')
expensePostArguments.add_argument("paid_for",action='append')


# Function to add members to the group which are previously not in the group
def addMembers(groups,res,groupId):
    for member in res:
        if member[1:-1] not in groups[groupId]['members']:
            groups[groupId]['members'].append(member[1:-1])
            balances[groupId][member[1:-1]]={'balance':0,'owes_to':{},'owes_by':{}}
    return groups[groupId]

# Function to convert string to dictionary
def convertTodic(s):
    return {sub.split(":")[0]: sub.split(":")[1] for sub in s[1:-1].split(", ")}