from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.db import transaction
from .forms import AddTherapistForm
from .models import Therapist, TherapistLogin, TherapistWorkingDay, TimeSlot, WorkingDay
from django.shortcuts import render, redirect,get_object_or_404
from .forms import AddSpecialityForm
from django.contrib import messages
from .models import Speciality
from .forms import AddSpecialityForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from .forms import PrescriptionForm
from appointments.models import Appointment






@transaction.atomic  # Ensures database integrity
def add_new_therapist(request):
    # Initialize a context dictionary to hold any data that needs to be passed to the template
    context = {}
    
    # Check if the request is a POST request
    if request.method == "POST":
        # Initialize the form with POST data
        form = AddTherapistForm(request.POST, request.FILES)
        
        # Validate the form
        if form.is_valid():
            try:
                # Create Therapist but don't save to database yet
                new_therapist = form.save(commit=False)
                new_therapist.save()
                
                # Now save many-to-many relationships
                form.save_m2m()

                # Create a User model for authentication
                user = User.objects.create_user(
                    username=form.cleaned_data['email'],
                    email=form.cleaned_data['email'],
                    password=form.cleaned_data['password1'],
                )

                # Create TherapistLogin to link the Therapist and User models
                TherapistLogin.objects.create(
                    therapist=new_therapist,
                    user=user,
                    profile_photo=form.cleaned_data['profile_photo']
                )

                # Handle the working days and time slots for the therapist
                for day in WorkingDay.objects.all():
                    # Get the time slots from form data for each working day
                    time_slot_str = form.cleaned_data[f'time_slot_{day.day_name}']
                    
                    # If there are time slots for this day
                    if time_slot_str:
                        # Parse and split the time slots
                        time_slots = time_slot_str.split(", ")
                        
                        # Create TherapistWorkingDay object for this therapist and day
                        working_day_rel = TherapistWorkingDay.objects.create(
                            therapist=new_therapist, working_day=day)
                        
                        # Create TimeSlot objects and link to the working day
                        for time in time_slots:
                            start, end = time.split("-")
                            new_time_slot = TimeSlot.objects.create(start_time=start, end_time=end)
                            working_day_rel.time_slots.add(new_time_slot)

                # Redirect to therapist list after successful creation
                return redirect('therapist_list')

            except Exception as e:
                # If there is any error, add it to the context to display it in the template
                context['error'] = str(e)
                # Rollback the transaction in case of any errors
                transaction.rollback()
                
    # If it's a GET request, initialize an empty form
    else:
        form = AddTherapistForm()

    # Add the form to the context
    context['form'] = form
    
    # Render the HTML template and pass the form to it
    return render(request, 'add_new_therapist.html', context)



def add_new_speciality(request):
    # Initialize an empty form and retrieve all existing specialities
    form = AddSpecialityForm()
    specialities = Speciality.objects.all()

    # Check if a POST request has been made
    if request.method == 'POST':
        # Determine the action based on a hidden field in the form
        action = request.POST.get('action')
        
        # Handle 'add' action to add a new speciality
        if action == 'add':
            form = AddSpecialityForm(request.POST)
            if form.is_valid():
                new_speciality = form.save()
                messages.success(request, f'Successfully added {new_speciality.name}.')
                return redirect('add_new_speciality')  # Redirect to clear form
        
        # Handle 'update' action to update an existing speciality
        elif action == 'update':
            speciality_id = request.POST.get('speciality_id')
            speciality = get_object_or_404(Speciality, id=speciality_id)
            form = AddSpecialityForm(request.POST, instance=speciality)
            if form.is_valid():
                form.save()
                messages.success(request, f'Successfully updated {speciality.name}.')
                return redirect('add_new_speciality')  # Redirect to show updated list

        # Handle 'delete' action to delete an existing speciality
        elif action == 'delete':
            speciality_id = request.POST.get('speciality_id')
            Speciality.objects.filter(id=speciality_id).delete()
            messages.success(request, 'Successfully deleted speciality.')
            return redirect('add_new_speciality')  # Redirect to show updated list

    # Render the template with the form and existing specialities
    return render(request, 'add_new_speciality.html', {'form': form, 'specialities': specialities})




def list_therapists(request):
    # Receive query parameters for filtering and pagination
    search_query = request.GET.get('search', '')
    is_active_filter = request.GET.get('is_active', None)
    page_number = request.GET.get('page', 1)
    
    # Create the initial QuerySet
    queryset = Therapist.objects.select_related('branch').prefetch_related('specialities')
    
    # Apply search and filter conditions
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) | 
            Q(branch__name__icontains=search_query) |
            Q(specialities__name__icontains=search_query)
        ).distinct()
    
    if is_active_filter is not None:
        is_active = bool(int(is_active_filter))
        queryset = queryset.filter(is_active=is_active)
        
    # Apply pagination
    paginator = Paginator(queryset, 10)  # Show 10 therapists per page
    therapists = paginator.get_page(page_number)
    
    context = {
        'therapists': therapists,
        'search_query': search_query,
        'is_active_filter': is_active_filter
    }
    
    return render(request, 'therapist_list.html', context)


def get_therapist_profile(request, therapist_id):
    try:
        therapist = Therapist.objects.select_related('branch').prefetch_related('specialities').get(id=therapist_id)
        specialities = [speciality.name for speciality in therapist.specialities.all()]
        profile_data = {
            'name': therapist.name,
            'branch': therapist.branch.name,
            'qualification': therapist.qualification,
            'specialities': specialities,
            'is_active': therapist.is_active,
            # Add other fields as needed
        }
        return JsonResponse(profile_data)
    except Therapist.DoesNotExist:
        return JsonResponse({'error': 'Therapist not found'}, status=404)




def add_prescription(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, initial={
            'appointment': appointment,
        })
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.appointment = appointment
            prescription.therapist = appointment.therapist
            prescription.patient = appointment.patient
            prescription.save()
            messages.success(request, f'Prescription for {prescription.patient} successfully added.')
            return redirect('appointment_detail', appointment_id=appointment.id)
        else:
            messages.error(request, 'There was an error in your form.')
    else:
        form = PrescriptionForm(initial={
            'appointment': appointment,
            'therapist': appointment.therapist,
            'patient': appointment.patient,
        })
    
    return render(request, 'add_prescription.html', {'form': form})




def get_appointment_detail(request, appointment_id):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        appointment_detail = {
            'therapist': appointment.therapist.name,
            'patient': appointment.patient.name,
        }
        return JsonResponse(appointment_detail)
    except Appointment.DoesNotExist:
        return JsonResponse({'error': 'Appointment not found'}, status=404)
