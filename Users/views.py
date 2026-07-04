from django.shortcuts import render, redirect, get_object_or_404
from .models import Customer
from django.contrib import messages
from .blockchain import contract, get_customer_from_blockchain, web3 

# Create your views here.
def userhome(request):
    user = request.user
    return render(request, 'User/userhome.html', {'user':user})

def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'User/customer_list.html', {'customers': customers})

def add_customer(request):
    if request.method == 'POST':
        # Get all fields safely
        full_name = request.POST.get('full_name', '').strip()
        date_of_birth = request.POST.get('date_of_birth', '').strip()
        national_id = request.POST.get('national_id', '').strip()
        address = request.POST.get('address', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        kyc_status = request.POST.get('kyc_status', 'Pending').strip()

        # Validation - make sure required fields are not empty
        if not full_name or not date_of_birth or not national_id or not address:
            messages.error(request, "Please fill all required fields.")
            return render(request, 'user/add_customer.html')

        # Step 1: Save to Django DB first
        customer = Customer.objects.create(
            full_name=full_name,
            date_of_birth=date_of_birth,
            national_id=national_id,
            address=address,
            email=email if email else None,
            phone=phone if phone else None,
            kyc_status=kyc_status
        )

        # Step 2: Try saving to Blockchain
        try:
            tx_hash = contract.functions.addCustomer(
                full_name,
                national_id,
                kyc_status,
                "Bank A"  # Example, hardcoded or dynamic later
            ).transact({'from': web3.eth.default_account})

            web3.eth.wait_for_transaction_receipt(tx_hash)

            # Save blockchain transaction hash in the customer record
            customer.blockchain_tx = tx_hash.hex()
            customer.save()

            print("Blockchain Transaction Successful:", tx_hash.hex())
        except Exception as e:
            print("Blockchain Error:", e)
            messages.warning(request, "Customer saved locally, but failed to save on blockchain.")

        messages.success(request, "Customer added successfully.")
        return redirect('customer_list')

    # If GET request, just show the form
    return render(request, 'user/add_customer.html')

def view_blockchain_customer(request, national_id):
    national_id = national_id.strip()
    customer = get_object_or_404(Customer, national_id=national_id)

    blockchain_data = get_customer_from_blockchain(national_id)

    if not blockchain_data or blockchain_data['national_id'] == '':
        context = {
            'error': 'Customer data not found on blockchain.',
            'customer': customer,
            'contract_address': contract.address
        }
    else:
        context = {
            'blockchain_data': blockchain_data,
            'customer': customer,
            'contract_address': contract.address
        }

    return render(request, 'user/blockchain_customer.html', context)

