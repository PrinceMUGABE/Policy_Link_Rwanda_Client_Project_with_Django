import json
from django.contrib.auth import login as auth_login, logout




def view_all_institutions(request):
    # Fetch all institutions from the database
    institutions = Institute.objects.all().values('id', 'name', 'type')
    return JsonResponse({'institutions': list(institutions)})



def get_institutions_by_type(request):
    institution_type = request.GET.get('type', None)
    institutions = Institute.objects.filter(type=institution_type).values('id', 'name', 'type')
    return JsonResponse({'institutions': list(institutions)})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def add_institution(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        type = data.get('type')
        # Check if the institution already exists
        if Institute.objects.filter(name=name).exists():
            return JsonResponse({'message': 'Institution with this name already exists'}, status=400)
        # Create a new institution
        new_institution = Institute.objects.create(name=name, type=type)
        return JsonResponse({'message': 'Institution added successfully', 'id': new_institution.id}, status=201)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)

@csrf_exempt
def update_institution(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        type = data.get('type')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Update the institution type
        institution.type = type
        institution.save()
        return JsonResponse({'message': 'Institution updated successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_institution(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Delete the institution
        institution.delete()
        return JsonResponse({'message': 'Institution deleted successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)




def view_all_departments(request):
    # Fetch all departments from the database
    departments = Department.objects.all().values('id', 'name', 'institutionId')
    return JsonResponse({'departments': list(departments)})

@csrf_exempt
def add_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        institution_name = data.get('institution')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=institution_name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Create a new department
        new_department = Department.objects.create(name=name, institutionId=institution)
        return JsonResponse({'message': 'Department added successfully', 'id': new_department.id}, status=201)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def update_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        institution_name = data.get('institution_name')
        new_name = data.get('new_name')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=institution_name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Check if the department exists
        try:
            department = Department.objects.get(name=name, institutionId=institution)
        except Department.DoesNotExist:
            return JsonResponse({'message': 'Department not found for the specified institution'}, status=404)
        # Update the department name
        department.name = new_name
        department.save()
        return JsonResponse({'message': 'Department updated successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_department(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        institution_name = data.get('institution_name')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=institution_name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Check if the department exists
        try:
            department = Department.objects.get(name=name, institutionId=institution)
        except Department.DoesNotExist:
            return JsonResponse({'message': 'Department not found for the specified institution'}, status=404)
        # Delete the department
        department.delete()
        return JsonResponse({'message': 'Department deleted successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



def view_all_policies(request):
    # Fetch all policies from the database
    policies = Policy.objects.all().values('id', 'name', 'departmentId', 'description')
    return JsonResponse({'policies': list(policies)})


@csrf_exempt
def add_policy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        description = data.get('description')
        department_name = data.get('department_name')
        institution_name = data.get('institution_name')
        # Check if the institution exists
        try:
            institution = Institute.objects.get(name=institution_name)
        except Institute.DoesNotExist:
            return JsonResponse({'message': 'Institution not found'}, status=404)
        # Check if the department exists
        try:
            department = Department.objects.get(name=department_name, institutionId=institution)
        except Department.DoesNotExist:
            return JsonResponse({'message': 'Department not found for the specified institution'}, status=404)
        # Check if the policy already exists
        if Policy.objects.filter(name=name, departmentId=department).exists():
            return JsonResponse({'message': 'Policy already exists for the specified department'}, status=400)
        # Create a new policy
        new_policy = Policy.objects.create(name=name, description=description, departmentId=department)
        return JsonResponse({'message': 'Policy added successfully', 'id': new_policy.id}, status=201)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



@csrf_exempt
def update_policy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        policy_id = data.get('policy_id')
        new_name = data.get('new_name')
        new_description = data.get('new_description')
        # Check if the policy exists
        try:
            policy = Policy.objects.get(id=policy_id)
        except Policy.DoesNotExist:
            return JsonResponse({'message': 'Policy not found'}, status=404)
        # Update the policy
        if new_name:
            policy.name = new_name
        if new_description:
            policy.description = new_description
        policy.save()
        return JsonResponse({'message': 'Policy updated successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


@csrf_exempt
def delete_policy(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        policy_id = data.get('policy_id')
        # Check if the policy exists
        try:
            policy = Policy.objects.get(id=policy_id)
        except Policy.DoesNotExist:
            return JsonResponse({'message': 'Policy not found'}, status=404)
        # Delete the policy
        policy.delete()
        return JsonResponse({'message': 'Policy deleted successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)



def get_departments_by_institution_name(request):
    institution_name = request.GET.get('name', None)
    departments = Department.objects.filter(institutionId__name=institution_name).values('id', 'name')
    return JsonResponse({'departments': list(departments)})


def get_policies_by_department_name(request):
    department_name = request.GET.get('name', None)
    policies = Policy.objects.filter(departmentId__name=department_name).values('id', 'name', 'description')
    return JsonResponse({'policies': list(policies)})




































































def get_institutions_by_type(request):
    institution_type = request.GET.get('type', None)
    institutions = list(Institute.objects.filter(type=institution_type).values('id', 'name'))
    return JsonResponse(institutions, safe=False)


def get_departments_by_institution(request):
    institution_id = request.GET.get('institution_id', None)
    departments = list(Department.objects.filter(institutionId_id=institution_id).values('id', 'name'))
    return JsonResponse(departments, safe=False)


from django.http import JsonResponse
from .models import Institute, Department, Policy


def get_policies_by_department(request):
    department_id = request.GET.get('department_id', None)

    # Fetch department, institute, and institute type for the given department
    department = Department.objects.get(id=department_id)
    department_name = department.name
    institute_name = department.institutionId.name
    institute_type = department.institutionId.type

    # Print retrieved information
    print("Department Name:", department_name)
    print("Institute Name:", institute_name)
    print("Institute Type:", institute_type)

    # Fetch policies for the department
    policies = list(Policy.objects.filter(departmentId_id=department_id).values('id', 'name', 'description'))

    # Add department, institute, and institute type to each policy
    for policy in policies:
        policy['department_name'] = department_name
        policy['institute_name'] = institute_name
        policy['institute_type'] = institute_type

    # Print policies
    print("Policies:", policies)

    # Return the policies along with additional information
    return JsonResponse({'policies': policies, 'department_name': department_name, 'institute_name': institute_name,
                         'institute_type': institute_type}, safe=False)
