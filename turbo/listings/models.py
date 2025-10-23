from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify

# Create your models here.

User = get_user_model()

STATUS_CHOICES = [
    ('PENDING', 'Pending'),
    ('APPROVED', 'Approved'),
    ('REJECTED', 'Rejected'),
]


class ListingStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    APPROVED = 'APPROVED', 'Approved'
    REJECTED = 'REJECTED', 'Rejected'


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listings')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField()
    price = models.PositiveIntegerField()
    city = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    year = models.PositiveIntegerField(null=True, blank=True)
    milage = models.PositiveIntegerField(null=True, blank=True)
    fuel = models.CharField(max_length=100)
    gearbox = models.CharField(max_length=70)
    main_image = models.ImageField(upload_to='listings/', blank=True, null=True)

    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default=ListingStatus.PENDING)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['published_at', '-created_at']
        indexes = [models.Index(fields=['status', 'brand', 'model', 'city', 'price'])]

    def get_absolute_url(self):
        return reverse('listing_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # slug auto
        if not self.slug:
            base = slugify(self.title)[:200]
            candidate = base
            i = 1
            while Listing.objects.filter(slug=candidate).exists():
                i += 1
                candidate = f'{base}-{i}'
            self.slug = candidate

        if self.pk is not None:
            orig = Listing.objects.get(pk=self.pk)
            changed_fields = []
            for f in ['title', 'description', 'price', 'city', 'brand', 'model', 'year', 'milage', 'fuel', 'gearbox','main_image']:
                if getattr(orig, f) != getattr(self, f):
                    changed_fields.append(f)
            if changed_fields and orig.status == ListingStatus.APPROVED:
                self.status = ListingStatus.PENDING
                self.published_at = None

        super().save(*args, **kwargs)

class ListingImage(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='images')
    image=models.ImageField(upload_to='listings/extra/', blank=True, null=True)
    alt=models.CharField(max_length=200,blank=True)
    order=models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order','id']

    def __str__(self):
        return f'{self.listing.title} - {self.pk}'