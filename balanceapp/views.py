from django.shortcuts import render, redirect
from .models import Bank, Transaction
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from decimal import Decimal

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful.")
                return redirect('add_transaction')  # Redirect to dashboard after login
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid form submission.")
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

# Dashboard View
def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login
    banks = Bank.objects.filter(user=request.user)
    transactions = Transaction.objects.filter(bank__user=request.user).order_by('-date')[:10]
    context = {
        'banks': banks,
        'transactions': transactions,
    }
    return render(request, 'dashboard.html', context)

# Add Bank View
def add_bank(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login
    if request.method == 'POST':
        bank_name = request.POST.get('bank_name')
        account_number = request.POST.get('account_number')
        balance = request.POST.get('balance')

        if bank_name and account_number and balance:
            Bank.objects.create(
                user=request.user,
                bank_name=bank_name,
                account_number=account_number,
                balance=float(balance),
            )
            return redirect('dashboard')
        else:
            return render(request, 'add_bank.html', {'error': 'All fields are required!'})

    return render(request, 'add_bank.html')

# Add Transaction View
def add_transaction(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect unauthenticated users to login
    if request.method == 'POST':
        bank_id = request.POST.get('bank')
        transaction_type = request.POST.get('type')
        amount = request.POST.get('amount')
        description = request.POST.get('description')

        if bank_id and transaction_type and amount:
            try:
                bank = Bank.objects.get(id=bank_id, user=request.user)
                amount = Decimal(amount)  # Convert the amount to a Decimal

                if transaction_type == 'credit':
                    bank.balance += amount  # Add amount to the balance
                elif transaction_type == 'debit':
                    if bank.balance < amount:
                        return render(request, 'add_transaction.html', {'error': 'Insufficient balance!'})
                    bank.balance -= amount  # Subtract amount from the balance
                bank.save()

                # Create a new transaction record
                Transaction.objects.create(
                    bank=bank,
                    type=transaction_type,
                    amount=amount,
                    description=description,
                )
                return redirect('dashboard')
            except Bank.DoesNotExist:
                return render(request, 'add_transaction.html', {'error': 'Invalid bank selected!'})
        else:
            return render(request, 'add_transaction.html', {'error': 'All fields are required!'})

    banks = Bank.objects.filter(user=request.user)
    return render(request, 'add_transaction.html', {'banks': banks})

# Logout View
def user_logout(request):
    logout(request)  # Logs out the user
    messages.success(request, "You have been logged out successfully.")  # Optional: Display logout success message
    return redirect('login')