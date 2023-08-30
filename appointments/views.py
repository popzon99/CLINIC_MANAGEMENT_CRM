# Import necessary modules
from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse
from django.contrib import messages
from django.core.serializers import serialize
from .forms import AppointmentForm
from .models import Appointment
from physiotherapists.models import Therapist
from patients.models import Patient
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.utils import timezone
from calendar import monthrange, monthcalendar
from collections import defaultdict
from datetime import timedelta, date
from collections import defaultdict
from datetime import date
from django.shortcuts import render, redirect






# View function to schedule an appointment
def schedule_appointment(request, patient_id=None):
    # Check if there's a patient_id passed in the URL
    if patient_id:
        # Fetch the patient object using the provided patient_id
        patient = get_object_or_404(Patient, id=patient_id)
        form = AppointmentForm(initial={'patient': patient})
    else:
        form = AppointmentForm()
    
    # Handle AJAX requests for available slots
    if request.is_ajax():
        therapist_id = request.GET.get('therapist_id')
        appointment_date = request.GET.get('appointment_date')
        if therapist_id and appointment_date:
            return get_available_slots(request, therapist_id, appointment_date)
    
    # Handle POST data when the form is submitted
    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save form data but set status to 'Pending'
            new_appointment = form.save(commit=False)
            new_appointment.status = 'Pending'
            new_appointment.save()

            
            # Flash a success message
            messages.success(request, 'Appointment is pending approval.')
            return redirect('receptionist_dashboard')
        else:
            # Flash an error message
            messages.error(request, 'An error occurred. Please try again.')
    
    # Fetch all therapists and serialize the queryset
    therapists = Therapist.objects.all()
    therapists_list = []
    for therapist in therapists:
        therapist_dict = {
            'id': therapist.id,
            'name': therapist.name,
            'working_days': list(therapist.working_days.values_list('weekday_number', flat=True)),  # Assuming working_days is a related field
        }
        therapists_list.append(therapist_dict)

    context = {
        'form': form,
        'therapists': json.dumps(therapists_list),  # Convert list of dictionaries to JSON string
    }

    return render(request, 'schedule_appointment.html', context)


# Function to get available slots
def get_available_slots(request, therapist_id, appointment_date):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    existing_appointments = Appointment.objects.filter(
        therapist=therapist,
        appointment_date=appointment_date,
        status__in=['Pending', 'Accepted']
    )
    booked_slots = [appointment.time_slot.id for appointment in existing_appointments]
    
    # Fetch all available slots for this therapist
    all_slots = list(therapist.time_slots.values('id', 'name'))  # name is a field in time_slot model
    available_slots = []
    
    for slot in all_slots:
        slot_id = slot['id']
        is_booked = slot_id in booked_slots
        available_slots.append({
            'id': slot_id,
            'name': slot['name'],  
            'is_booked': is_booked
        })
    
    # Return the list of available slots as JSON
    return JsonResponse({'available_slots': available_slots})



def list_appointments(request):
    if request.method == 'GET' and request.is_ajax():
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', 'all')

        appointments = Appointment.objects.filter(
            Q(patient__user__first_name__icontains=search_query) |
            Q(therapist__name__icontains=search_query) |
            Q(appointment_date__icontains=search_query)
        )

        # Status Filtering for AJAX
        if status_filter == 'today':
            appointments = appointments.filter(appointment_date=timezone.now().date())
        elif status_filter == 'upcoming':
            appointments = appointments.filter(appointment_date__gt=timezone.now().date())
        elif status_filter == 'cancelled':
            appointments = appointments.filter(status='Cancelled')
        elif status_filter == 'completed':
            appointments = appointments.filter(status='Completed')

        appointments = appointments.values('id', 'patient__user__first_name', 'therapist__name', 'appointment_date', 'status', 'time_slot__name', 'patient__phone')

        return JsonResponse(list(appointments), safe=False)

    else:
        search_query = request.GET.get('search', '')
        status_filter = request.GET.get('status', 'all')
        selected_appointments = request.GET.get('selected_appointments', '')

        appointments = Appointment.objects.select_related('patient', 'therapist', 'time_slot').filter(
            Q(patient__user__first_name__icontains=search_query) |
            Q(therapist__name__icontains=search_query) |
            Q(appointment_date__icontains=search_query)
        )

        # Standard Status Filtering
        if status_filter == 'today':
            appointments = appointments.filter(appointment_date=timezone.now().date())
        elif status_filter == 'upcoming':
            appointments = appointments.filter(appointment_date__gt=timezone.now().date())
        elif status_filter == 'cancelled':
            appointments = appointments.filter(status='Cancelled')
        elif status_filter == 'completed':
            appointments = appointments.filter(status='Completed')

        paginator = Paginator(appointments, 10)
        page_number = request.GET.get('page')
        page_appointments = paginator.get_page(page_number)

        context = {
            'appointments': page_appointments,
            'search_query': search_query,
            'status_filter': status_filter
        }

        return render(request, 'listing_appointments.html', context)



# Function to delete an appointment
def delete_appointment(request, appointment_id):
    # Check if the request method is POST
    if request.method == "POST":
        try:
            # Fetch the appointment object to be deleted
            appointment = get_object_or_404(Appointment, id=appointment_id)

            # You can add authorization checks here. For example:
            # if request.user != appointment.patient.user and not request.user.is_staff:
            #     return HttpResponseForbidden("You don't have permission to delete this appointment.")
            
            appointment.delete()
            
            # Flash a success message
            messages.success(request, 'Appointment deleted successfully.')
        except Exception as e:
            # Flash an error message
            messages.error(request, f"An error occurred: {e}")
        return redirect('list_appointments')  # Change to your listing view name
    else:
        return HttpResponseForbidden("Invalid method.")


def calendar_view(request):
    selected_month = request.GET.get('month', timezone.now().month)
    selected_year = request.GET.get('year', timezone.now().year)

    try:
        selected_month = int(selected_month)
        selected_year = int(selected_year)
    except ValueError:
        return redirect('calendar_view')

    if selected_month < 1 or selected_month > 12 or selected_year < 1900 or selected_year > 3000:
        return redirect('calendar_view')

    first_day = date(selected_year, selected_month, 1)
    last_day_of_month = monthrange(selected_year, selected_month)[1]
    last_day = date(selected_year, selected_month, last_day_of_month)

    appointments_this_month = Appointment.objects.filter(appointment_date__range=(first_day, last_day))

    appointment_count_by_day = defaultdict(int)
    for appointment in appointments_this_month:
        appointment_count_by_day[appointment.appointment_date.day] += 1

    today = timezone.now().date()
    appointments_today = Appointment.objects.filter(appointment_date=today)

    calendar_data = monthcalendar(selected_year, selected_month)

    context = {
        'appointment_count_by_day': appointment_count_by_day,
        'appointments_today': appointments_today,
        'today': today,
        'calendar_data': calendar_data,
        'selected_month': selected_month,
        'selected_year': selected_year,
    }

    return render(request, 'calendar_view.html', context)
