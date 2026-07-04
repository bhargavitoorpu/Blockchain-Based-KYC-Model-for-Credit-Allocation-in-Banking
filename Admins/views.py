from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from Users.models import Customer


import os
import pickle
import numpy as np
from django.conf import settings

def adminhome(request):
    users = User.objects.filter(is_staff=False, is_superuser=False) 
    return render(request, "Admin/adminhome.html", {"users": users})

def admin_update_userstatus(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        
        # Toggle the is_active status
        user.is_active = not user.is_active
        user.save()

        # Display message based on the action
        if user.is_active:
            messages.success(request, f"User {user.username} has been activated.")
        else:
            messages.success(request, f"User {user.username} has been deactivated.")
        
        return redirect('adminhome')  # Redirect back to the admin home page
    except User.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect('adminhome')

def customer_lists(request):
    customers = Customer.objects.all().order_by('-created_at')  
    return render(request, 'admin/customer_list.html', {'customers': customers})

def update_kyc_status(request, customer_id):
    customer = get_object_or_404(Customer, id=customer_id)
    customer.kyc_status = 'Verified'
    customer.save()
    return redirect('customer_list')

def predict_loan(request):
    prediction = None
    if request.method == 'POST':
        # Load model and preprocessing objects INSIDE the view
        MODEL_PATH = os.path.join(settings.BASE_DIR, 'model/loan_approval_model.pkl')
        SCALER_PATH = os.path.join(settings.BASE_DIR, 'model/standard_scaler.pkl')
        ENCODER_COLUMNS = ['person_gender', 'person_education', 'person_home_ownership', 'loan_intent', 'previous_loan_defaults_on_file']
        ENCODER_PATHS = {col: os.path.join(settings.BASE_DIR, f'model/{col}_label_encoder.pkl') for col in ENCODER_COLUMNS}

        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)

        label_encoders = {}
        for col, path in ENCODER_PATHS.items():
            with open(path, 'rb') as f:
                label_encoders[col] = pickle.load(f)

        try:
            # Collect input data from POST
            input_data = {
                'person_age': float(request.POST.get('person_age')),
                'person_gender': request.POST.get('person_gender'),
                'person_education': request.POST.get('person_education'),
                'person_income': float(request.POST.get('person_income')),
                'person_emp_exp': int(request.POST.get('person_emp_exp')),
                'person_home_ownership': request.POST.get('person_home_ownership'),
                'loan_amnt': float(request.POST.get('loan_amnt')),
                'loan_intent': request.POST.get('loan_intent'),
                'loan_int_rate': float(request.POST.get('loan_int_rate')),
                'loan_percent_income': float(request.POST.get('loan_percent_income')),
                'cb_person_cred_hist_length': float(request.POST.get('cb_person_cred_hist_length')),
                'credit_score': int(request.POST.get('credit_score')),
                'previous_loan_defaults_on_file': request.POST.get('previous_loan_defaults_on_file')
            }

            # Apply label encoders
            for col in ENCODER_COLUMNS:
                input_data[col] = label_encoders[col].transform([input_data[col]])[0]

            # Prepare final feature array
            numeric_features = ['person_age', 'person_income', 'loan_amnt', 'loan_int_rate',
                                'loan_percent_income', 'cb_person_cred_hist_length', 'credit_score']

            scaled_values = scaler.transform([[input_data[col] for col in numeric_features]])[0]

            # Combine all features
            final_features = list(scaled_values) + [
                input_data['person_gender'],
                input_data['person_education'],
                input_data['person_emp_exp'],
                input_data['person_home_ownership'],
                input_data['loan_intent'],
                input_data['previous_loan_defaults_on_file']
            ]

            final_array = np.array(final_features).reshape(1, -1)

            # Predict
            pred = model.predict(final_array)[0]
            prediction = "Loan Approved" if pred == 1 else "Loan Denied"

        except Exception as e:
            prediction = f"Error in prediction: {str(e)}"

    return render(request, 'admin/predict.html', {'prediction': prediction})
