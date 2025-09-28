from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# NOTE: For simplicity, we are not linking to a 'User' model.
# In a real application, both Booking and Review would have a ForeignKey to a User model.

class Listing(models.Model):
    """Represents a property available for booking."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    price_per_night = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)]
    )
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    
    # A simple rating field, could be calculated in a real app
    average_rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0.0,
        validators=[MinValueValidator(0.0), MaxValueValidator(5.0)]
    )

    def __str__(self):
        return f"{self.title} in {self.city}, {self.country}"

class Booking(models.Model):
    """Represents a customer's reservation for a Listing."""
    # ForeignKey links a Booking to a specific Listing (Many-to-One)
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0.01)]
    )
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking for {self.listing.title} from {self.start_date} to {self.end_date}"

    class Meta:
        # Ensures no overlapping bookings for the same listing
        constraints = [
            models.UniqueConstraint(
                fields=['listing', 'start_date', 'end_date'],
                name='unique_booking_dates'
            )
        ]

class Review(models.Model):
    """Represents a user review for a Listing."""
    # ForeignKey links a Review to a specific Listing (Many-to-One)
    listing = models.ForeignKey(
        Listing, 
        on_delete=models.CASCADE, 
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.listing.title}: {self.rating} stars"