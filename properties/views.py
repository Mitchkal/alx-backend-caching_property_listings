#!/usr/bin/env python3
from django.views.decorators.cache import cache_page
from .models import Property
from django.http import JsonResponse

@cache_page(60 * 15)
def property_list(request):
    properties = Property.Objects.all()
    return JsonResponse({'data': list(properties)}, safe=False)
    # return render(request, 'properties/property_list.html', {'properties': properties})

# Create your views here.
