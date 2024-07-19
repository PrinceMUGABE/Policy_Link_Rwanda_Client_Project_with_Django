from django.contrib.auth import logout
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.hashers import check_password, make_password
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.crypto import get_random_string
import plotly
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import CustomUser
from .serializers import ContactUsSerializer, CustomUserSerializer
import random
import string


@api_view(['GET'])
def index(request):
    return Response({"message": "Welcome to the accounts API"})

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from userAccount.models import CustomUser
import random
import string

from django.utils.http import urlencode
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site
from .models import ActivationToken


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from userAccount.models import CustomUser, ActivationToken
import random
import string
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str  # Import force_str instead of smart_text
from django.contrib.auth.tokens import default_token_generator

# @api_view(['GET'])
# def activate_account(request, uidb64, token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uidb64))  # Use force_str instead of smart_text
#         user = CustomUser.objects.get(pk=uid)
#         if default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save()
#             # Send email to the user to confirm account activation
#             subject = 'Account Activated'
#             message = 'Your account has been successfully activated.'
#             from_email = 'Policy-Link-Rwanda'
#             recipient_list = [user.email]
#             send_mail(subject, message, from_email, recipient_list)
#             return Response({'message': 'Your account has been successfully activated.'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(['POST'])
# def signup(request):
#     data = request.data
#     first_name = data.get('first_name')
#     last_name = data.get('last_name')
#     email = data.get('email')
#     phone = data.get('phone')
#     username = data.get('username')

#     if not email or not email.strip():
#         return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
#     if CustomUser.objects.filter(email=email).exists():
#         return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

#     if not phone or not phone.strip():
#         return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
#     if len(phone) != 10 or not phone.isdigit():
#         return Response({'error': 'Phone number must be 10 digits'}, status=status.HTTP_400_BAD_REQUEST)
#     valid_prefixes = ['078', '072', '073', '079']
#     if not phone.startswith(tuple(valid_prefixes)):
#         return Response({'error': 'The phone number must be from Rwandan Society'}, status=status.HTTP_400_BAD_REQUEST)
#     if CustomUser.objects.filter(phone=phone).exists():
#         return Response({'error': 'Phone number is already registered'}, status=status.HTTP_400_BAD_REQUEST)

#     if not username or not username.strip():
#         return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
#     if CustomUser.objects.filter(username=username).exists():
#         return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

#     password = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    
#     user = CustomUser.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name, phone=phone)
#     user.is_active = False  # Set user to inactive until they click the activation link
#     user.save()

#     # Generate activation token
#     token = default_token_generator.make_token(user)

#     # Build activation link
#     uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
#     activation_link = f"http://127.0.0.1:8000//account/activate/{uidb64}/{token}"

#     # Send activation email
#     subject = 'Activate Your Account'
#     message = f'Hello {first_name},\n\nThank you for signing up with us. Please click the link below to activate your account:\n\n{activation_link}\n\nPlease note that this link will expire in 20 minutes.'
#     from_email = 'Policy-Link-Rwanda'
#     recipient_list = [email]
#     send_mail(subject, message, from_email, recipient_list)
    
