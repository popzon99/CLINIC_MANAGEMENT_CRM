from django.shortcuts import render, redirect
from .models import Branch

def branches(request):
    branches_list = Branch.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        is_working = request.POST.get('is_working') == 'on'

        Branch.objects.create(
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            is_working=is_working
        )
        return redirect('branches')

    context = {'branches_list': branches_list}
    return render(request, 'superadmin/branches.html', context)

def update_branch(request, pk):
    branch = Branch.objects.get(pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        is_working = request.POST.get('is_working') == 'on'

        branch.name = name
        branch.email = email
        branch.address = address
        branch.phone_number = phone_number
        branch.is_working = is_working
        branch.save()

        return redirect('branches')

    context = {'branch': branch}
    return render(request, 'branches/update_branch.html', context)

def delete_branch(request, pk):
    branch = Branch.objects.get(pk=pk)
    
    if request.method == 'POST':
        branch.delete()
        return redirect('branches')

    context = {'branch': branch}
    return render(request, 'branches/delete_branch.html', context)

def add_branch(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        is_working = request.POST.get('is_working') == 'on'

        Branch.objects.create(
            name=name,
            email=email,
            address=address,
            phone_number=phone_number,
            is_working=is_working
        )
        return redirect('branches')

    return render(request, 'branches/add_branch.html')
