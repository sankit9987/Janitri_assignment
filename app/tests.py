from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from django.utils import timezone
from .models import Patient, HeartRate


class AuthTests(APITestCase):
    """Tests for registration and JWT token retrieval."""

    def test_register_and_token_obtain(self):
        # Register a new user
        response = self.client.post(
            reverse("register"),
            {
                "username": "tester",
                "email": "test@example.com",
                "password": "StrongPass123",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Obtain JWT token
        token_response = self.client.post(
            "/api/auth/token/", {"username": "tester", "password": "StrongPass123"}
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertIn("access", token_response.data)
        self.assertIn("refresh", token_response.data)


class PatientHeartRateTests(APITestCase):
    """Tests for creating patients and heart-rate records."""

    def setUp(self):
        # Create a user and authenticate with JWT
        self.user = User.objects.create_user(username="u1", password="pw123456")
        token = self.client.post(
            "/api/auth/token/", {"username": "u1", "password": "pw123456"}
        ).data["access"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_and_list_patients(self):
        # Create a patient
        response = self.client.post(
            reverse("patients-list-create"),
            {"first_name": "John", "last_name": "Doe", "date_of_birth": "1990-01-01"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        patient_id = response.data["id"]

        # List patients (should contain the created patient)
        list_response = self.client.get(reverse("patients-list-create"))
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        ids = [p["id"] for p in list_response.data["results"]]
        self.assertIn(patient_id, ids)

    def test_retrieve_patient(self):
        # Create a patient and retrieve it
        patient = Patient.objects.create(first_name="Jane", created_by=self.user)
        url = reverse("patient-detail", args=[patient.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], "Jane")

    def test_add_and_list_heart_rate(self):
        # Create patient
        patient = Patient.objects.create(first_name="Alice", created_by=self.user)

        # Add a heart-rate record
        hr_response = self.client.post(
            reverse("heartrate-create"),
            {
                "patient": patient.id,
                "bpm": 75,
                "recorded_at": timezone.now().isoformat(),
            },
        )
        self.assertEqual(hr_response.status_code, status.HTTP_201_CREATED)

        # List heart-rate records for the patient
        list_response = self.client.get(
            reverse("heartrate-list") + f"?patient={patient.id}"
        )
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(list_response.data["results"]), 1)

    def test_invalid_bpm_validation(self):
        # Create patient
        patient = Patient.objects.create(first_name="Bob", created_by=self.user)

        # Attempt to create invalid heart-rate record
        bad_response = self.client.post(
            reverse("heartrate-create"),
            {
                "patient": patient.id,
                "bpm": 10,  # invalid bpm
                "recorded_at": timezone.now().isoformat(),
            },
        )
        self.assertEqual(bad_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("bpm", bad_response.data)
