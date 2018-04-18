from rest_framework import viewsets, permissions, mixins, generics
from .models import Staff,EmailVerifycode
from .permissions import IndenticalUserOrReadOnly
from . import permissions as user_permissions
from .serializers import StaffSerializer, JSONWebTokenSerializer, RefreshJSONWebTokenSerializer,EmailVerifycodeSerializer,ResetStaffSerializer
from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import list_route
# from utils import email_send

class CreateStaffView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Staff.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = StaffSerializer

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({"status": -1, "msg": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)  
    

    

class StaffViewSet(mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    permission_classes = (user_permissions.IndenticalUserOrReadOnly, )

    @list_route(methods=['get'], url_path='exist_email', permission_classes=[IndenticalUserOrReadOnly])
    def email_exists(self, request):
        email = request.GET['email']
        staff = Staff.objects.filter(email__iregex=r'^' + email +"$").first()
        if not staff:
            return Response({"status": 0})
        else:
            return Response({"status": -1, "msg": 'Email existed'})

    @list_route(methods=['get'], url_path='exist_username', permission_classes=[IndenticalUserOrReadOnly])
    def username_exists(self, request):
        username = request.GET['username']
        staff = Staff.objects.filter(username__iregex=r'^' + username +"$").first()
        if not staff:
            return Response({"status": 0})
        else:
            return Response({"status": -1, "msg": 'Username existed'})

    @list_route(methods=['get'], url_path='my_roles', permission_classes=[IndenticalUserOrReadOnly])
    def roles(self, request):
        return {
            'staff': StaffSerializer(staff, context={'request': request}).data
        }
    @list_route(methods=['post'], url_path='api-vericode', permission_classes=[IndenticalUserOrReadOnly])    
    def email_vericode(self, request):
        return Response({"status": -1, "msg": 'Failed'})


class ObtainJSONWebToken(JSONWebTokenAPIView):
    """
    API View that receives a POST with a user's username and password.
    Returns a JSON Web Token that can be used for authenticated requests.
    """
    serializer_class = JSONWebTokenSerializer


class RefreshJSONWebToken(JSONWebTokenAPIView):
    """
    API View that returns a refreshed token (with new expiration) based on
    existing token
    If 'orig_iat' field (original issued-at-time) is found, will first check
    if it's within expiration window, then copy it to the new token
    """
    serializer_class = RefreshJSONWebTokenSerializer

class EmailVerifycodeView(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = EmailVerifycode.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = EmailVerifycodeSerializer

    def post(self, request, *args, **kwargs):
        try:
            return self.create(request, *args, **kwargs)
        except Exception as e:
            return Response({"status": -1, "msg": str(e)}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
class ResetStaffView(mixins.CreateModelMixin,mixins.UpdateModelMixin, generics.GenericAPIView):
    queryset = Staff.objects.all()
    permission_classes = (permissions.AllowAny, )
    serializer_class = ResetStaffSerializer 

    def put(self, request, *args, **kwargs):
        params = request.data
        email, verify_code, password = params['email'], params['vericode'], params['password']
        codes = EmailVerifycode.objects.filter(email=email, code=verify_code)
        if len(codes) > 0:
            codes.delete()
            staff = Staff.objects.get(email=email)
            staff.set_password(password)
            staff.save()
            return Response({'status':0, 'msg':'成功'})
        else:
            return Response({'status':'-1', 'msg':'验证码错误'}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

register_user = CreateStaffView.as_view()
obtain_jwt_token = ObtainJSONWebToken.as_view()
refresh_jwt_token = RefreshJSONWebToken.as_view()
email_vericode = EmailVerifycodeView.as_view()
reset_password = ResetStaffView.as_view()


