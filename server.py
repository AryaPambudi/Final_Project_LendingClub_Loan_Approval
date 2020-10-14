from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import seaborn as sb
import plotly
import plotly.graph_objs as go
import mysql.connector
# Data dari flask di kirim ke browser dalam bentuk json
import json
import joblib

app = Flask(__name__)

def sql() :
    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Karepenyong1?'
    )
    c = con.cursor()
    q1 = 'USE data'
    c.execute(q1)
    q2 = 'SELECT * FROM data.lendingclub_loan'
    c.execute(q2)
    res = c.fetchall()
    LendingClub = pd.DataFrame(res, columns=c.column_names)
    con.commit()
    return LendingClub

@app.route('/')
def start():
    return render_template('signin.html')

@app.route('/signin', methods=["POST"])
def signin():
    input = request.form
    Username = input['Username']
    Password = input['Password']
    if Username == "Arya" and Password == "Karepenyong1" :
        return render_template('home.html')
    else :
        return render_template('signin.html')

@app.route('/home')
def home():
    return render_template('home.html')
# Render Picture
@app.route('/static/<path:x>')
def gal(x):
    return send_from_directory("static",x)

# Render About page
@app.route('/about')
def about():
    return render_template('about.html')

# # # # # # # # # #
# HISTOGRAM & BOX #
# # # # # # # # # #

def category_plot(cat_plot = 'histplot', cat_x = 'term', cat_y = 'loan_amnt', estimator ='count', hue='loan_status'):
    
    LCL = sql()
    if cat_plot == 'histplot':
        data = []

        for val in LCL[hue].unique(): # [No, Yes]
            hist = go.Histogram(
                        x = LCL[LCL[hue] == val ][cat_x],
                        y = LCL[LCL[hue] == val ][cat_y],
                        histfunc=estimator,
                        name= val
                    )
            
            data.append(hist)

        title = 'Histogram'
    else :
        data = []

        for val in LCL[hue].unique(): # [No, Yes]
            hist = go.Box(
                        x = LCL[LCL[hue] == val ][cat_x],
                        y = LCL[LCL[hue] == val ][cat_y],
                        name= val
                    )
            
            data.append(hist)

        title = 'Box'

    if title == 'Histogram' and estimator == 'count' :
        ytitle = 'Borrowers'
    else :
        ytitle = cat_y

    layout = go.Layout(
        title=title,
        title_x=0.5,
        xaxis={"title" : cat_x},
        yaxis={"title" : ytitle},
        boxmode='group'
    )

    final = {"data" : data, "layout" : layout}

    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/index')
def index():
    plot = category_plot()

    # list dropdown
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('term', 'Term'), ('loan_status', 'Loan Status')]
    list_y = [('loan_amnt', 'Loan Amount'), ('int_rate', 'Interest Rate'), ('annual_inc', 'Annual Income'), ('revol_bal', 'Revolving Balance')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]

    return render_template(
        'category.html', 
        plot=plot, 
        focus_plot='histplot', 
        focus_x='term', 
        focus_y='loan_amnt', 
        focus_estimator='count',
        focus_hue='loan_status',
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_estimator,
        drop_hue = list_x
    )

@app.route('/cat_fn')
def cat_fn():
    cat_plot = request.args.get('cat_plot') # histplot
    cat_x = request.args.get('cat_x') # NewExist
    cat_y = request.args.get('cat_y') # Term
    estimator = request.args.get('estimator') # avg
    hue = request.args.get('hue') # MIS_Status

    # Ketika kita klik menu 'Histogram & Box' di Navigasi
    if cat_plot == None and cat_x == None and cat_y == None and estimator == None and hue == None:
        cat_plot = 'histplot'
        cat_x = 'term'
        cat_y = 'loan_amnt'
        estimator = 'count'
        hue = 'loan_status'

    # Ketika kita pindah dari boxplot (disabled) ke histogram
    if estimator == None:
        estimator = 'count'

    # Ketika kita pindah dari histogram ke boxplot
    # saat estimator count, dropdown menu sumbu Y di disabled dan memberikan nilai None
    if cat_y == None:
        cat_y = "loan_amnt"

    plot = category_plot(cat_plot, cat_x, cat_y, estimator, hue)

    # list dropdown
    list_plot = [('histplot', 'Histogram'), ('boxplot', 'Box')]
    list_x = [('term', 'Term'), ('loan_status', 'Loan Status')]
    list_y = [('loan_amnt', 'Loan Amount'), ('int_rate', 'Interest Rate'), ('annual_inc', 'Annual Income'), ('revol_bal', 'Revolving Balance')]
    list_estimator = [('count', 'Count'), ('sum', 'Sum'),('avg','Average'), ('min', 'Minimum'), ('max', 'Maximum')]
                                                                                            
    return render_template(
        'category.html', 
        plot=plot, 
        focus_plot=cat_plot, 
        focus_x=cat_x, 
        focus_y=cat_y, 
        focus_estimator=estimator,
        focus_hue = hue,
        drop_plot = list_plot,
        drop_x = list_x,
        drop_y = list_y,
        drop_estimator = list_estimator,
        drop_hue = list_x
    )


