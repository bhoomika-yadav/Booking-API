from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import FitnessClass, Booking
from django.utils.timezone import now
from datetime import timedelta

class BookingAPITestCase(APITestCase):
    def setUp(self):
        self.fitness_class = FitnessClass.objects.create(
            name="Yoga",
            date_time=now() + timedelta(days=1),
            instructor="Alice",
            total_slots=10,
            available_slots=10
        )

    def test_get_classes(self):
        url = reverse('classes-list')  # adjust name to your URL pattern
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_post_booking_success(self):
        url = reverse('book-class')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Test User",
            "client_email": "test@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.fitness_class.refresh_from_db()
        self.assertEqual(self.fitness_class.available_slots, 9)

    def test_post_booking_no_slots(self):
        self.fitness_class.available_slots = 0
        self.fitness_class.save()
        url = reverse('book-class')
        data = {
            "class_id": self.fitness_class.id,
            "client_name": "Test User",
            "client_email": "test@example.com"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No slots available", str(response.data))

    def test_get_bookings_by_email(self):
        Booking.objects.create(
            fitness_class=self.fitness_class,
            client_name="Test User",
            client_email="test@example.com"
        )
        url = reverse('bookings-list')
        response = self.client.get(url, {'email': 'test@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

