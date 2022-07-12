# Group Expense Tracker

## Getting Started with the project

1. **Install Libraries** -The first step after cloning the repository is installing the libraries from requirements.txt `pip install -r requirements.txt`

2. **Run the project**- To start the server run the command `python app.py` in the command line.

3. **Run Testcase**- A testcase file is available. 

## How to

**Create a Group-** <br>
`
http://127.0.0.1:5000/groups/<int:groupId>
`

JSON Structure
`
{
"name": "",
"members": []
}
`

<br>

**View a Group/ Groups** 
<br>

View all Groups- 
`
http://127.0.0.1:5000/groups
`

View a single Group-
`
http://127.0.0.1:5000/groups/<int:groupId>
`

<br>

**Add/Update an expense**  <br>

Add Link-
`http://127.0.0.1:5000/addexpense/<int:groupId>
`

Update Link-
`
http://127.0.0.1:5000/updateexpense/<int:groupId>/<string:ExpenseName>
`

JSON Structure <br>
`
  {
    "name": "",
    "value": ,
    "paid_by": {},
    "paid_for": {}
  }
`
<br>
<br>

**Delete an Expense** <br>
Link- 
`
http://127.0.0.1:5000/deleteexpense/<int:groupId>/<string:ExpenseName>
`

<br>

**View Balance** <br>
Link-
`
http://127.0.0.1:5000/balance/<int:groupId>
`
