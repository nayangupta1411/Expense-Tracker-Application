from pymongo import MongoClient 
from flask_pymongo import PyMongo

DATABASE_BASE='mongodb://localhost:27017/'
print('database--',DATABASE_BASE)

client=MongoClient("mongodb://localhost:27017/")
expenseTrackerDB=client["expenseTrackerDB"]
# addExpense=expenseTrackerDB.create_collection('addExpense')
# mydict=addExpense.insert_one({'addDate':'2024-11-08',
#                               'addCategory':'car',
#                               'addExpense':'2000',
#                               'addDescription':'Service'})
print('client-',client.list_database_names())
db=client.expenseTrackerDB
# show_expenses=db.addExpense.find()
# arr=[{**item, "_id":str(item["_id"])} for item in show_expenses]
# print('show_expenses',arr)
