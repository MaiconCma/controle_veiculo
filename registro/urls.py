# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.painel_principal, name='painel_principal'),
    path('registrar_entrada/', views.registrar_entrada, name='registrar_entrada'),
    path('registrar_saida/<int:veiculo_id>/', views.registrar_saida, name='registrar_saida'),
    path('veiculo_detalhes/<int:veiculo_id>/', views.veiculo_detalhes, name='veiculo_detalhes'),
    path('relatorio/', views.RelatorioView.as_view(), name='relatorio'),
    path('relatorio/pdf/', views.RelatorioPDFView.as_view(), name='relatorio_pdf'),
    path('buscar_veiculos/', views.buscar_veiculos, name='buscar_veiculos'),
    path('editar_veiculo/<int:veiculo_id>/', views.editar_veiculo, name='editar_veiculo'),
]
