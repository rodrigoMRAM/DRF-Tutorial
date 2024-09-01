from rest_framework import generics, mixins, permissions, authentication
from django.views.generic.detail import DetailView
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from django.http import Http404
from django.shortcuts import get_object_or_404
from api.mixins import (
    StaffEditorPermissionMixin,
    UserQuerySetMixin)

from .models import Product
from .serializers import ProductSerializer

# RETRIEVE SE UTILIZA PARA RECUPERAR UN CONJUNTO DE DATOS O UNO SOLO , ES COMO USAR EL @API_VIEW PERO EN CLASES
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # SOLO SE PUEDE ACCEDER SI ESTA AUTENTICADO 
    authentication_classes = [authentication.SessionAuthentication  ]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# VISTA GENERICA PARA CREAR VISTAS
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ES PARA GET Y POST OBTIENE LISTA Y TAMBIEN CREA UN NUEVO OBJETO
class ProductListCreateAPIViewAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
# ES GET Y TRAE LISTA DE DATOS
class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# UPDATE
class ProductUpdateAPIView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # ES EN QUE SE VA A BASAR LA BUSQUEDA DEL ID
    lookup_field = 'pk'
    # MODIFICACION DEL COMPORTAMIENTO DE LA ACTUALIZACION EN ESTE CASO SI NO HAY CONTET, EL CONTENT = A TITLE
    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title

class ProductDestroyAPIView(generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # ES EN QUE SE VA A BASAR LA BUSQUEDA DEL ID
    lookup_field = 'pk'
    # MODIFICACION DEL COMPORTAMIENTO DE LA ACTUALIZACION EN ESTE CASO SI NO HAY CONTET, EL CONTENT = A TITLE
    def perform_destroy(self, instance):
        return super().perform_destroy(instance)




#EL EQUIVALENTE A RETRIEVEAPIVIEW
@api_view(["GET"])
def getTables(request,id):
    tables = Product.objects.filter(identificacion=id)
    serializar = ProductSerializer(tables, many=True)
    print(tables)
    return Response(serializar.data)




class ProductListCreateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # SOBREESCRIBE LOS DATOS MODIFICANDOLOS A GUSTO
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        #OBTIENE EL TITLE VALIDATED_DATA ES DONDE SE ALMACENAN LOS DATOS DE SERIALIZER CUANDO PASAN LAS VALIDACIONES CORRESPONDIENTES DEL SERIALIZER
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        # ACA ESTA IGUALANDO CONTENT = TITLE Y MAS ABAJO LO GUARDA
        if content is None:
            content = title
        serializer.save(user=self.request.user, content=content)
        # send a Django signal
    
    # def get_queryset(self, *args, **kwargs):
    #     qs = super().get_queryset(*args, **kwargs)
    #     request = self.request
    #     user = request.user
    #     if not user.is_authenticated:
    #         return Product.objects.none()
    #     # print(request.user)
    #     return qs.filter(user=request.user)


product_list_create_view = ProductListCreateAPIView.as_view()

class ProductDetailAPIView(
    UserQuerySetMixin, 
    StaffEditorPermissionMixin,
    generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = 'pk' ??

product_detail_view = ProductDetailAPIView.as_view()


class ProductUpdateAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_update(self, serializer):
        instance = serializer.save()
        if not instance.content:
            instance.content = instance.title
            ## 

product_update_view = ProductUpdateAPIView.as_view()


class ProductDestroyAPIView(
    UserQuerySetMixin,
    StaffEditorPermissionMixin,
    generics.DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def perform_destroy(self, instance):
        # instance 
        super().perform_destroy(instance)

product_destroy_view = ProductDestroyAPIView.as_view()

# class ProductListAPIView(generics.ListAPIView):
#     '''
#     Not gonna use this method
#     '''
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# product_list_view = ProductListAPIView.as_view()

# ES COMO LA FUNCION DE ABAJO product_alt_view PERO EN VEZ DE USAR CONDICIONALES 
#SE USAN LAS FUNCIONES DE GET POST, CADA MIXIN CORRESPONDE 
#A CADA FUNCION DEL CRUD, CREATE, LIST, RETRIEVE
class ProductMixinView(
    mixins.CreateModelMixin,  # ESTE MIXIN TIENE LA FUNCION DE CREAR , LA CUAL ESTA INCLUIDO EN ListCreateAPIView
    mixins.ListModelMixin, # ESTE MIXIN TIENE LA FUNCION DE EN LISTAR 
    mixins.RetrieveModelMixin, # ESTE MIXIN TIENE  LA FUNCION DE RECUPERAR 
    generics.GenericAPIView  # Y ESTA ES UNA VISTA GENERICA A LA CUAL TIENE LOS VALORES ANTERIORES EN EL CUAL SE PUEDE CREAR VER Y RECUPERAR DATOS
    ):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'pk'

    def get(self, request, *args, **kwargs): #HTTP -> get
        # EN LOS KWARS ESTAMOS RECIBIENDO EL ID POR LA URL O MAS BIEN EL PK
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        title = serializer.validated_data.get('title')
        content = serializer.validated_data.get('content') or None
        if content is None:
            content = "this is a single view doing cool stuff"
        serializer.save(content=content)

    # def post(): #HTTP -> post

product_mixin_view = ProductMixinView.as_view()


# CREAR UNA FUNCION QUE TENGA GET Y POST A LA VEZ DEPENDIENDO EL FORM
@api_view(['GET', 'POST'])
def product_alt_view(request, pk=None, *args, **kwargs):
    method = request.method  
    # SI ES GET ->
    if method == "GET":
        if pk is not None:
            # detail view
            # OBTENIENDO EL MODEL
            obj = get_object_or_404(Product, pk=pk)
            #SERIALIZANDO 
            data = ProductSerializer(obj, many=False).data
            # RESPUESTA
            return Response(data)
        # list view
        # SINO MUESTRA LA LISTA DE TODOS LOS PRODUCTOS
        queryset = Product.objects.all() 
        data = ProductSerializer(queryset, many=True).data
        return Response(data)
    # SI EL METODO ES POST
    if method == "POST":
        # create an item
        #OBTENIENDO LA DATA Y SERIALIZANDO
        serializer = ProductSerializer(data=request.data)
        # validando y si hay error SE PUEDE MANEJAR EL ERROR VALIDATIONERROR 
        if serializer.is_valid(raise_exception=True):
            title = serializer.validated_data.get('title')
            content = serializer.validated_data.get('content') or None
            #ARRIBA SE OBTEIENE EL CONTENIDO DE TITLE Y CONTENT, SI NO HAY CONTENIDO SE EJECUTA LO DE ABAJO, CONTENIDO SERA IGUAL A TITLE
            if content is None:
                content = title
                # GUARDAMOS
            serializer.save(content=content)
            # DEVOLVEMOS RESPUESTA
            return Response(serializer.data)
        # SI EL SERIALIZER IS NOT VALID , SE EJECUTA ESTO
        return Response({"invalid": "not good data"}, status=400)

class VerLista(DetailView):
    model = Product
    template_name = ""