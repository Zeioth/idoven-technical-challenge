from config import config as c
import requests
from fastapi import status


def test_login():
    """
    Login using the admin credentials

    Asserts:
        - Status code 200.
        - The field access_token exist in the response.
    """

    # ACT - Get token
    response = requests.post(
        f"{c.BASE_URL}/login",
        headers={"accept": "application/json",
                 "Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "user", "password": "user"}
    )

    # ASSERT
    assert response.status_code == status.HTTP_200_OK
    assert "access_token" in response.json()


def test_create_user():
    """
    Ensures a user with the role 'admin' can create users

    IMPORTANT:
    Our current requirements allow admins to create other admins.
    We should probably change that behavior and add a new assertion.

    Asserts:
        - Login as the user 'admin' returns status 200.
        - Deleting a user as the user 'admin' returns status 200 or 404.
        - Creating a new user as the user 'admin' returns status 200.
    """

    # ACT - Login as admin and get the access token
    login_response = requests.post(
        f"{c.BASE_URL}/login",
        headers={"accept": "application/json",
                 "Content-Type": "application/x-www-form-urlencoded"},
        data={"username": "admin", "password": "admin"}
    )
    access_token = login_response.json()["access_token"]

    # Delete the user if it already exists
    delete_user_response = requests.post(
        f"{c.BASE_URL}/delete-user/newuser",
        headers={"accept": "application/json",
                 "Authorization": f"Bearer {access_token}"}
    )

    # ACT - Create a new user using the obtained access token
    new_user_response = requests.post(
        f"{c.BASE_URL}/create-user",
        headers={
            "accept": "application/json", "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}"},
        json={"username": "newuser", "password": "newpassword", "role": "user"}
    )

    # ASSERT
    assert login_response.status_code == status.HTTP_200_OK
    assert delete_user_response.status_code in (status.HTTP_200_OK,
                                                status.HTTP_404_NOT_FOUND)
    assert new_user_response.status_code == status.HTTP_200_OK