#     return Response({'message': 'User data stored. Please check your email for the activation link.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def signup(request):
    data = request.data
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    username = data.get('username')

    print(f'Received data: first_name={first_name}, last_name={last_name}, email={email}, phone={phone}, username={username}')

    if not email or not email.strip():
        return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(email=email).exists():
        return Response({'error': 'Email is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    if not phone or not phone.strip():
        return Response({'error': 'Phone number is required'}, status=status.HTTP_400_BAD_REQUEST)
    if len(phone) != 10 or not phone.isdigit():
        return Response({'error': 'Phone number must be 10 digits'}, status=status.HTTP_400_BAD_REQUEST)
    valid_prefixes = ['078', '072', '073', '079']
    if not phone.startswith(tuple(valid_prefixes)):
        return Response({'error': 'The phone number must be from Rwandan Society'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(phone=phone).exists():
        return Response({'error': 'Phone number is already registered'}, status=status.HTTP_400_BAD_REQUEST)

    if not username or not username.strip():
        return Response({'error': 'Username is required'}, status=status.HTTP_400_BAD_REQUEST)
    if CustomUser.objects.filter(username=username).exists():
        return Response({'error': 'Username is already taken'}, status=status.HTTP_400_BAD_REQUEST)

    password = generate_password()
    print(f'Generated password: {password}')
    
    hashed_password = make_password(password)
    user = CustomUser(
        first_name=first_name,  # Ensure first_name is properly passed
        last_name=last_name,
        email=email,
        phone=phone,
        username=username,
        password=hashed_password,
        is_active=False  # User is not active until they activate
    )
    user.save()

    # Generate and save the activation token
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    ActivationToken.objects.create(user=user, token=token)

    # Generate activation link
    current_site = get_current_site(request)
    activation_link = f"http://{current_site.domain}{reverse('activate', kwargs={'token': token})}"

    # Send activation email
    subject = 'Activate Your Account'
    message = f'Hi {first_name},\n\n Welcome to POLICY LINK RWANDA \n Your details are:\n Username: {username}\n Password: {password}\n\n Please click the link below to activate your account:\n\n{activation_link}\n\nThis link will expire in 20 minutes.'
    from_email = 'Policy-Link-Rwanda'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)

    return Response({'message': 'Please check your email to activate your account.'}, status=status.HTTP_200_OK)



def generate_password():
    while True:
        password = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=10))
        if (any(c.islower() for c in password) and
            any(c.isupper() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in string.punctuation for c in password) and
            len(password) >= 5):
            return password



from django.shortcuts import get_object_or_404
from django.utils import timezone

@api_view(['GET'])
def activate(request, token):
    activation_token = get_object_or_404(ActivationToken, token=token)
    
    if activation_token.is_expired():
        return Response({'error': 'Activation link has expired.'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = activation_token.user
    user.is_active = True
    user.save()
    
    # Optionally, delete the token after activation
    activation_token.delete()
    
    return Response({'message': 'Account activated successfully. You can now login.'}, status=status.HTTP_200_OK)



from django.http import HttpResponseRedirect
from django.urls import reverse

@api_view(['GET'])
def activate_account(request, token):
    try:
        activation_token = ActivationToken.objects.get(token=token)
        user = activation_token.user
        user.is_active = True
        user.save()
        activation_token.delete()  # Delete the token after activation
        return render(request, 'accounts/account_activation_success.html')
    except ActivationToken.DoesNotExist:
        return Response({'error': 'Invalid activation token.'}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import CustomUser

@api_view(['POST'])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = CustomUser.objects.get(username=username)
        if not check_password(password, user.password):
            print(' \n\n Ivalid password \n\n')
            return Response({'error': 'Invalid password.'}, status=status.HTTP_400_BAD_REQUEST)
        elif not user.is_active:
            print('\n\n Activate your account \n\n')
            return Response({'error': 'Activate your account'}, status=status.HTTP_400_BAD_REQUEST)

        # Increment login count
        user.login_count += 1
        user.save()

        # Add user data to the response
        response_data = {
            'user': {
                'username': user.username,
                'role': user.role,
                'login_count': user.login_count,
                'email': user.email
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        print('\n\n Invalid username \n\n')
        return Response({'error': 'Invalid username.'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def user_dashboard(request):
    return Response({"message": "Welcome to the user dashboard"})


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def admin_dashboard(request):
    return Response({"message": "Welcome to the admin dashboard"})


@api_view(['GET'])
def view_all_users(request):
    users = CustomUser.objects.all()
    for user in users:
        print(f"User: {user.username}, Firstname: {user.first_name}, Lastname: {user.last_name}")
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
# @permission_classes([IsAuthenticated])
def edit_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    data = request.data

    serializer = CustomUserSerializer(user, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
def delete_user(request, user_id):
    try:
        user = CustomUser.objects.get(pk=user_id)
        user.delete()
        return Response({'success': True}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)




'''
    Reports about users
'''


from django.http import HttpResponse, JsonResponse
from .models import CustomUser
from django.db.models import Count

# Total number of users
@api_view(['GET'])
def total_users(request):
    total_users = CustomUser.objects.count()
    return JsonResponse({'total_users': total_users})

# Distribution of users by role
@api_view(['GET'])
def users_distribution(request):
    distribution = CustomUser.objects.values('role').annotate(count=Count('role'))
    return JsonResponse({'users_distribution': list(distribution)})

# List of all users with details
@api_view(['GET'])
def all_users(request):
    users = CustomUser.objects.all()
    user_data = [{'username': user.username, 'email': user.email, 'role': user.role} for user in users]
    return JsonResponse({'users': user_data})





# views.py

import json
from django.http import JsonResponse
import plotly.graph_objects as go

def user_growth_over_years(request):
    # Retrieve user growth data from the database or any other data source
    years = [2020, 2021, 2022, 2023, 2024]
    user_counts = [100, 150, 200, 250, 300]  # Sample data

    # Create a Plotly line chart
    fig = go.Figure(data=go.Scatter(x=years, y=user_counts, mode='lines+markers'))

    # Customize the chart layout
    fig.update_layout(title='User Growth Over Years',
                      xaxis_title='Year',
                      yaxis_title='Number of Users')

    # Convert the Plotly figure to JSON
    graph_data = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return JsonResponse({'graph_data': graph_data})





from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CustomUser

@api_view(['POST'])
def reset_password(request):
    email = request.data.get('email')
    new_password = request.data.get('new_password')

    try:
        user = CustomUser.objects.get(email=email)
        
        # Update the user's password
        user.password = make_password(new_password)
        user.save()

        # Send email notification about the password change
        subject = 'Your Password Has Been Changed'
        message = f'Hello {user.username},\n\nYour password has been successfully changed.\n\nIf you did not request this change, please contact support immediately.'
        from_email = 'Policy-Link-Rwanda'
        recipient_list = [email]
        send_mail(subject, message, from_email, recipient_list)

        print("\n\nPassword changed successfully\n\n")

        return Response({'message': 'Password reset successfully. Please check your email for confirmation.'}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        print('\n\nInvalid email, user does not exist\n\n')
        return Response({'error': 'Invalid username or email.'}, status=status.HTTP_400_BAD_REQUEST)



# userAccount/views.py
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import CustomUser

def get_user_by_id(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'created_at': user.created_at,
        'last_login': user.last_login,
    }
    return JsonResponse(user_data)


def get_user_by_username(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_data = {
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'phone': user.phone,
        'role': user.role,
        'created_at': user.created_at,
        'last_login': user.last_login,
        'login_count': user.login_count,
    }
    return JsonResponse(user_data)





from django.http import HttpResponse
from django.shortcuts import get_list_or_404
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import pandas as pd
from .models import CustomUser

# Function to generate and download users in PDF format
def download_users_pdf(request):
    users = get_list_or_404(CustomUser)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="all_users.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    y = height - 40

    p.drawString(100, y, "All Users")
    y -= 30

    for user in users:
        p.drawString(30, y, f"Username: {user.username}")
        p.drawString(200, y, f"Email: {user.email}")
        p.drawString(400, y, f"Role: {user.role}")
        y -= 20
        if y < 40:
            p.showPage()
            y = height - 40

    p.save()
    return response

# Function to generate and download users in Excel format
def download_users_excel(request):
    users = CustomUser.objects.all()
    user_data = [{
        'Username': user.username,
        'First Name': user.first_name,
        'Last Name': user.last_name,
        'Email': user.email,
        'Phone': user.phone,
        'Role': user.role,
        'Created At': user.created_at,
        'Last Login': user.last_login,
    } for user in users]

    df = pd.DataFrame(user_data)
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="all_users.xlsx"'
    df.to_excel(response, index=False)
    return response



from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

@api_view(['POST'])
def contact_us(request):
    serializer = ContactUsSerializer(data=request.data)
    if serializer.is_valid():
        names = serializer.validated_data['names']
        email = serializer.validated_data['email']
        subject = serializer.validated_data['subject']
        description = serializer.validated_data['description']
        
        # Check for empty fields
        if not names.strip():
            return Response({"error": "Name field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        if not subject.strip():
            return Response({"error": "Subject field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)
        if not description.strip():
            return Response({"error": "Description field cannot be empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        try:
            validate_email(email)
        except ValidationError:
            return Response({"error": "Invalid email format."}, status=status.HTTP_400_BAD_REQUEST)

        # Sending email
        send_mail(
            subject=f"Contact Us: {subject}",
            message=f"Name: {names}\nEmail: {email}\n\nDescription:\n{description}",
            from_email=email,
            recipient_list=['princemugabe567@gmail.com'],
            fail_silently=False,
        )
        return Response({"message": "Email sent successfully."}, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
