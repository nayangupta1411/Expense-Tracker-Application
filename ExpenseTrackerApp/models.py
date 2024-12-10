from Database.database import db
import pandas as pd
import bson
import plotly.graph_objects as go
from datetime import datetime

class Expense:

    def __init__(self):
        return
    
    def current_month():
        current_date=datetime.now()
        return current_date.month
    
    def current_month_name(num):
        arr=["January", "February", "March", "April", "May", "June",
              "July", "August", "September", "October", "November", "December"]
        return arr[num-1]



    def show_all_expense():
        show_expenses=db.addExpense.find()
        expense_arr=[{**expense, "_id":str(expense["_id"])} for expense in show_expenses]
        return expense_arr[::-1]
    
    def monthly_expense(expense_arr,month):
        # print('models expense_arr-->',expense_arr)
        month_expense={'Medical':{'total':0,'times':[]},
                       'Grocery': {'total':0,'times':[]},
                       'Vehicle': {'total':0,'times':[]},
                       'Rent': {'total':0,'times':[]},
                       'House Allowance': {'total':0,'times':[]},
                       'Other': {'total':0,'times':[]},
                         }
        for i in expense_arr:
          if str(int(i['addDate'].split('-')[1]))==str(month):
                try:
                    month_expense[i['addCategory']]['total']+=int(i['addExpense'])
                    month_expense[i['addCategory']]['times']+=[{'Date':i['addDate'],'Expense':i['addExpense']}]
                except:
                    month_expense[i['addCategory']]={'total':int(i['addExpense']), 'times': [{'Date':i['addDate'],'Expense':i['addExpense']}]}
        return month_expense
    
    def deleteExpense(id):
        exp=db.addExpense.delete_one({"_id": bson.ObjectId(id)})
        expense_arr=Expense.show_all_expense()
        return expense_arr

    def updateExpense(id):
        expense=db.addExpense.find({"_id": bson.ObjectId(id)})
        selected_expense=[{**expense, "_id":str(expense["_id"])} for expense in expense]
        print("itexpense-->",selected_expense)
        return selected_expense

    def total_monthly_expense(expense_of_month):
        total=0
        for key,value in expense_of_month.items():
            total+=int(value['total'])
        # print('total expense-->',total)
        return total
    
    def yearly_expense_category():
        yearly_expense_category=dict()
        for i in range(12):
            yearly_expense_category[i]=Expense.monthly_expense(Expense.show_all_expense(),i+1)
        # print('yearly_expense_category --->',yearly_expense_category)
        df=pd.DataFrame(yearly_expense_category)
        return df
    
    def Medical():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[0].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def Grocery():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[1].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def Vehicle():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[2].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def Rent():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[3].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def House_Allowance():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[4].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def Other():
        df=Expense.yearly_expense_category()
        medicalDf=pd.DataFrame(df.iloc[5].to_dict())
        return medicalDf.iloc[0].tolist()
    
    def yearly_chart():
        categories = ['Jan', 'Feb', 'March', 'April','May','June','July','Aug','Sept','Oct','Nov','Dec']
        medical = Expense.Medical()
        grocery = Expense.Grocery()
        vehicle = Expense.Vehicle()
        rent=Expense.Rent()
        house_allowance=Expense.House_Allowance()
        other=Expense.Other()
        
        fig = go.Figure()
 
    # Add bars to the figure
        fig.add_trace(go.Bar(x=categories, y=medical, name='Medical',
                         hovertemplate='Expense: %{y}', marker=dict(color='#003f5c')))
        fig.add_trace(go.Bar(x=categories, y=grocery, name='Grocery',
                         hovertemplate='Expense: %{y}', marker=dict(color='#58508d')))
        fig.add_trace(go.Bar(x=categories, y=vehicle, name='Vehicle',
                         hovertemplate='Expense: %{y}', marker=dict(color='#bc5090')))
        fig.add_trace(go.Bar(x=categories, y=rent, name='Rent',
                         hovertemplate='Expense: %{y}', marker=dict(color='#ff6361')))
        fig.add_trace(go.Bar(x=categories, y=house_allowance, name='House Allowance',
                         hovertemplate='Expense: %{y}', marker=dict(color='#ffa600')))
        fig.add_trace(go.Bar(x=categories, y=other, name='Other',
                         hovertemplate='Expense: %{y}', marker=dict(color='#b35900')))
    # Update layout
        fig.update_layout(
        title="yearly epxense with categories",
        xaxis_title="Categories",
        yaxis_title="Expenses",
        barmode='stack',  # Stack the bars
        plot_bgcolor='rgba(240, 240, 240, 1)',  # Set background color
        margin=dict(l=50, r=100, t=50, b=50),  # Adjust the margins
        height=400
        )
 
    # Convert the figure to HTML
        graph_html = fig.to_html(full_html=False)
        return graph_html
    
    def monthly_chart(expense_arr,month): 

        monthly_expense=Expense.monthly_expense(expense_arr,month)
        monthlyDF=pd.DataFrame(monthly_expense)

        categories = ['Medical','Grocery','Vehicle','Rent','House Allowance','Other']
        values = monthlyDF.iloc[0].tolist()
        print("models values-->",values)
        

        fig=go.Figure()
        fig.add_trace(go.Bar(
                x=categories,
                y=values,
                name='',
                hovertemplate='%{x} Expense: %{y}',
                marker=dict(color=['#003f5c', '#58508d', '#bc5090', '#ff6361','#ffa600','#b35900'])
            ))
        
    
        fig.update_layout(
        title="monthly epxense with categories",
        xaxis_title="Categories",
        yaxis_title="Expenses",
        plot_bgcolor='rgba(240, 240, 240, 1)',  # Set background color
        margin=dict(l=50, r=100, t=50, b=50),  # Adjust the margins
        height=400
        )

        graph_html=fig.to_html(full_html=False)

        # plt.figure(figsize=(9, 4))
        # plt.bar(categories, values, color=['#003f5c', '#58508d', '#bc5090', '#ff6361','#ffa600','#b35900'])
        # plt.title('monthly epxense with categories')
        # plt.xlabel('Categories')
        # plt.ylabel('Expenses')

        # img = io.BytesIO()
        # plt.savefig(img, format='png')
        # img.seek(0)
    
        # Encode the BytesIO object in base64
        # img_base64 = base64.b64encode(img.getvalue()).decode('utf8')
        return graph_html




