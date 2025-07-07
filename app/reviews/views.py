from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from reviews.models import Country, Manufacturer, Car, Comment
from reviews.serializers import (
    CountrySerializer,
    ManufacturerSerializer,
    CarSerializer,
    CommentSerializer
)
import pandas as pd
from django.http import HttpResponse
from rest_framework.authentication import TokenAuthentication
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseBadRequest
from rest_framework_csv.renderers import CSVRenderer
from drf_excel.renderers import XLSXRenderer
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.permissions import AllowAny
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class IsAdminToken(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.auth is not None
    
class IndexView(TemplateView):
    template_name = "index.html"

class ExportMixin:
    def _export_data(self, queryset, fields, filename, fmt):
        df = pd.DataFrame(list(queryset.values(*fields)))

        if fmt == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            df.to_csv(path_or_buf=response, index=False)
            return response

        elif fmt == 'xlsx':
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
            df.to_excel(response, index=False)
            return response

        else:
            return HttpResponseBadRequest("Unsupported format. Use 'csv' or 'xlsx'.")

class ObtainAuthTokenCustom(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
class CountryViewSet(viewsets.ModelViewSet, ExportMixin):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CSVRenderer, XLSXRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'export_csv': [permissions.AllowAny],
        'export_xlsx': [permissions.AllowAny],
        'create': [permissions.IsAdminUser],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    queryset = Country.objects.all().order_by('id')

    def get_permissions(self):
        return [perm() for perm in
                self.permission_classes_by_action.get(self.action,
                                                     [permissions.IsAuthenticated])]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return self._export_data(self.get_queryset(), ['id', 'name'], 'countries', 'csv')

    @action(detail=False, methods=['get'])
    def export_xlsx(self, request):
        return self._export_data(self.get_queryset(), ['id', 'name'], 'countries', 'xlsx')

class CustomAPIRootView(APIView):
    def get(self, request, format=None):
        return Response({
            "countries": reverse('country-list', request=request, format=format),
            "manufacturers": reverse('manufacturer-list', request=request, format=format),
            "cars": reverse('car-list', request=request, format=format),
            "comments": reverse('comment-list', request=request, format=format),
            "get_token": reverse('api-token', request=request, format=format),
        })

class ManufacturerViewSet(viewsets.ModelViewSet, ExportMixin):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CSVRenderer, XLSXRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'export_csv': [permissions.AllowAny],
        'export_xlsx': [permissions.AllowAny],
        'create': [permissions.IsAdminUser],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    queryset = Manufacturer.objects.all().order_by('id')

    def get_permissions(self):
        return [perm() for perm in
                self.permission_classes_by_action.get(self.action,
                                                     [permissions.IsAuthenticated])]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return self._export_data(self.get_queryset(), ['id', 'name', 'country_id'], 'manufacturers', 'csv')

    @action(detail=False, methods=['get'])
    def export_xlsx(self, request):
        return self._export_data(self.get_queryset(), ['id', 'name', 'country_id'], 'manufacturers', 'xlsx')


class CarViewSet(viewsets.ModelViewSet, ExportMixin):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CSVRenderer, XLSXRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'export_csv': [permissions.AllowAny],
        'export_xlsx': [permissions.AllowAny],
        'create': [permissions.IsAdminUser],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['manufacturer__name', 'start_year', 'end_year']
    search_fields = ['name']
    queryset = Car.objects.all().order_by('id')

    def get_permissions(self):
        return [perm() for perm in
                self.permission_classes_by_action.get(self.action,
                                                     [permissions.IsAuthenticated])]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return self._export_data(
            self.get_queryset(),
            ['id', 'name', 'manufacturer_id', 'start_year', 'end_year'],
            'cars',
            'csv'
        )

    @action(detail=False, methods=['get'])
    def export_xlsx(self, request):
        return self._export_data(
            self.get_queryset(),
            ['id', 'name', 'manufacturer_id', 'start_year', 'end_year'],
            'cars',
            'xlsx'
        )


class CommentViewSet(viewsets.ModelViewSet, ExportMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer, CSVRenderer, XLSXRenderer]
    authentication_classes = [TokenAuthentication]
    permission_classes_by_action = {
        'list': [permissions.AllowAny],
        'retrieve': [permissions.AllowAny],
        'export_csv': [permissions.AllowAny],
        'export_xlsx': [permissions.AllowAny],
        'create': [permissions.AllowAny],
        'update': [permissions.IsAdminUser],
        'destroy': [permissions.IsAdminUser],
    }
    queryset = Comment.objects.all().order_by('created_at')
    
    def get_permissions(self):
        return [perm() for perm in
                self.permission_classes_by_action.get(self.action,
                                                     [permissions.IsAuthenticated])]

    @action(detail=False, methods=['get'])
    def export_csv(self, request):
        return self._export_data(self.get_queryset(),
                                 ['id', 'email', 'car_id', 'created_at', 'content'],
                                 'comments',
                                 'csv')

    @action(detail=False, methods=['get'])
    def export_xlsx(self, request):
        return self._export_data(self.get_queryset(),
                                 ['id', 'email', 'car_id', 'created_at', 'content'],
                                 'comments',
                                 'xlsx')