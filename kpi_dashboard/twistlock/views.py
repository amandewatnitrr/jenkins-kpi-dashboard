from django.shortcuts import render
from .models import Twistlock

def twistlock_view(request):
    # Fetch data from the Twistlock model
    twistlock_data = Twistlock.objects.all()

    # Prepare data for the template
    context = {
        'twistlock_data': twistlock_data,
    }

    # Pass data to the template
    return render(request, "twistlock/Twistlock.html", context)
