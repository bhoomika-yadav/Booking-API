import logging
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import FitnessClass, Booking
from .serializers import FitnessClassSerializer, BookingSerializer
from django.utils.timezone import now
from zoneinfo import ZoneInfo

logger = logging.getLogger(__name__)

# GET /classes
@api_view(['GET'])
def get_classes(request):
    user_timezone = request.query_params.get('timezone', 'Asia/Kolkata')  # default IST
    classes = FitnessClass.objects.filter(date_time__gte=now()).order_by('date_time')
    result = []

    for c in classes:
        dt_in_user_tz = c.date_time.astimezone(ZoneInfo(user_timezone))
        result.append({
            "id": c.id,
            "name": c.name,
            "date_time": dt_in_user_tz.isoformat(),
            "instructor": c.instructor,
            "available_slots": c.available_slots
        })

    return Response(result)

# POST /book
@api_view(['POST'])
def book_class(request):
    data = request.data
    required_fields = ['class_id', 'client_name', 'client_email']

    # Check for missing fields
    for field in required_fields:
        if field not in data:
            return Response({"error": f"Missing field: {field}"}, status=status.HTTP_400_BAD_REQUEST)

    class_id = data['class_id']
    client_name = data['client_name']
    client_email = data['client_email']

    try:
        fitness_class = FitnessClass.objects.get(id=class_id)
    except FitnessClass.DoesNotExist:
        return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

    if fitness_class.available_slots <= 0:
        return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)

    # Create booking
    booking = Booking.objects.create(
        fitness_class=fitness_class,
        client_name=client_name,
        client_email=client_email
    )

    # Reduce available slots
    fitness_class.available_slots -= 1
    fitness_class.save()

    # Log the booking
    logger.info(f"New booking: {client_name} ({client_email}) booked {fitness_class.name} at {fitness_class.date_time}")

    serializer = BookingSerializer(booking)
    return Response({"message": "Booking successful!", "booking": serializer.data}, status=status.HTTP_201_CREATED)

# GET /bookings?email=xxx
@api_view(['GET'])
def get_bookings(request):
    email = request.query_params.get('email')

    if not email:
        return Response({"error": "Missing email parameter"}, status=status.HTTP_400_BAD_REQUEST)

    bookings = Booking.objects.filter(client_email=email).order_by('-booking_time')
    serializer = BookingSerializer(bookings, many=True)
    return Response(serializer.data)


