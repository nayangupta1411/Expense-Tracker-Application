from flask import Flask, render_template,request
from flask_cors import CORS
import bson
from Database.database import db
from models import Expense

app = Flask(__name__)

CORS(app)

@app.route('/')
def index():
    current_month=Expense.current_month()
    expense_arr=Expense.show_all_expense()
    month_expense=Expense.monthly_expense(expense_arr,current_month)
    # print('month_expense on index-->',month_expense)
    active_section='add_expense'
    return render_template("index.html",result = expense_arr, current_month=current_month,month_expense=month_expense,active_section=active_section)
  

# add expense api

@app.route('/addExpense', methods=['POST','GET'])
def addExpense():
    if request.method == 'POST':
        result = request.form.to_dict()
        # print('res--',result)
        add_item=db.addExpense.insert_one(
            {
                'addDate': result.get("addDate"),
            'addCategory': result.get("addCategory"),
             'addExpense': result.get("addExpense"),
         'addDescription': result.get("addDescription")

            }
        )
        arr=Expense.show_all_expense()
        active_section='add_expense'

    return render_template('index.html',result=arr,active_section=active_section)


# add expense page view
@app.route('/add_expense')
def add_expense():
    active_section='add_expense'
    return render_template("index.html",active_section=active_section)

#recent expense page view
@app.route('/recent_expense')
def recent_expense():
    recent_expense=Expense.show_all_expense()
    active_section='recent_expense'
    return render_template('index.html',result=recent_expense,active_section=active_section)



month_expense=dict()
@app.route('/monthSelect/<selected_option>', methods=['POST','GET'])
def monthSelect(selected_option):
    expense_arr=Expense.show_all_expense()
    month_expense=Expense.monthly_expense(expense_arr,selected_option)
    # print('select res--',selected_option) 
    month=Expense.current_month_name(int(selected_option))
    total_expense=Expense.total_monthly_expense(month_expense)
    active_section='monthly_expense'
    return render_template("index.html",month_expense=month_expense,active_section=active_section,currentMonth=month,total_expense=total_expense)


@app.route('/monthly_expense',methods=['POST','GET'])
def monthly_expense():
    global month_expense
    current_month=Expense.current_month()
    expense_arr=Expense.show_all_expense()
    # print("current expense-->",expense_arr)
    default_month_expense=Expense.monthly_expense(expense_arr,current_month)
    expense_of_month=dict()
    if month_expense:
        expense_of_month=month_expense
    else:
        expense_of_month=default_month_expense
    # print('month_expense-->',expense_of_month)
    total_expense=Expense.total_monthly_expense(expense_of_month)
    # print('total_expense in main file-->',total_expense)
    active_section='monthly_expense'
    return render_template("index.html",month_expense=expense_of_month,active_section=active_section,current_month=current_month,total_expense=total_expense)


@app.route("/visualize_expense",methods=['POST','GET'])
def visualize_expense():

    graph_html=Expense.yearly_chart()
    chartViewSelect='Yearly'
    active_section='visualize_expense'
    return render_template("index.html", graph_html=graph_html,active_section=active_section,selected_option=chartViewSelect)

@app.route('/chartView/<selected_option>',methods=['POST','GET'])
def chartView(selected_option):
    # print("chartView selected_option--",selected_option)
    chartViewSelect=['Yearly','Monthly'][int(selected_option)-1]
    month=Expense.current_month()
    month_name=Expense.current_month_name(int(month))
    expense_arr=Expense.show_all_expense()
    if chartViewSelect=='Yearly':
        graph_html=Expense.yearly_chart()
    if chartViewSelect=='Monthly':
        graph_html=Expense.monthly_chart(expense_arr,month)
    active_section='visualize_expense'
    # return render_template("visualizeExpense.html",selected_option=selected_option)
    return render_template("index.html",selected_option=chartViewSelect,active_section=active_section,graph_html=graph_html,selected_month_option=month_name)

@app.route('/monthChartView/<option>',methods=['POST','GET'])
def monthChartView(option):
    print("monthChartView option--",option)
    expense_arr=Expense.show_all_expense()
    graph_html=Expense.monthly_chart(expense_arr,option)
    month_name=Expense.current_month_name(int(option))
    active_section='visualize_expense'
    return render_template("index.html",selected_option='Monthly',selected_month_option=month_name,active_section=active_section,graph_html=graph_html)

@app.route('/deleteExpense/<users_id>',methods=['POST','GET'])
def deleteExpense(users_id):
    print("users_id-->",users_id)
    new_recent_expense=Expense.deleteExpense(users_id)
    # if request.method == 'POST':
    #     result = request.get_data()
    #     print("delete res-->",result)
    active_section='recent_expense'
    return render_template('index.html',result=new_recent_expense,active_section=active_section)


@app.route('/updateExpense/<user_id>',methods=['POST','GET'])
def updateExpense(user_id):
    print("user-->",user_id)
    expense=Expense.updateExpense(user_id)
    print("main expense--->",expense)
    return render_template('updateExpense.html',expense=expense)

@app.route('/newUpdatedExpense/<user_id>',methods=['POST','GET'])
def newUpdatedExpense(user_id):
    if request.method == 'POST':
        result = request.form.to_dict()
        # print('res--',result)
        update_item=db.addExpense.update_one({"_id":  bson.ObjectId(user_id)}, { "$set" :
            {
                'addDate': result.get("addDate"),
            'addCategory': result.get("addCategory").split()[0],
             'addExpense': result.get("addExpense"),
         'addDescription': result.get("addDescription")

            }
            }
        )
        recent_expense=Expense.show_all_expense()
        active_section='recent_expense'
    return render_template('index.html',result=recent_expense,active_section=active_section) 

if __name__ == '__main__':

    app.run(debug=True)