from rest_framework import generics, permissions, filters
from .models import Patient, HeartRate
from .serializers import PatientSerializer, HeartRateSerializer, UserRegisterSerializer
from rest_framework.exceptions import PermissionDenied


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]


# Patients
class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Patient.objects.all()
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name"]
    ordering_fields = ["created_at", "first_name"]

    def get_queryset(self):
        # users can see only their created patients, or all if staff
        user = self.request.user
        qs = super().get_queryset()
        if user.is_staff:
            return qs
        return qs.filter(created_by=user)


class PatientRetrieveView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Patient.objects.all()

    def get_object(self):
        obj = super().get_object()
        if not self.request.user.is_staff and obj.created_by != self.request.user:
            raise PermissionDenied("You are not allowed to access this patient")
        return obj


# Heart rates
class HeartRateCreateView(generics.CreateAPIView):
    serializer_class = HeartRateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # ensure user has access to the patient
        patient = serializer.validated_data["patient"]
        if not (self.request.user.is_staff or patient.created_by == self.request.user):
            raise PermissionDenied("Not allowed to add readings for this patient")
        serializer.save()


class HeartRateListView(generics.ListAPIView):
    serializer_class = HeartRateSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["recorded_at", "bpm"]
    search_fields = ["note"]

    def get_queryset(self):
        patient_id = self.request.query_params.get("patient")
        qs = HeartRate.objects.all()
        if patient_id:
            qs = qs.filter(patient_id=patient_id)
        if not self.request.user.is_staff:
            qs = qs.filter(patient__created_by=self.request.user)
        return qs
