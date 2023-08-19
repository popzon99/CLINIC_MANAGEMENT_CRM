from django.shortcuts import render, redirect
from .models import Speciality, WorkingDay, TimeSlot, Therapist, TherapistLogin
from .forms import AddTherapistForm,AddSpecialityForm
from django.shortcuts import render, get_object_or_404

def add_new_therapist(request):
    if request.method == 'POST':
        form = AddTherapistForm(request.POST, request.FILES)
        if form.is_valid():
            # Process the form data and create a new therapist
            therapist = Therapist(
                name=form.cleaned_data['name'],
                address=form.cleaned_data['address'],
                branch=form.cleaned_data['branch'],
                phone=form.cleaned_data['phone'],
                date_of_birth=form.cleaned_data['date_of_birth'],
                gender=form.cleaned_data['gender'],
                slots_per_minute=form.cleaned_data['slots_per_minute'],
                is_active=True,  # New therapist is active by default
                profile_photo=form.cleaned_data['profile_photo']
            )
            therapist.save()

            # Assign selected specialities to the therapist
            therapist.specialities.set(form.cleaned_data['specialities'])

            # Assign working days and time slots to the therapist
            working_days = form.cleaned_data['working_days']
            for day in working_days:
                time_slot_field_name = f'time_slot_{day.day_name}'
                time_slot_value = form.cleaned_data[time_slot_field_name]
                start_time, end_time = time_slot_value.split('-')
                time_slot = TimeSlot(start_time=start_time.strip(), end_time=end_time.strip())
                time_slot.save()
                therapist.time_slots.add(time_slot)
                therapist.working_days.add(day)

            # Create a TherapistLogin instance and link it to the therapist
            therapist_login = TherapistLogin(therapist=therapist)
            therapist_login.save()

            return redirect('physiotherapists:therapist_list') # Redirect to therapist list view

    else:
        form = AddTherapistForm()

    return render(request, 'physiotherapists/add_new_therapist.html', {'form': form})

# You can create other views for listing therapists, adding specialities, profile.



def therapist_list(request):
    therapists = Therapist.objects.all()
    context = {'therapists': therapists}
    return render(request, 'physiotherapists/therapist_list.html', context)





def therapist_profile(request, therapist_id):
    therapist = get_object_or_404(Therapist, id=therapist_id)
    context = {'therapist': therapist}
    return render(request, 'physiotherapists/profile.html', context)


def add_new_speciality(request):
    if request.method == 'POST':
        form = AddSpecialityForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to create a new Speciality instance
            return redirect('physiotherapists:therapist_list')  # Redirect to therapist list or other page
    else:
        form = AddSpecialityForm()
    context = {'form': form}
    return render(request, 'physiotherapists/add_new_speciality.html', context)