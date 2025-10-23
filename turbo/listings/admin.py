from django.contrib import admin
from .models import Listing, ListingStatus, ListingImage

from django.utils import timezone

# Register your models here.

class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display=('id','title','owner','price','status','published_at','created_at')
    list_filter=('status','brand','city','year')
    search_fields=('title','description','brand','model','city','owner__email','owner__username')
    autocomplete_fields=('owner',)
    readonly_fields=('created_at','updated_at','published_at','slug')
    inlines=[ListingImageInline]

    actions=['approve_listings','reject_listings']

    @admin.action(description="Approve selected Listings")
    def approve_listings(self, request, queryset):
        updated=queryset.update(status=ListingStatus.APPROVED,published_at=timezone.now())
        self.message_user(request,f'{updated} approved successfully!')

    @admin.action(description="Reject selected Listings")
    def reject_listings(self, request, queryset):
        updated=queryset.update(status=ListingStatus.REJECTED)
        self.message_user(request,f'{updated} rejected successfully!')

@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ('id','listing','order')