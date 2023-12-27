from config import config as c
from datetime import datetime
import requests
from fastapi import status

# ARRANGE (globally)
# -----------------------------------------------------------------------------

# Get the access token for user 1
TOKEN_USER_1 = requests.post(f"{c.BASE_URL}/login", data={
    "username": "user",
    "password": "user",
}).json().get("access_token", "")
HEADERS_USER_1 = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN_USER_1}"
}

# Get the access token for user 2
TOKEN_USER_2 = requests.post(f"{c.BASE_URL}/login", data={
    "username": "user2",
    "password": "user2",
}).json().get("access_token", "")
HEADERS_USER_2 = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TOKEN_USER_2}"
}

# Set payload
ECG_DATA_1 = {
    "date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    "leads": [
        {
            "name": "Lead III",
            "samples": 3,
            "signal": [7, 8, 9]
        }
    ]
}


# ACT AND ASSERT
# -----------------------------------------------------------------------------
def test_post_ecg():
    """
    Test the /post-ecg endpoint.

    asserts:
        - A user can successfully post a ecg.
        - The success message "ECG received successfully" is present in the
          response JSON.
    """

    # ACT
    response = requests.post(f"{c.BASE_URL}/post-ecg",
                             json=ECG_DATA_1, headers=HEADERS_USER_1)

    # ASSERT
    assert response.status_code == status.HTTP_200_OK, \
        f"Expected 200, but got {response.status_code}"
    assert "ECG received successfully" in response.json().get("message", "")


def test_get_ecg():
    """
    Test the /get-ecg/{ecg_id} endpoint.

    This test will fail if the users 'user' and 'user2' do not exist
    in the DB so make sure you are creating them on startup.
    We keep it this way to avoid potential security risks resulting
    from running tests with a user with the 'admin' role.

    Asserts:
        - A user can create a ecg.
        - A user different than the one who created the ecg is not able to
          access it.
    """

    # ACT - Try to get a ecg posted by user1 with the token of user2
    response_user1 = requests.post(f"{c.BASE_URL}/post-ecg",
                                   json=ECG_DATA_1, headers=HEADERS_USER_1)
    ecg_id_user1 = response_user1.json().get("ecg_id")

    response_user2 = requests.get(
        f"{c.BASE_URL}/get-ecg/{ecg_id_user1}", headers=HEADERS_USER_2)

    # Assert
    assert response_user1.status_code == status.HTTP_200_OK, \
        f"Failed to create ECG for user 1: {response_user1.content}"
    assert response_user2.status_code == status.HTTP_403_FORBIDDEN, \
        f"Unexpected status code: {response_user2.status_code}. User 2 should not have permission to access ECG created by user 1"


def test_get_ecg_not_found():
    """
    Test the /get-ecg/{ecg_id} endpoint case where the ECG is not found.

    Asserts:
        - The response status code is 404 when attempting to retrieve
          a nonexistent ECG.
        - The response JSON contains the expected detail message
          "ECG not found."
    """

    # ACT
    ecg_id = "nonexistent_ecg_id"
    response = requests.get(
        f"{c.BASE_URL}/get-ecg/{ecg_id}", headers=HEADERS_USER_1)

    # ASSERT
    assert response.status_code == status.HTTP_404_NOT_FOUND, \
        f"Expected 404, but got {response.status_code}"
    assert response.json() == {"detail": "ECG not found"}
