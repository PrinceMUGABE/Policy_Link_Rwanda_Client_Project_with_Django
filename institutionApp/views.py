from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
import requests
from .models import Institution, Department, Policy
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import DepartmentSerializer, InstitutionSerializer, PolicySerializer




@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def view_all_institutions(request):
    # Synchronize client database with server database
    synchronize_with_server()

    # Fetch all institutions from the client database
    institutions = Institution.objects.all()
    serializer = InstitutionSerializer(institutions, many=True)

    return Response(serializer.data)


from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import InstitutionSerializer



from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def add_institution(request):
    name = request.data.get('name')
    type = request.data.get('type')

    # Fetch all institutions from the server database
    server_url = 'https://policy-link-server.onrender.com/api/view_all_institutions/'
    try:
        response = requests.get(server_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        server_data = response.json()
        server_institutions = server_data.get('institutions', [])

        # Check if the institution already exists in the client database
        if Institution.objects.filter(name=name).exists():
            return Response({'error': f'Institution "{name}" already exists in the client database.'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the submitted institution exists in the retrieved data
        matching_institution = next((inst_data for inst_data in server_institutions if inst_data['name'] == name), None)
        if not matching_institution:
            return Response({'error': f'Institution "{name}" does not exist on the server.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create new institution in client database
        new_institution = Institution.objects.create(name=name, type=type)

        # Retrieve associated departments for this institution from the server
        departments_url = f'https://policy-link-server.onrender.com/api/get_departments_by_institution_name/?name={name}'
        dept_response = requests.get(departments_url)
        dept_data = dept_response.json().get('departments', [])
        for dept in dept_data:
            dept_name = dept.get('name')
            dept_id = dept.get('id')

            # Create new department in client database
            department = Department.objects.create(name=dept_name, institution=new_institution)

            # Retrieve associated policies for this department from the server
            policies_url = f'https://policy-link-server.onrender.com/api/get_policies_by_department_name/?name={dept_name}'
            policy_response = requests.get(policies_url)
            policy_data = policy_response.json().get('policies', [])
            for policy in policy_data:
                policy_name = policy.get('name')
                policy_description = policy.get('description')
                # Create new policy in client database
                Policy.objects.create(name=policy_name, description=policy_description, department=department)

        return Response({'message': 'Data retrieved and saved successfully.'}, status=status.HTTP_201_CREATED)

    except requests.exceptions.RequestException as e:
        return Response({'error': f'Error occurred while retrieving data from the server: {e}'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
# @permission_classes([IsAuthenticated])
@csrf_exempt
def delete_institution(request, institution_id):
    institution = get_object_or_404(Institution, id=institution_id)
    institution.delete()
    return JsonResponse({'message': 'institution deleted successfully'}, status=200)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def view_all_departments(request):
    departments = Department.objects.all()
    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def view_all_policies(request):
    policies = Policy.objects.all()
    serializer = PolicySerializer(policies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @login_required
def get_institutions_by_type(request):
    institution_type = request.GET.get('type')
    synchronize_with_server()
    institutions = Institution.objects.filter(type=institution_type).values('id', 'name')
    return JsonResponse(list(institutions), safe=False)


import logging

logger = logging.getLogger(__name__)

@api_view(['GET'])
def get_departments_by_institution(request):
    institution_id = request.GET.get('institution_id')
    logger.debug(f"Received institution_id: {institution_id}")

    departments = Department.objects.filter(institution=institution_id)
    logger.debug(f"Departments found: {departments}")

    serializer = DepartmentSerializer(departments, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_policies_by_department(request):
    department_id = request.GET.get('department_id')
    
    department = Department.objects.get(id=department_id)
    
    
    policies = Policy.objects.filter(department=department)
    serializer = PolicySerializer(policies, many=True)
    response_data = {
        'policies': serializer.data,
        'department_name': department.name,
        'institute_name': department.institution.name,
        'institute_type': department.institution.type,
    }
    return Response(response_data)



def synchronize_with_server():
    try:
        # Fetch all institutions from the server database
        server_url = 'https://policy-link-server.onrender.com/api/view_all_institutions/'
        print(f'Fetching institutions from {server_url}')
        response = requests.get(server_url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        server_data = response.json()
        server_institutions = server_data.get('institutions', [])
        print(f'Received {len(server_institutions)} institutions from server')

        # Collect all institution names from the server for comparison
        server_institution_names = set(inst_data['name'] for inst_data in server_institutions)

        # Retrieve all institutions from the client database
        client_institutions = Institution.objects.all()

        # Update or add institutions based on server data
        for server_inst_data in server_institutions:
            server_inst_name = server_inst_data.get('name')
            server_inst_type = server_inst_data.get('type')

            # Check if the institution exists in the client database
            existing_inst = client_institutions.filter(name=server_inst_name).first()
            if existing_inst:
                # Update existing institution if its type has changed
                if existing_inst.type != server_inst_type:
                    existing_inst.type = server_inst_type
                    existing_inst.save()
                    print(f'Updated institution type for {server_inst_name}: {server_inst_type}')

                # Synchronize departments for this institution
                synchronize_departments_with_server(existing_inst)

            else:
                print(f'Institution "{server_inst_name}" does not exist in the client database.')

        # Remove institutions from the client database that are not present on the server
        to_delete = client_institutions.exclude(name__in=server_institution_names)
        if to_delete.exists():
            print(f'Removing {to_delete.count()} institutions not present on the server')
            to_delete.delete()

        print('Synchronization with server database completed successfully.')

    except requests.exceptions.RequestException as e:
        print(f'Error occurred while synchronizing data with the server: {e}')


def synchronize_departments_with_server(institution):
    try:
        # Fetch departments for the given institution from the server
        departments_url = f'https://policy-link-server.onrender.com/api/get_departments_by_institution_name/?name={institution.name}'
        print(f'Fetching departments from {departments_url}')
        dept_response = requests.get(departments_url)
        dept_response.raise_for_status()
        dept_data = dept_response.json().get('departments', [])
        print(f'Received {len(dept_data)} departments for institution {institution.name}')

        # Retrieve all departments for the institution from the client database
        client_departments = institution.department_set.all()

        # Update or add departments based on server data
        for dept_info in dept_data:
            dept_name = dept_info.get('name')
            dept_id = dept_info.get('id')

            # Check if the department exists in the client database
            existing_dept = client_departments.filter(name=dept_name).first()
            if existing_dept:
                print(f'Department "{dept_name}" already exists for institution "{institution.name}"')
            else:
                # Create new department in client database
                new_department = Department.objects.create(name=dept_name, institution=institution)
                print(f'New department added for institution {institution.name}: {dept_name}')

            # Synchronize policies for this department
            synchronize_policies_with_server(existing_dept or new_department)

        # Remove departments from the client database that are not present on the server
        dept_names_from_server = [dept['name'] for dept in dept_data]
        to_delete = client_departments.exclude(name__in=dept_names_from_server)
        if to_delete.exists():
            print(f'Removing {to_delete.count()} departments not present on the server for institution {institution.name}')
            to_delete.delete()

    except requests.exceptions.RequestException as e:
        print(f'Error occurred while synchronizing departments with the server: {e}')


def synchronize_policies_with_server(department):
    try:
        # Fetch policies for the given department from the server
        policies_url = f'https://policy-link-server.onrender.com/api/get_policies_by_department_name/?name={department.name}'
        print(f'Fetching policies from {policies_url}')
        policy_response = requests.get(policies_url)
        policy_response.raise_for_status()
        policy_data = policy_response.json().get('policies', [])
        print(f'Received {len(policy_data)} policies for department {department.name}')

        # Retrieve all policies for the department from the client database
        client_policies = department.policy_set.all()

        # Extract policy names from policy_data
        policy_names_from_server = [policy['name'] for policy in policy_data]

        # Update or add policies based on server data
        for policy_info in policy_data:
            policy_name = policy_info.get('name')
            policy_description = policy_info.get('description')

            # Check if the policy exists in the client database
            existing_policy = client_policies.filter(name=policy_name).first()
            if existing_policy:
                print(f'Policy "{policy_name}" already exists for department "{department.name}"')
            else:
                # Create new policy in client database
                Policy.objects.create(name=policy_name, description=policy_description, department=department)
                print(f'New policy added for department {department.name}: {policy_name}')

        # Remove policies from the client database that are not present on the server
        to_delete = client_policies.exclude(name__in=policy_names_from_server)
        if to_delete.exists():
            print(f'Removing {to_delete.count()} policies not present on the server for department {department.name}')
            to_delete.delete()

    except requests.exceptions.RequestException as e:
        print(f'Error occurred while synchronizing policies with the server: {e}')






















'''
    The following part is for generating repots on the institutions, departments
        and policies
'''


from django.http import JsonResponse
from .models import Department
from django.db.models import Count
from django.http import JsonResponse
from .models import Institution


# Total number of institutions
def total_institutions(request):
    total_count = Institution.objects.count()
    return JsonResponse({'total_institutions': total_count})

# Distribution of institutions by type
def institutions_distribution(request):
    distribution = Institution.objects.values('type').annotate(count=Count('type'))
    return JsonResponse({'institutions_distribution': list(distribution)})

# List of all institutions with details
def all_institutions(request):
    institutions = Institution.objects.values('name', 'type')
    return JsonResponse({'institutions': list(institutions)})

# Summary statistics (average number of departments per institution)
def average_departments_per_institution(request):
    average_departments = Department.objects.all().count() / Institution.objects.count()
    return JsonResponse({'average_departments_per_institution': average_departments})



'''
    For departments
'''

from django.http import JsonResponse
from .models import Department

def department_performance_report(request):
    # Perform analysis and gather performance metrics for each department
    # Example: Calculate policy compliance rates, completion rates, etc.
    # Replace this with your actual analysis logic
    
    # For demonstration purposes, let's assume we're fetching department names and their compliance rates
    departments_performance = [{'department': department.name, 'compliance_rate': calculate_compliance_rate(department)} for department in Department.objects.all()]
    
    # Identify departments with highest and lowest performance
    highest_performance = max(departments_performance, key=lambda x: x['compliance_rate'])
    lowest_performance = min(departments_performance, key=lambda x: x['compliance_rate'])
    
    return JsonResponse({
        'departments_performance': departments_performance,
        'highest_performance': highest_performance,
        'lowest_performance': lowest_performance
    })

def calculate_compliance_rate(department):
    # Placeholder function to calculate compliance rate
    # Replace this with your actual calculation logic
    return 0.8  # Example: 80% compliance rate




from django.http import JsonResponse
from .models import Policy

def policy_compliance_report(request):
    # Perform analysis and track policy compliance rates across departments or institutions
    # Example: Calculate compliance rates for each policy and department
    
    # Placeholder data for demonstration
    policies = Policy.objects.all()
    compliance_report = [{'policy': policy.name, 'compliance_rate': calculate_compliance_rate(policy)} for policy in policies]
    
    # Identify areas of non-compliance and potential areas for improvement
    non_compliant_policies = [report for report in compliance_report if report['compliance_rate'] < 0.8]  # Example: 80% compliance threshold
    
    return JsonResponse({
        'policy_compliance_report': compliance_report,
        'non_compliant_policies': non_compliant_policies
    })

def calculate_compliance_rate(policy):
    # Placeholder function to calculate compliance rate
    # Replace this with your actual calculation logic
    return 0.8  # Example: 80% compliance rate






from django.http import JsonResponse
from .models import Institution
from datetime import datetime, timedelta

def trend_analysis_report(request):
    # Perform trend analysis over time for metrics such as institution growth, policy adoption rates, etc.
    # Example: Analyze growth in the number of institutions over time
    
    # Placeholder data for demonstration
    institutions = Institution.objects.all()
    current_year = datetime.now().year
    years = range(current_year - 5, current_year + 1)  # Analyze data for the past 5 years
    
    # Calculate institution growth for each year
    institution_growth = [{'year': year, 'institution_count': Institution.objects.filter(establishment_year__year=year).count()} for year in years]
    
    # Example: Analyze policy adoption rates over time
    
    # Calculate policy adoption rates for each year
    policy_adoption_rates = [{'year': year, 'adoption_rate': calculate_adoption_rate(year)} for year in years]
    
    return JsonResponse({
        'institution_growth': institution_growth,
        'policy_adoption_rates': policy_adoption_rates
    })

def calculate_adoption_rate(year):
    # Placeholder function to calculate policy adoption rate
    # Replace this with your actual calculation logic
    return 0.75  # Example: 75% adoption rate




from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from .models import Policy, Department

def download_policies_pdf(request, institution_name, department_name):
    # Fetch policies for the given department and institution
    try:
        department = Department.objects.get(name=department_name)
        policies = Policy.objects.filter(department=department)
    except Department.DoesNotExist:
        return HttpResponse("Department not found", status=404)
    
    # Create PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{institution_name}_{department_name}_policies.pdf"'
    
    doc = SimpleDocTemplate(response, pagesize=letter)
    
    # Prepare data for PDF table
    data = [['ID', 'Name', 'Description']]
    for policy in policies:
        data.append([str(policy.id), policy.name, policy.description])
    
    # Create PDF table
    table = Table(data)
    table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                               ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                               ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                               ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                               ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                               ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                               ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
    
    # Build PDF document
    doc.build([table])
    
    return response
















from django.http import JsonResponse
from django.db.models import Count
from datetime import datetime, timedelta
from .models import Institution

# RESTful API for institution increase over time
def institution_increase_over_time(request):
    # Define time periods (e.g., monthly)
    start_date = datetime(2020, 1, 1)  # Start date of data collection
    end_date = datetime.now()           # End date is the current date

    # Aggregate data for each month
    data = []
    current_date = start_date
    while current_date <= end_date:
        next_date = current_date + timedelta(days=30)  # Assume each month has 30 days
        count = Institution.objects.filter(created_at__range=(current_date, next_date)).count()
        data.append(count)
        current_date = next_date

    # Format data for histogram chart
    labels = []
    current_date = start_date
    while current_date <= end_date:
        labels.append(current_date.strftime('%Y-%m'))
        current_date += timedelta(days=30)  # Move to the next month

    histogram_data = {
        'labels': labels,
        'data': data,
    }

    return JsonResponse(histogram_data)






'''
    Comments functions for the users upon policies
'''

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from .models import Comment, Policy
from userAccount.models import CustomUser

@api_view(['POST'])

def add_comment(request):
    if request.method == 'POST':
        email = request.data.get('email')
        institution_name = request.data.get('institution')
        department_name = request.data.get('department')
        policy_name = request.data.get('policy')
        comment_description = request.data.get('description')

        # Retrieve user based on email
        user = get_object_or_404(CustomUser, email=email)

        # Retrieve policy based on name and department
        policy = get_object_or_404(Policy, name=policy_name, department__name=department_name,
                                   department__institution__name=institution_name)

        # Create and save the comment
        comment = Comment(user=user, description=comment_description, policy=policy)
        comment.save()

        return JsonResponse({'message': 'Comment added successfully'}, status=201)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)



def view_all_comments(request):
    comments = Comment.objects.all()
    data = [
        {
            'id': comment.id,
            'user': comment.user.email,
            'policy': comment.policy.name,
            'description': comment.description,
            'created_at': comment.created_at,
            'department': comment.policy.department.name,
            'institution': comment.policy.department.institution.name
        }
        for comment in comments
    ]
    return JsonResponse({'comments': data})



def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return JsonResponse({'message': 'Comment deleted successfully'}, status=200)

def search_comment(request):
    if request.method == 'POST':
        search_query = request.POST.get('search_query')

        comments = Comment.objects.filter(description__icontains=search_query)
        data = [{'id': comment.id, 'user': comment.user.email, 'policy': comment.policy.name,
                 'description': comment.description, 'created_at': comment.created_at} for comment in comments]

        return JsonResponse({'comments': data})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
    
    
    
    

'''
    report on comments
'''

from django.http import JsonResponse
from django.db.models import Count
from django.utils.timezone import now
from .models import Comment, Institution, Department, Policy
from userAccount.models import CustomUser

def generate_comment_reports(request):
    # Total number of comments
    total_comments = Comment.objects.count()

    # Most commented institution
    most_commented_institution = Institution.objects.annotate(comment_count=Count('department__policy__comment')).order_by('-comment_count').first()

    # Most commented department
    most_commented_department = Department.objects.annotate(comment_count=Count('policy__comment')).order_by('-comment_count').first()

    # Most commented policy
    most_commented_policy = Policy.objects.annotate(comment_count=Count('comment')).order_by('-comment_count').first()

    # Most commenting emails
    most_commenting_users = CustomUser.objects.annotate(comment_count=Count('comment')).order_by('-comment_count')[:5]

    # Comments over time (by month)
    comments_over_time = Comment.objects.dates('created_at', 'month').annotate(comment_count=Count('id')).order_by('created_at')

    # Preparing data for the response
    report_data = {
        'total_comments': total_comments,
        'most_commented_institution': most_commented_institution.name if most_commented_institution else None,
        'most_commented_department': most_commented_department.name if most_commented_department else None,
        'most_commented_policy': most_commented_policy.name if most_commented_policy else None,
        'most_commenting_users': [
            {'email': user.email, 'comment_count': user.comment_count} for user in most_commenting_users
        ],
        'comments_over_time': [
            {'month': comment_date.strftime('%Y-%m'), 'comment_count': comment_count}
            for comment_date, comment_count in zip(comments_over_time, [Comment.objects.filter(created_at__month=dt.month, created_at__year=dt.year).count() for dt in comments_over_time])
        ]
    }

    return JsonResponse(report_data)

