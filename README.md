# Final_Project_LendingClub_Loan_Approval


by: Arya Pambudi Bayuaji

Dataset: lending_club_loan_two.csv [gdrive](https://drive.google.com/file/d/1k0HmRq5JCOgU2ctKphxypd9UGNMwIFfS/view?usp=sharing)

*The dataset is separate from the repository because it exceeds github file size limit.


Source : [kaggle](https://www.kaggle.com/prashdash112/lending-club-loan-two-new-version)



PROJECT DESCRIPTION
---

The dataset is from the LendingClub Company

LendingClub is an American peer-to-peer lending company, headquartered in San Francisco, California. It was the first peer-to-peer lender to register its offerings as securities with the Securities and Exchange Commission (SEC), and to offer loan trading on a secondary market. LendingClub is the world's largest peer-to-peer lending platform. The company claims that $15.98 billion in loans had been originated through its platform up to December 31, 2015.

LendingClub enables borrowers to create unsecured personal loans between $1,000 and $40,000. The standard loan period is three years. Investors can search and browse the loan listings on LendingClub website and select loans that they want to invest in based on the information supplied about the borrower, amount of loan, loan grade, and loan purpose. Investors make money from interest. LendingClub makes money by charging borrowers an origination fee and investors a service fee.

From the LendingClub dataset. We can learn that around 20% of loans guaranteed by the LendingClub have a financial problem. If this condition happens with a big frequency and amount of loan, it can reduce the interest of investors to invest money and borrowers to owe money and also resulting in reduced corporate profits because borrowers and investors are also reduced.

In this final project, I will build a Flask-based web app that can recommend whether the personal loan is approved or not based on the given term and loan condition. The project's main mission is to reduce the risk of charge off credit loans for LendingClub company. 


PROJECT GOALS
---

The goal of the project is to reduce the risk of charge off credit loans for LendingClub company by making machine learning-based applications to determine the loan request based on historical data. 

APPS
---

SIGNIN
---
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/sign_in.PNG)

HOMEPAGE
---
Home interface:
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/home.PNG)

About interface:
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/about.PNG)

PREDICTION PAGE 
---
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/predict.PNG)

The application user can input data as described below:
- `laon_amnt`    : The listed amount of the loan applied for by the borrower.
- `term`         : The number of payments on the loan. Values are in months and can be either 36 or 60.
- `int_rate`     : Interest Rate on the loan
- `annual_inc`   : The self-reported annual income provided by the borrower during registration.
- `revol_bal`    : Total credit revolving balance

PREDICTION RESULT
---
The prediction result interface:
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/result.PNG)

VISUALISATION PAGE
---
Histogram
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/histogram.PNG)

Boxplot
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/boxplot.PNG)

Scatter Plot
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/scatter.PNG)

Pie Chart
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/pie.PNG)

DATA PAGE 
---
Data Table
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/data%20table.PNG)

Input & Delete Data
![](https://github.com/AryaPambudi/Final_Project_LendingClub_Loan_Approval/blob/main/Interface/input%20and%20delete%20data.PNG)
