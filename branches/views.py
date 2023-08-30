from django.shortcuts import render, redirect, get_object_or_404
from .models import Branch
from .forms import BranchForm, AddBranchForm

def branches(request):
    branches_list = Branch.objects.all()
    context = {'branches_list': branches_list}
    return render(request, 'branches/branches.html', context)

def update_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)

    if request.method == 'POST':
        form = BranchForm(request.POST, instance=branch)
        if form.is_valid():
            form.save()
            return redirect('branches')
    else:
        form = BranchForm(instance=branch)

    context = {'form': form, 'branch': branch}
    return render(request, 'branches/update_branch.html', context)

def delete_branch(request, pk):
    branch = get_object_or_404(Branch, pk=pk)

    if request.method == 'POST':
        branch.delete()
        return redirect('branches')

    context = {'branch': branch}
    return render(request, 'branches/delete_branch.html', context)

def add_branch(request):
    if request.method == 'POST':
        form = AddBranchForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('branches')
    else:
        form = AddBranchForm()

    context = {'form': form}
    return render(request, 'branches/add_branch.html', context)
