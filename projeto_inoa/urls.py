from django.contrib import admin
from django.urls import path
from app_inoa import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('cadastrar_usuario/', views.cadastrar_usuario, name='cadastrar_usuario'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('monitoramento/', views.usuario_monitoramento, name='monitoramento'),
    path('cadastrar_ativo/', views.cadastrar_ativo, name='cadastrar_ativo'),
    path('buscar_ativos/', views.buscar_ativos, name='buscar_ativos'),
    path('editar_ativo/', views.editar_ativo, name='editar_ativo'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('excluir_ativo/', views.excluir_ativo, name='excluir_ativo'),
    path('iniciar_monitoramento/', views.iniciar_monitoramento, name='iniciar_monitoramento'),
    path('parar_monitoramento/', views.parar_monitoramento, name='parar_monitoramento'),
    path('get_ativo_grafico/<int:ativo_id>/', views.get_ativo_grafico, name='get_ativo_grafico'),
]
