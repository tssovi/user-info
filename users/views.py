from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import Users
from users.serializers import UsersSerializer


class UsersView(APIView):
    # Process get request from api
    @staticmethod
    def get(request, *args, **kwargs):
        user_ids = request.GET.get('user_ids')

        # Check if the keys has any key or not
        if user_ids:
            user_ids = user_ids.split(',')
            response_data = Users.objects.get_user_by_id(user_ids)
        else:
            response_data = Users.objects.get_all_users()

        # Serialize response data
        users_data = UsersSerializer(response_data, many=True)
        data = users_data.data

        # Check response data empty or not
        if len(data) > 0:
            return Response(
                {
                    'data': data,
                    'message': "Get Requested User Data",
                    'response_code': "GRD-200"
                }, status=status.HTTP_200_OK
            )
        else:
            if user_ids:
                return Response(
                    {
                        'message': "No User Data Found for This User ID(s) - {}".format(user_ids),
                        'response_code': "NDF-400"
                    }, status=status.HTTP_404_NOT_FOUND
                )
            else:
                return Response(
                    {
                        'message': "No User Data Found In Storage",
                        'response_code': "NDS-400"
                    }, status=status.HTTP_404_NOT_FOUND
                )

    # Process post request from api
    @staticmethod
    def post(request, *args, **kwargs):
        data = request.data
        s_users, e_users = Users.objects.insert_user_data(data)

        # Check if any error occurred during insertion or not
        if len(e_users) < 1:
            response_data = Users.objects.get_user_by_id(s_users)
            users_data = UsersSerializer(response_data, many=True)

            return Response(
                {
                    'data': users_data.data,
                    'message': "User Data Inserted Successfully",
                    'response_code': "DIS-201"
                }, status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'message': "Error Occurred During User Data Insertion for This User(s) - {}".format(e_users),
                'response_code': "DIF-400"
            }, status=status.HTTP_400_BAD_REQUEST
        )

    # Process patch request from api
    @staticmethod
    def patch(request, *args, **kwargs):
        data = request.data
        s_users, e_users = Users.objects.update_user_data_by_id(data)

        # Check if any error occurred during update or not
        if len(e_users) < 1:
            response_data = Users.objects.get_user_by_id(s_users)
            users_data = UsersSerializer(response_data, many=True)
            return Response(
                {
                    'data': users_data.data,
                    'message': "User Data Updated Successfully",
                    'response_code': "DUS-201"
                }, status=status.HTTP_201_CREATED
            )

        return Response(
            {
                'message': "Error Occurred During User Info Update for This User ID(s) - {}".format(e_users),
                'response_code': "EDU-400"
            }, status=status.HTTP_400_BAD_REQUEST
        )

    # Process delete request from api
    @staticmethod
    def delete(request, *args, **kwargs):
        user_ids = request.GET.get('user_ids')

        # Check if the keys has any key or not
        if user_ids:
            user_ids = user_ids.split(',')
            del_count = Users.objects.delete_user_data_by_id(user_ids)
            user_count = len(user_ids)
            if del_count > 0:
                return Response(
                    {
                        'message': "{} User(s) Data Deleted Successfully. {} User ID Provided.".format(
                            del_count, user_count
                        ),
                        'response_code': "DDS-200"
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {
                        'message': "No User Found With Provided User ID(s). Please Try Again With A Valid ID",
                        'response_code': "DNF-200"
                    }, status=status.HTTP_404_NOT_FOUND
                )
        else:
            return Response(
                {
                    'message': "Can't Delete Users With User ID",
                    'response_code': "CDD-404"
                }, status=status.HTTP_404_NOT_FOUND
            )
