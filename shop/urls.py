from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('login/', views.LoginView.as_view(), name='vendor-login'),
    path('logout/', views.LogoutView.as_view(), name='vendor-logout'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Vendor dashboard URLs
    path('dashboard/', views.VendorDashboardView.as_view(), name='vendor-dashboard'),
    path('products/', views.VendorProductListView.as_view(), name='vendor-products'),
    path('products/<int:pk>/', views.VendorProductDetailView.as_view(), name='vendor-product-detail'),
    path('categories/', views.VendorCategoryListView.as_view(), name='vendor-categories'),
    path('categories/<int:pk>/', views.VendorCategoryDetailView.as_view(), name='vendor-category-detail'),
    
    # Public URLs
    path('init-app-data/', views.init_app_data_view, name='init-app-data'),
    path('public/products/', views.PublicProductListView.as_view(), name='public-products'),
    path('public/boutiques/', views.PublicBoutiqueListView.as_view(), name='public-boutiques'),
    path('public/sliders/', views.PublicSliderListView.as_view(), name='public-sliders'),
    path('public/config/', views.PublicCompanyConfigView.as_view(), name='public-config'),
]