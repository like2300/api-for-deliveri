from django.shortcuts import render
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import CompanyConfig, Boutique, Slider, Product, Category, VendorUser
from .serializers import (
    CompanyConfigSerializer, BoutiqueSerializer, SliderSerializer, 
    ProductSerializer, CategorySerializer, VendorUserSerializer, LoginSerializer
)


class IsVendorOwner(BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Check if the object has a boutique attribute
        if hasattr(obj, 'boutique'):
            return obj.boutique.owner == request.user
        # For Boutique objects specifically
        elif isinstance(obj, Boutique):
            return obj.owner == request.user
        return False


class LoginView(APIView):
    """
    View to handle vendor login
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        
        # Log the user in
        login(request, user)
        
        # Return user data
        vendor_serializer = VendorUserSerializer(user)
        return Response({
            'user': vendor_serializer.data,
            'message': 'Connexion réussie'
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    View to handle vendor logout
    """
    def post(self, request):
        logout(request)
        return Response({'message': 'Déconnexion réussie'}, status=status.HTTP_200_OK)


class VendorDashboardView(APIView):
    """
    View to get vendor-specific data for dashboard
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if hasattr(request.user, 'boutique'):
            boutique = request.user.boutique
            boutique_serializer = BoutiqueSerializer(boutique)
            return Response(boutique_serializer.data)
        else:
            return Response({'error': 'Aucune boutique associée à cet utilisateur'}, status=status.HTTP_404_NOT_FOUND)


class VendorProductListView(generics.ListCreateAPIView):
    """
    View to list and create products for the authenticated vendor
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'boutique'):
            return Product.objects.filter(boutique=self.request.user.boutique)
        return Product.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'boutique'):
            serializer.save(boutique=self.request.user.boutique)
        else:
            raise serializers.ValidationError('Aucune boutique associée à cet utilisateur')


class VendorProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a specific product for the authenticated vendor
    """
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwner]

    def get_queryset(self):
        if hasattr(self.request.user, 'boutique'):
            return Product.objects.filter(boutique=self.request.user.boutique)
        return Product.objects.none()


class VendorCategoryListView(generics.ListCreateAPIView):
    """
    View to list and create categories for the authenticated vendor
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if hasattr(self.request.user, 'boutique'):
            return Category.objects.filter(boutique=self.request.user.boutique)
        return Category.objects.none()

    def perform_create(self, serializer):
        if hasattr(self.request.user, 'boutique'):
            serializer.save(boutique=self.request.user.boutique)
        else:
            raise serializers.ValidationError('Aucune boutique associée à cet utilisateur')


class VendorCategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a specific category for the authenticated vendor
    """
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsVendorOwner]

    def get_queryset(self):
        if hasattr(self.request.user, 'boutique'):
            return Category.objects.filter(boutique=self.request.user.boutique)
        return Category.objects.none()


class ChangePasswordView(APIView):
    """
    View to allow vendors to change their password
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        # Check if old password is correct
        if not user.check_password(old_password):
            return Response(
                {'error': 'Ancien mot de passe incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(new_password)
        user.save()

        return Response(
            {'message': 'Mot de passe modifié avec succès'},
            status=status.HTTP_200_OK
        )


# Public API views (for customers)
class PublicProductListView(generics.ListAPIView):
    """
    Public view to list all products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class PublicBoutiqueListView(generics.ListAPIView):
    """
    Public view to list all boutiques
    """
    queryset = Boutique.objects.all()
    serializer_class = BoutiqueSerializer
    permission_classes = [permissions.AllowAny]


class PublicSliderListView(generics.ListAPIView):
    """
    Public view to list all sliders
    """
    queryset = Slider.objects.all()
    serializer_class = SliderSerializer
    permission_classes = [permissions.AllowAny]


class PublicCompanyConfigView(generics.RetrieveAPIView):
    """
    Public view to get company config
    """
    queryset = CompanyConfig.objects.all()
    serializer_class = CompanyConfigSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_object(self):
        # Return the first (and typically only) company config
        return CompanyConfig.objects.first()


@api_view(['GET'])
@permission_classes([AllowAny])
def init_app_data_view(request):
    """
    View that returns all necessary data for the WhatsApp Commerce app:
    - Company configuration
    - Sliders
    - Boutiques
    - Products
    """
    # Get company config (assuming there's only one for now)
    company_config = CompanyConfig.objects.first()
    company_serializer = CompanyConfigSerializer(company_config) if company_config else None

    # Get all sliders
    sliders = Slider.objects.all()
    slider_serializer = SliderSerializer(sliders, many=True)

    # Get all boutiques with their associated products
    boutiques = Boutique.objects.all()
    boutique_serializer = BoutiqueSerializer(boutiques, many=True)

    # Get all products
    products = Product.objects.all()
    product_serializer = ProductSerializer(products, many=True)

    data = {
        'company_config': company_serializer.data if company_serializer else None,
        'sliders': slider_serializer.data,
        'boutiques': boutique_serializer.data,
        'products': product_serializer.data
    }

    return Response(data)