# # # # # #
# SCATTER # 
# # # # # #

def scatter_plot(cat_x, cat_y, hue):

    LCL = sql()
    data = []

    for val in LCL[hue].unique() : 
        scatt = go.Scatter(
            x=LCL[LCL[hue] == val][cat_x],
            y=LCL[LCL[hue] == val][cat_y],
            mode='markers',
            name = val
        )

        data.append(scatt)

    # membuat layout, nama variable tidak harus 'layout'
    layout = go.Layout(
        title='Scatter',
        title_x= 0.5,
        xaxis = dict(title=cat_x),
        yaxis = dict(title=cat_y)
    )

    # Gabungkan antara plot dengan layout
    # variable yang menyimpan dictionary tidak harus final
    # dict harus memiliki key 'data' dan 'layout
    res = {"data" : data, "layout" : layout}

    # hasil json yang akan dikirim tidak harus menggunakan 'graphJSON'
    graphJSON = json.dumps(res, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/scatt_fn')
def scatt_fn():
    # Memilih dari menu dropdown
    # Keduanya akan bernilai None hanya ketika kita mengunjungi via 'Scatter' menu di navbar
    cat_x = request.args.get('cat_x')
    cat_y = request.args.get('cat_y')
    hue = request.args.get('hue')

    # Jika kita klick menu 'Scatter' pada navbar, keduanya akan bernilai None
    if cat_x == None and cat_y == None:
        cat_x = 'loan_amnt'
        cat_y = 'annual_inc'
        hue = 'loan_status'

    list_x = [('loan_amnt', 'Loan Amount'), ('int_rate', 'Interest Rate'), ('annual_inc', 'Annual Income'), ('revol_bal', 'Revolving Balance')]
    list_hue = [('term', 'Term'), ('loan_status', 'Loan Status')]

    plot = scatter_plot(cat_x, cat_y, hue)
    
    # Kirim ke browser
    return render_template(
        'scatter.html', 
        plot=plot,
        drop_x=list_x,
        drop_y=list_x,
        drop_hue=list_hue, 
        focus_x=cat_x, 
        focus_y=cat_y,
        focus_hue=hue
    )


# # # #
# PIE #
# # # #

def pie_plot(hue):

    # result : list of tupple dari penghitungan banyak data secara unique 
    LCL = sql()
    result = LCL[hue].value_counts()

    labels_source = []
    values_source = []

    for item in result.iteritems():
        labels_source.append(item[0])
        values_source.append(item[1])

    data_source = [
        go.Pie(
            labels=labels_source,
            values=values_source
        )
    ]

    layout_source = go.Layout(
        title='Pie',
        title_x=0.5
    )

    final = {"data" : data_source, "layout" : layout_source}

    # hasil json yang akan dikirim tidak harus menggunakan 'graphJSON'
    graphJSON = json.dumps(final, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/pie_fn')
def pie_fn():
    hue_source = request.args.get('hue')

    # Saat diakses melalui link, hue_sorce akan bernilai None
    if hue_source == None:
        hue_source = 'loan_status'

    list_hue = [('term', 'Term'), ('loan_status', 'Loan Status')]

    plot_source = pie_plot(hue_source)

    return render_template(
        'pie.html', 
        plot=plot_source, 
        focus_hue=hue_source,
        drop_hue=list_hue)

# Prediction Page
@app.route('/predict')
def predict():
    return render_template('predict.html')

# Result Page
@app.route('/LendingClub_Loan_Result', methods=["POST"])
def LendingClub_Loan_predict():
    input = request.form
    loan_amnt = float(input['Loan_Amount'])
    int_rate = float(input['Interest_Rate'])
    annual_inc = float(input['Annual_Income'])
    revol_bal = float(input['Revolving_Balance'])
    term = input['Term']
    if term == '1':
        term_cat = '60 Months '
    else:
        term_cat = '36 Months'

# Term, NewExist, GrAppv, SBA_Appv, RevLineCr, Lowdoc, NAICS_11 DIRUBAH
    pred_proba = gbc_smo.predict_proba([[loan_amnt, term, int_rate, annual_inc, revol_bal]])

    if pred_proba[0][1] < 0.703496022411385 :
        pred = 0
        prob = pred_proba[0][0]
    else :
        pred = 1
        prob = pred_proba[0][1]
        
    pred_and_prob = f"{round(prob*100,2)}% {'APPROVED' if pred == 1 else 'DENIED'}"

    return render_template('result.html',
    data=input, prediction=pred_and_prob, loan_amnt=input['Loan_Amount'], 
    int_rate=input['Interest_Rate'], annual_inc=input['Annual_Income'],
    revol_bal=input['Revolving_Balance'], term=term_cat)


    
@app.route('/inputdata')
def data():
    LCL = sql()
    n = [a for a in range(len(LCL))]
    list_loan_amnt = LCL['loan_amnt']
    list_int_rate = LCL['int_rate']
    list_annual_inc = LCL['annual_inc']
    list_loan_status = LCL['loan_status']
    list_revol_bal = LCL['revol_bal']
    list_term = LCL['term']
    return render_template('input.html', n=n, list_loan_amnt=list_loan_amnt, list_int_rate=list_int_rate,
                            list_annual_inc=list_annual_inc, list_loan_status=list_loan_status,
                            list_revol_bal=list_revol_bal, list_term=list_term)

@app.route('/input', methods=["POST"])
def inputdata():
    input = request.form
    loan_amnt = float(input['Loan_Amount'])
    int_rate = float(input['Interest_Rate'])
    annual_inc = float(input['Annual_Income'])
    revol_bal = float(input['Revolving_Balance'])
    term = input['Term']
    if term == '1':
        term_cat = '60 months'
    else:
        term_cat = '36 months'
    loan_status = input['Loan_Status']
    if loan_status == '1':
        loan_status_cat = 'Fully Paid'
    else:
        loan_status_cat = 'Charged Off'

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Karepenyong1?'
    )
    c = con.cursor()
    q1 = "USE data"
    c.execute(q1)
    q2 = "SELECT MAX(lendingclub_loan.index) FROM data.lendingclub_loan"
    c.execute(q2)
    res = c.fetchall()
    row_index = int(res[0][0])
    q3 = f"INSERT INTO data.lendingclub_loan values({row_index+1},{loan_amnt},'{term_cat}',{int_rate},{annual_inc},'{loan_status_cat}',{revol_bal})"
    c.execute(q3)
    con.commit()
    q4 = "SELECT * FROM data.lendingclub_loan"
    c.execute(q4)
    res = c.fetchall()
    LendingClub = pd.DataFrame(res, columns=c.column_names)
    
    LCL = LendingClub
    n = [a for a in range(len(LCL))]
    list_loan_amnt = LCL['loan_amnt']
    list_int_rate = LCL['int_rate']
    list_annual_inc = LCL['annual_inc']
    list_loan_status = LCL['loan_status']
    list_revol_bal = LCL['revol_bal']
    list_term = LCL['term']
    return render_template('input.html', n=n, list_loan_amnt=list_loan_amnt, list_int_rate=list_int_rate,
                            list_annual_inc=list_annual_inc, list_loan_status=list_loan_status,
                            list_revol_bal=list_revol_bal, list_term=list_term)

@app.route('/delete', methods=["POST"])
def delete():
    input = request.form
    row = int(input['Row'])

    con = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='Karepenyong1?'
    )
    c = con.cursor()
    q1 = "USE data"
    c.execute(q1)
    q2 = "SELECT * FROM data.lendingclub_loan"
    c.execute(q2)
    res = c.fetchall()
    LendingClub = pd.DataFrame(res, columns=c.column_names)

    if 0 < row <= len(LendingClub) :
        row = LendingClub['index'].iloc[row-1]
        q3 = f"DELETE FROM lendingclub_loan WHERE lendingclub_loan.index = {row}"
        c.execute(q3)
        con.commit()
        q4 = "SELECT * FROM data.lendingclub_loan"
        c.execute(q4)
        res = c.fetchall()
        LendingClub = pd.DataFrame(res, columns=c.column_names)

    LCL = LendingClub
    n = [a for a in range(len(LCL))]
    list_loan_amnt = LCL['loan_amnt']
    list_int_rate = LCL['int_rate']
    list_annual_inc = LCL['annual_inc']
    list_loan_status = LCL['loan_status']
    list_revol_bal = LCL['revol_bal']
    list_term = LCL['term']

    return render_template('input.html', n=n, list_loan_amnt=list_loan_amnt, list_int_rate=list_int_rate,
                            list_annual_inc=list_annual_inc, list_loan_status=list_loan_status,
                            list_revol_bal=list_revol_bal, list_term=list_term)


if __name__ == '__main__':
    gbc_smo = joblib.load('gbc_smo_LendingClub_Loan')
    app.run(debug=True, port=4000)