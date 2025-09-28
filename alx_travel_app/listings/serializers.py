from rest_framework import serializers
from .models import Listing, Booking, Review

# 1. Serializer for the Review model (often nested)
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'rating', 'comment', 'created_at')

# 2. Serializer for the Listing model
class ListingSerializer(serializers.ModelSerializer):
    # Include all reviews related to the listing using the nested serializer
    reviews = ReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Listing
        # 'reviews' comes from the related_name='reviews' in the Review model ForeignKey
        fields = ('id', 'title', 'description', 'price_per_night', 'city', 'country', 'average_rating', 'reviews')
        
# 3. Serializer for the Booking model
class BookingSerializer(serializers.ModelSerializer):
    # Display the title of the listing instead of just the ID
    listing_title = serializers.ReadOnlyField(source='listing.title')

    class Meta:
        model = Booking
        fields = ('id', 'listing', 'listing_title', 'start_date', 'end_date', 'total_price', 'booked_at')
        read_only_fields = ('booked_at', 'total_price') # Total price would be calculated on save