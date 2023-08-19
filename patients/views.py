from django.shortcuts import render, redirect
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from io import BytesIO
from .models import Patient
from .forms import AddPatientForm, PatientFilterForm
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def add_new_patient(request):
    if request.method == 'POST':
        form = AddPatientForm(request.POST, request.FILES)
        if form.is_valid():
            patient = form.save(commit=False)

            # Process additional fields or logic here

            patient.save()
            return redirect('patient_list')  # Redirect to patient list view
    else:
        form = AddPatientForm()

    context = {'form': form}
    return render(request, 'patients/add_new_patient.html', context)

def patient_list(request):
    patients = Patient.objects.all()

    # Patient filtering
    form = PatientFilterForm(request.GET)
    if form.is_valid():
        gender = form.cleaned_data.get('gender')
        if gender:
            patients = patients.filter(gender=gender)

        location = form.cleaned_data.get('location')
        if location:
            patients = patients.filter(location=location)

        # Apply the logic for the first feature (latest patients)
        latest_count = form.cleaned_data.get('latest_count')
        if latest_count:
            patients = patients.order_by('-id')[:latest_count]

    # Export patients to Excel
    if 'export_excel' in request.GET:
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename="patient_list.xlsx"'
        wb = Workbook()
        ws = wb.active
        ws.title = "Patient List"

        # Write headers
        headers = ["Name", "Address", "Gender", "Date of Birth", "Phone", "Location"]
        for col_num, header_title in enumerate(headers, 1):
            col_letter = get_column_letter(col_num)
            ws[f"{col_letter}1"] = header_title
            ws.column_dimensions[col_letter].width = 15

        # Write data
        for row_num, patient in enumerate(patients, 2):
            ws[f"A{row_num}"] = patient.name
            ws[f"B{row_num}"] = patient.address
            ws[f"C{row_num}"] = patient.gender
            ws[f"D{row_num}"] = patient.date_of_birth
            ws[f"E{row_num}"] = patient.phone
            ws[f"F{row_num}"] = patient.location.name

        output = BytesIO()
        wb.save(output)
        output.seek(0)
        response.write(output)
        return response

    # Pagination
    paginator = Paginator(patients, 10)  # Show 10 patients per page
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    context = {
        'patients': patients,
        'form': form,
    }
    return render(request, 'patients/patient_list.html', context)


def patient_profile(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    context = {'patient': patient}
    return render(request, 'patients/patient_profile.html', context)



# ... Previous imports ...

def update_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    form = AddPatientForm(instance=patient)

    if request.method == 'POST':
        form = AddPatientForm(request.POST, request.FILES, instance=patient)
        if form.is_valid():
            patient = form.save()
            return redirect('patient_list')

    context = {'form': form, 'patient': patient}
    return render(request, 'patients/update_patient.html', context)

def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)

    if request.method == 'POST':
        patient.delete()
        return redirect('patient_list')

    context = {'patient': patient}
    return render(request, 'patients/delete_patient.html', context)
