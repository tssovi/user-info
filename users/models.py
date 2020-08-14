from django.db import models
from django.utils.crypto import get_random_string


class UsersManager(models.Manager):
    # Get all value
    def get_all_users(self):
        data = self.all()
        return data

    # Get filtered value
    def get_user_by_id(self, user_ids):
        data = self.filter(user_id__in=user_ids)
        return data

    # Get user data
    def get_user_data_id(self, users_id):
        data = self.filter(user_id=users_id).values('user_type').first()
        return data

    # Insert user data
    def insert_user_data(self, request_data):
        s_users = []
        e_users = []

        for data in request_data:
            user_id = get_random_string(8).upper()
            first_name = data['first_name']
            last_name = data['last_name']
            user_type = data['user_type']

            full_name = first_name + " " + last_name

            # Check if user type
            if user_type == 'parent':
                address = data['address']
                street = data['street']
                city = data['city']
                state = data['state']
                zip_code = data['zip_code']
                # Try to insert data in database
                try:
                    flag = self.create(
                        user_id=user_id,
                        first_name=first_name,
                        last_name=last_name,
                        address=address,
                        street=street,
                        city=city,
                        state=state,
                        zip_code=zip_code,
                        user_type=user_type
                    )
                    s_users.append(user_id)
                except IndexError:
                    flag = 0

                # If any issue arise then save the user info in an error list
                if flag == 0:
                    e_users.append(full_name)
            # If action executed successfully then save the user info in a success list
            else:
                parent_id = data['parent_id']
                parent_data = self.get_user_data_id(parent_id)

                if parent_data:
                    try:
                        is_parent_type = parent_data['user_type']
                    except IndexError:
                        is_parent_type = ""
                else:
                    is_parent_type = ""

                if is_parent_type == "parent":
                    # Try to insert data in database
                    try:
                        flag = self.create(
                            user_id=user_id,
                            first_name=first_name,
                            last_name=last_name,
                            user_type=user_type,
                            parent_id=parent_id
                        )
                        s_users.append(user_id)
                    except IndexError:
                        flag = 0

                    # If any issue arise then save the user info in an error list
                    if flag == 0:
                        e_users.append(full_name)
                else:
                    e_users.append(full_name)
        # Return success and error list for further message
        return s_users, e_users

    # Update value against user_id
    def update_user_data_by_id(self, request_data):
        s_users = []
        e_users = []
        for data in request_data:
            user_id = data['user_id']
            first_name = data['first_name']
            last_name = data['last_name']
            user_type = data['user_type']

            # Check if user_id is empty
            if user_id:
                # Try to update data in database
                if user_type == 'parent':
                    address = data['address']
                    street = data['street']
                    city = data['city']
                    state = data['state']
                    zip_code = data['zip_code']

                    # Try to update parent type user data in database
                    try:
                        flag = self.filter(user_id=user_id).update(
                            first_name=first_name,
                            last_name=last_name,
                            address=address,
                            street=street,
                            city=city,
                            state=state,
                            zip_code=zip_code,
                            user_type=user_type
                        )
                        s_users.append(user_id)
                    except IndexError:
                        flag = 0

                    # If any issue arise then save the user info in an error list
                    if flag == 0:
                        e_users.append(user_id)
                # If action executed successfully then save the user info in a success list
                else:
                    parent_id = data['parent_id']
                    parent_data = self.get_user_data_id(parent_id)

                    try:
                        is_parent_type = parent_data['user_type']
                    except IndexError:
                        is_parent_type = ""

                    if is_parent_type == "parent":
                        # Try to update child type user data in database
                        try:
                            flag = self.filter(user_id=user_id).update(
                                first_name=first_name,
                                last_name=last_name,
                                user_type=user_type,
                                parent_id=parent_id
                            )
                            s_users.append(user_id)
                        except IndexError:
                            flag = 0

                        # If any issue arise then save the user info in an error list
                        if flag == 0:
                            e_users.append(user_id)
                    else:
                        e_users.append(user_id)
            # If action executed successfully then save the user info in a success list
            else:
                e_users.append(user_id)
        # Return success and error user list for further message
        return s_users, e_users

    # Delete user data by user id(s)
    def delete_user_data_by_id(self, user_ids):
        # Delete requested data
        query = self.filter(user_id__in=user_ids).delete()
        # Calculate deleted row(s) count
        del_count = query[0]
        # Return deleted row(s) count
        return del_count


class Users(models.Model):
    USERS_TYPE = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )

    user_id = models.CharField(max_length=8, primary_key=True, unique=True)
    first_name = models.CharField(max_length=250, null=False)
    last_name = models.CharField(max_length=250, null=False)
    address = models.TextField(default="")
    street = models.CharField(max_length=100, default="")
    city = models.CharField(max_length=100, default="")
    state = models.CharField(max_length=100, default="")
    zip_code = models.CharField(max_length=50, default="")
    user_type = models.CharField(max_length=10, choices=USERS_TYPE, default='parent')
    parent_id = models.CharField(max_length=8, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UsersManager()

    def __str__(self):
        return 'User ID: {} | User Name: {} {} | City: {} | User Type at: {}'.format(
            self.user_id, self.first_name, self.last_name, self.city, self.user_type
        )
