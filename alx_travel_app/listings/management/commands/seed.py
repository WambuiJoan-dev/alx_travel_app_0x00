import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from django.db import transaction
from listings.models import Listing, Booking, Review

# Helper function to generate sample data
def get_sample_listings(count=5):
    """Generates a list of dictionaries with sample Listing data."""
    sample_data = []
    
    # Simple lists to pick random data from
    cities = ['New York', 'Paris', 'Tokyo', 'London', 'Sydney', 'Cape Town', 'Nairobi']
    countries = ['USA', 'France', 'Japan', 'UK', 'Australia', 'South Africa', 'Kenya']
    titles = ['Cozy Studio', 'Luxury Penthouse', 'Rustic Cabin', 'Modern Loft', 'Beachfront Villa']
    descriptions = [
        "A quiet, sunlit space with great access to the city center.",
        "Stunning views and top-tier amenities for a truly luxurious stay.",
        "Escape to nature in this charming, secluded wooden cabin.",
        "Sleek design and modern comforts, perfect for business travelers.",
        "Wake up to the sound of waves in your private beach retreat."
    ]

    for i in range(count):
        city = random.choice(cities)
        country = random.choice(countries)
        
        sample_data.append({
            'title': f"{random.choice(titles)} in {city}",
            'description': random.choice(descriptions),
            'price_per_night': round(random.uniform(50.0, 500.0), 2),
            'city': city,
            'country': country,
            'average_rating': round(random.uniform(3.0, 5.0), 2)
        })
    return sample_data

def get_sample_booking(listing):
    """Generates a sample Booking for a given Listing."""
    today = date.today()
    # Randomly select a future date
    start_date = today + timedelta(days=random.randint(5, 30))
    # Random stay length (2 to 7 nights)
    end_date = start_date + timedelta(days=random.randint(2, 7))
    
    num_nights = (end_date - start_date).days
    total_price = listing.price_per_night * num_nights
    
    return Booking(
        listing=listing,
        start_date=start_date,
        end_date=end_date,
        total_price=total_price
    )

def get_sample_review(listing):
    """Generates a sample Review for a given Listing."""
    ratings = [5, 5, 4, 3] # Weighted to be mostly positive
    comments = [
        "Absolutely loved my stay! Highly recommend.",
        "The host was very helpful and the place was spotless.",
        "Great location, but the check-in process was a bit slow.",
        "An amazing experience, will definitely book again.",
        "Fantastic value for money."
    ]
    
    return Review(
        listing=listing,
        rating=random.choice(ratings),
        comment=random.choice(comments)
    )

class Command(BaseCommand):
    help = 'Seeds the database with sample Listings, Bookings, and Reviews.'

    def add_arguments(self, parser):
        # Optional argument to control the number of listings
        parser.add_argument(
            '--listings', 
            type=int, 
            default=10, 
            help='Number of sample listings to create.'
        )

    @transaction.atomic
    def handle(self, *args, **kwargs):
        listing_count = kwargs['listings']
        self.stdout.write("Starting database seeding...")

        # 1. Clear existing data
        Review.objects.all().delete()
        Booking.objects.all().delete()
        Listing.objects.all().delete()
        self.stdout.write(self.style.WARNING("Cleared all existing Listings, Bookings, and Reviews."))
        
        # 2. Create Listings
        listing_objects = []
        for data in get_sample_listings(count=listing_count):
            listing_objects.append(Listing(**data))
        
        Listing.objects.bulk_create(listing_objects)
        self.stdout.write(self.style.SUCCESS(f"Successfully created {listing_count} sample listings."))
        
        # 3. Create Bookings and Reviews for each Listing
        created_listings = Listing.objects.all()
        booking_objects = []
        review_objects = []
        
        for listing in created_listings:
            # Create a random number of bookings (1 to 3)
            for _ in range(random.randint(1, 3)):
                booking_objects.append(get_sample_booking(listing))
            
            # Create a random number of reviews (1 to 5)
            for _ in range(random.randint(1, 5)):
                review_objects.append(get_sample_review(listing))

        # Bulk create the related objects
        Booking.objects.bulk_create(booking_objects)
        Review.objects.bulk_create(review_objects)
        
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(booking_objects)} bookings."))
        self.stdout.write(self.style.SUCCESS(f"Successfully created {len(review_objects)} reviews."))
        
        self.stdout.write(self.style.SUCCESS("Database seeding completed! 🎉"))