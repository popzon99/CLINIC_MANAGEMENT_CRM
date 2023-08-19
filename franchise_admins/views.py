from django.shortcuts import render, redirect, get_object_or_404
from .forms import FranchiseAdminForm
from .models import FranchiseAdmin

def franchise_admins_list(request):
    franchise_admins = FranchiseAdmin.objects.all()
    return render(request, 'franchise_admins/franchise_admins_list.html', {'franchise_admins': franchise_admins})

def view_franchise_admin(request, admin_id):
    franchise_admin = get_object_or_404(FranchiseAdmin, pk=admin_id)
    return render(request, 'franchise_admins/view_franchise_admin.html', {'franchise_admin': franchise_admin})

def add_franchise_admin(request):
    if request.method == 'POST':
        form = FranchiseAdminForm(request.POST)
        if form.is_valid():
            # Create and save a new franchise admin
            franchise_admin = FranchiseAdmin(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                phone=form.cleaned_data['phone'],
                branch=form.cleaned_data['branch'],
                role=form.cleaned_data['role'],
                password=form.cleaned_data['password'],
                is_active=form.cleaned_data['is_active']
            )
            franchise_admin.save()
            return redirect('franchise-admins-list')
    else:
        form = FranchiseAdminForm()
    return render(request, 'franchise_admins/add_franchise_admin.html', {'form': form})

# Implement update and delete views similar to add_franchise_admin

# ... other imports ...

def update_franchise_admin(request, admin_id):
    franchise_admin = get_object_or_404(FranchiseAdmin, pk=admin_id)

    if request.method == 'POST':
        form = FranchiseAdminForm(request.POST)
        if form.is_valid():
            # Update and save the franchise admin
            franchise_admin.name = form.cleaned_data['name']
            franchise_admin.email = form.cleaned_data['email']
            franchise_admin.phone = form.cleaned_data['phone']
            franchise_admin.branch = form.cleaned_data['branch']
            franchise_admin.role = form.cleaned_data['role']
            franchise_admin.password = form.cleaned_data['password']
            franchise_admin.is_active = form.cleaned_data['is_active']
            franchise_admin.save()
            return redirect('franchise-admins-list')
    else:
        initial_data = {
            'name': franchise_admin.name,
            'email': franchise_admin.email,
            'phone': franchise_admin.phone,
            'branch': franchise_admin.branch,
            'role': franchise_admin.role,
            'is_active': franchise_admin.is_active,
            # Other initial data
        }
        form = FranchiseAdminForm(initial=initial_data)
    
    return render(request, 'franchise_admins/update_franchise_admin.html', {'form': form, 'franchise_admin': franchise_admin})

def delete_franchise_admin(request, admin_id):
    franchise_admin = get_object_or_404(FranchiseAdmin, pk=admin_id)
    
    if request.method == 'POST':
        # Delete the franchise admin
        franchise_admin.delete()
        return redirect('franchise-admins-list')
    
    return render(request, 'franchise_admins/delete_franchise_admin.html', {'franchise_admin': franchise_admin})

