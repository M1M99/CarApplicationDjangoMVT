from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Listing, ListingStatus, STATUS_CHOICES
from .forms import ListingForm, ListingImageFormSet


# Create your views here.

def listing_list(request):
    qs=Listing.objects.filter(status=ListingStatus.APPROVED)

    q=request.GET.get('q') or ''
    city=request.GET.get('city') or ''
    brand=request.GET.get('brand') or ''
    minp=request.GET.get('min_price') or ''
    maxp=request.GET.get('max_price') or ''

    if q:
        qs=qs.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(model__icontains=q) | Q(brand__icontains=q))

    if city:
        qs=qs.filter(city__iexact=city)

    if brand:
        qs=qs.filter(brand__iexact=brand)

    if minp.isdigit():
        qs=qs.filter(price__gte=int(minp))

    if maxp.isdigit():
        qs=qs.filter(price__lte=int(maxp))

    context={
        'listings':qs.select_related('owner')[:100],
        'q':q,'city':city,'brand':brand,'minp':minp,'maxp':maxp
    }

    return render(request,'listings/listing_list.html',context)

def listing_detail(request,slug):
    listing=get_object_or_404(Listing,slug=slug)
    return render(request,'listings/listing_detail.html',{'listing':listing})

@login_required
def listing_create(request):
    if request.method=='POST':
        form = ListingForm(request.POST,request.FILES)
        formset=ListingImageFormSet(request.POST,request.FILES,instance=Listing())

        if form.is_valid() and formset.is_valid():
            obj=form.save(commit=False)
            obj.owner=request.user

            obj.save()

            formset.instance=obj
            formset.save()

            messages.success(request,'Advertisement sent , after admin approve adv will shown')
            return redirect('my_listings')

    else:
        form = ListingForm()
        formset=ListingImageFormSet()
    return render(request,'listings/listing_form.html',{'form':form,'formset':formset,'mode':'create'})

@login_required
def listing_update(request,slug):
    listing=get_object_or_404(Listing,slug=slug,owner=request.user)
    if request.method=='POST':
        form = ListingForm(request.POST,request.FILES,instance=listing)
        formset=ListingImageFormSet(request.POST,request.FILES,instance=listing)

        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.info(request,'Advertisement updated , after admin approve adv will shown')
            return redirect('my_listings')
    else:
        form = ListingForm(instance=listing)
        formset=ListingImageFormSet(instance=listing)

    return render(request,'listings/listing_form.html',{'form':form,'formset':formset,'mode':'update'})

@login_required
def listing_delete(request,slug):
    listing=get_object_or_404(Listing,slug=slug,owner=request.user)
    if request.method=='POST':
        listing.delete()
        messages.success(request,'Advertisement deleted successfully')
    return redirect('my_listings')

@login_required
def my_listings(request):
    qs=Listing.objects.filter(owner=request.user)
    status=request.GET.get('status') or ''
    q=request.GET.get('q') or ''
    if status in dict(STATUS_CHOICES):
        qs=qs.filter(status=status)
    if q:
        qs=qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
    return render(request,'listings/my_listings.html',{'listings':qs,'q':q,'status':status})













