import base64
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, generics

from orders.models import Orders
from .serializers import CustomerSerializer, Customer
from drf_spectacular.utils import extend_schema


@extend_schema(
    request=None,  # No request body for login, as it's through the Authorization header
    responses={200: CustomerSerializer, 401: "Invalid credentials", 400: "Bad request"},
)
@api_view(["GET"])
def login(request):
    """
    Handles user login via Basic Authentication.

    This view expects a GET request with an "Authorization" header containing
    Basic Authentication credentials. It decodes the credentials, verifies the
    username and password, and returns the user's data if the credentials are valid.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: A Response object containing the serialized user data if the
        credentials are valid, or an error message if they are not.
    """
    auth = request.headers.get("Authorization")
    print(auth)
    if auth and auth.startswith("Basic "):

        auth = auth.split(" ")[1]

        user_pass = base64.b64decode(auth).decode("utf-8")

        print(user_pass)

        email, password = user_pass.split(":")
        print(email, password)
        user = Customer.objects.filter(email=email).first()

        if user and user.check_password(password):
            serializer = CustomerSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )
    else:
        return Response(
            {"error": "Authorization header missing"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@extend_schema(
    request=CustomerSerializer, responses={201: CustomerSerializer, 400: "Bad Request"}
)
@api_view(["POST"])
def register(request):
    """
    Handles user registration.

    This view expects a POST request with a JSON body containing the user's data.
    It creates a new user with the provided data and returns the user's data.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: A Response object containing the serialized user data.
    """

    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        order = Orders.objects.create(user=user, status="CART")
        order.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=CustomerSerializer,
    responses={
        200: CustomerSerializer,
        400: "Bad Request",
        401: "Authentication required",
    },
)
@api_view(["PATCH"])
def update_customer(request):
    """
    Handles updating a customer's data.

    This view expects a PATCH request with a JSON body containing the fields to update.
    It updates the customer's data and returns the updated data.

    Args:
        request (Request): The HTTP request object.

    Returns:
        Response: A Response object containing the serialized customer data.
    """
    if not request.user.is_authenticated:
        return Response(
            {"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED
        )
    customer = request.user
    serializer = CustomerSerializer(customer, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
