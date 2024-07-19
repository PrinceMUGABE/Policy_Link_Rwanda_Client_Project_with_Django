from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserInstitution
from .serializers import UserInstitutionSerializer

@api_view(['POST'])
def create_user_institution(request):
    if request.method == 'POST':
        serializer = UserInstitutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def get_user_institution_by_id(request, pk):
    try:
        user_institution = UserInstitution.objects.get(pk=pk)
    except UserInstitution.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = UserInstitutionSerializer(user_institution)
    return Response(serializer.data)

@api_view(['DELETE'])
def delete_user_institution(request, pk):
    try:
        user_institution = UserInstitution.objects.get(pk=pk)
    except UserInstitution.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    user_institution.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
