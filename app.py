from flask import Flask, render_template, request

app = Flask(__name__)

def safe_float(value):
    """Converts a string to float, returning 0.0 if empty or invalid."""
    try:
        return float(value) if value.strip() else 0.0
    except ValueError:
        return 0.0

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if request.method == 'GET':
        return render_template('calculator.html') 
    elif request.method == 'POST':
        taxable_income = safe_float(request.form.get('taxable-income', '0'))
        mortgage_interest = safe_float(request.form.get('mortgage-interest', '0'))
        student_loan = safe_float(request.form.get('student-loan', '0'))
        medical_expenses = safe_float(request.form.get('medical-expenses', '0'))
        charity = safe_float(request.form.get('charity', '0'))
        property_taxes = safe_float(request.form.get('property-taxes', '0'))
        retirement = safe_float(request.form.get('retirement', '0'))
        self_employment = safe_float(request.form.get('self-employment', '0'))

        filing_status = request.form.get('filing-status', 'single')
        is_senior = request.form.get('senior') == 'on'

        # Standard deductions
        standard_deductions = {'single': 14600, 'married': 29200, 'head': 21900}
        senior_deductions = {'single': 1950, 'married': 1550, 'head': 1550}  # Fixed for Head of Household

        deduction = standard_deductions.get(filing_status, 14600)
        if is_senior:
            deduction += senior_deductions.get(filing_status, 0)

        # Itemized deductions
        itemized_deductions = mortgage_interest + student_loan + charity + property_taxes + retirement + self_employment

        # Medical expenses deduction (Only exceeding 7.5% of AGI)
        medical_threshold = taxable_income * 0.075
        if medical_expenses > medical_threshold:
            itemized_deductions += (medical_expenses - medical_threshold)

        itemized_deductions = min(itemized_deductions, 10000)  # SALT limit

        # Use the greater of standard deduction or itemized deductions
        total_deduction = max(deduction, itemized_deductions)

        # Calculate taxable income after deductions
        taxable_after_deductions = max(0, taxable_income - total_deduction)


        result={
            'taxableIncome': taxable_income,
            'totalDeductions': total_deduction,
            'finalTaxableIncome': taxable_after_deductions
        }
        return render_template('calculator.html', result=result) 

if __name__ == '__main__':
    app.run(debug=True)

# from flask import Flask, render_template, request

# app = Flask(__name__)

# def safe_float(value):
#     """Converts a string to float, returning 0.0 if empty or invalid."""
#     try:
#         return float(value) if value.strip() else 0.0
#     except ValueError:
#         return 0.0

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/calculate', methods=['GET', 'POST'])
# def calculate():
#     # deduction_result = None
#     if request.method == 'GET':
#         return render_template('calculator.html') 
#     elif request.method == 'POST':
            
#             # deduction=0
#             taxable_income = safe_float(request.form.get('taxable-income','0'))
#             mortgage_interest = safe_float(request.form.get('mortgage-interest','0'))
#             student_loan = safe_float(request.form.get('student-loan','0'))
#             medical_expenses = safe_float(request.form.get('medical-expenses','0'))
#             charity = safe_float(request.form.get('charity','0'))
#             property_taxes = safe_float(request.form.get('property-taxes','0'))
#             retirement = safe_float(request.form.get('retirement','0'))
#             self_employment = safe_float(request.form.get('self-employment','0'))
#             # retirement = float(user_inputs['retirement']) if user_inputs['retirement'] else 0
#             # self_employment = float(user_inputs['self-employment']) if user_inputs['self-employment'] else 0

#             filing_status = request.form.get('filing-status', 'single')
#             is_senior = request.form.get('senior') == 'on'

#             # Standard deductions based on filing status
#             standard_deductions = {'single': 14600, 'married': 29200, 'head': 21900}
#             senior_deductions = {'single': 1950, 'married': 1550}

#             deduction = standard_deductions.get(filing_status, 14600)
#             if is_senior:
#                 deduction += senior_deductions.get(filing_status, 0)

#             # Calculate total itemized deductions
#             itemized_deductions = mortgage_interest + student_loan + charity + property_taxes + retirement + self_employment

#             # Medical expenses deduction (Only exceeding 7.5% of AGI)
#             medical_threshold = taxable_income * 0.075
#             if medical_expenses > medical_threshold:
#                 itemized_deductions += (medical_expenses - medical_threshold)

#             itemized_deductions = min(itemized_deductions, 10000)  # SALT limit

#             # Use the greater of standard deduction or itemized deductions
#             total_deduction = max(deduction, itemized_deductions)

#             # Calculate taxable income after deductions
#             taxable_after_deductions = max(0, taxable_income - total_deduction)

#             return render_template('calculator.html', result={
#             'taxableIncome': taxable_income,
#             'totalDeductions': total_deduction,
#             # 'educationLoanInterest': education_loan_interest,
#             'finalTaxableIncome': taxable_after_deductions
#         })
            

# if __name__ == '__main__':
#     app.run(debug=True)
