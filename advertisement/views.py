from django.shortcuts import render, redirect
from .models import Advertisement, AdvertisementImage
from .forms import AdvertisementForm
from django.contrib.auth.decorators import login_required


@login_required
def create_ad_view(request):
    """Create new advertisement view"""
    if request.method == 'POST':
        form = AdvertisementForm(request.POST)
        images = request.FILES.getlist('images')
        if form.is_valid():
            new_ad = Advertisement.objects.create(
                title=form.cleaned_data['title'],
                user=request.user,
                description=form.cleaned_data['description']
            )
            for image in images:
                AdvertisementImage.objects.create(
                    advertisement=new_ad,
                    image=image
                )
            return redirect('home')
    else:
        form = AdvertisementForm()
    context = {
        'form': form,
    }
    return render(request, 'advertisement/advertisement_create.html', context)
