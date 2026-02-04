from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import CompanyConfig, Boutique, Slider, Product
from .serializers import CompanyConfigSerializer, BoutiqueSerializer, SliderSerializer, ProductSerializer


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
