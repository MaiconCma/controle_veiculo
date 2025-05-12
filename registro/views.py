from datetime import datetime, time
from tkinter import Canvas  # Importa datetime e time para usar combine() e time.min/time.max
from django.http import HttpResponse
from django.utils import timezone     # Permite usar timezone.now() e timezone.localtime()
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from django.db.models import Q         # Importa Q diretamente para as consultas
from .forms import SaidaForm, VeiculoForm, RelatorioForm
from .models import Veiculo
from reportlab.pdfgen import canvas


def painel_principal(request):
    veiculos_no_patio = Veiculo.objects.filter(data_saida__isnull=True)
    veiculos_saida = Veiculo.objects.filter(data_saida__isnull=False)
    return render(request, 'registro/painel_principal.html', {
        'veiculos_no_patio': veiculos_no_patio,
        'veiculos_saida': veiculos_saida
    })

def registrar_entrada(request):
    if request.method == 'POST':
        form = VeiculoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('painel_principal')
    else:
        form = VeiculoForm()
    return render(request, 'registro/registrar_entrada.html', {'form': form})

def registrar_saida(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    
    if request.method == 'POST':
        veiculo.data_saida = timezone.now()  # Define a data e hora atuais automaticamente
        veiculo.save()
        return redirect('painel_principal')
    
    return render(request, 'registro/registrar_saida.html', {'veiculo': veiculo})

def veiculo_detalhes(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    return render(request, 'registro/veiculo_detalhes.html', {'veiculo': veiculo})

class RelatorioView(ListView):
    model = Veiculo
    template_name = 'registro/relatorio.html'
    context_object_name = 'veiculos'
    
    def get_queryset(self):
        form = RelatorioForm(self.request.GET)
        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']
            # Converte as datas para abranger o dia completo:
            inicio = datetime.combine(data_inicial, time.min)
            fim = datetime.combine(data_final, time.max)
            return Veiculo.objects.filter(data_entrada__range=[inicio, fim])
        return Veiculo.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Converte os datetimes dos veículos para o horário local e adiciona novos atributos
        veiculos = context['veiculos']
        for veiculo in veiculos:
            veiculo.data_entrada_local = timezone.localtime(veiculo.data_entrada)
            if veiculo.data_saida:
                veiculo.data_saida_local = timezone.localtime(veiculo.data_saida)
            else:
                veiculo.data_saida_local = None
        
        context['form'] = RelatorioForm(self.request.GET or None)
        context['total_veiculos'] = veiculos.count()
        return context

def buscar_veiculos(request):
    query = request.GET.get('q')
    if query:
        veiculos = Veiculo.objects.filter(
            Q(nome__icontains=query) | Q(placa__icontains=query)
        )
    else:
        veiculos = Veiculo.objects.all()
    return render(request, 'registro/buscar_veiculos.html', {'veiculos': veiculos})

def editar_veiculo(request, veiculo_id):
    veiculo = get_object_or_404(Veiculo, id=veiculo_id)
    if request.method == 'POST':
        form = VeiculoForm(request.POST, instance=veiculo)
        if form.is_valid():
            form.save()
            return redirect('painel_principal')
    else:
        form = VeiculoForm(instance=veiculo)
    return render(request, 'registro/editar_veiculo.html', {'form': form, 'veiculo': veiculo})

class RelatorioPDFView(View):
    def get(self, request, *args, **kwargs):
        # Utiliza o mesmo filtro do relatório (se os parâmetros estiverem presentes)
        form = RelatorioForm(request.GET)
        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']
            inicio = datetime.combine(data_inicial, time.min)
            fim = datetime.combine(data_final, time.max)
            veiculos = Veiculo.objects.filter(data_entrada__range=[inicio, fim])
        else:
            veiculos = Veiculo.objects.all()

        # Prepara a resposta do PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="relatorio.pdf"'

        p = canvas.Canvas(response)
        # Cabeçalho do PDF
        p.setFont("Helvetica-Bold", 16)
        p.drawString(50, 800, "Relatório de Veículos")
        p.setFont("Helvetica", 12)
        p.drawString(50, 780, f"Total de veículos: {veiculos.count()}")

        # Cabeçalho da 'tabela'
        y = 760
        p.drawString(50, y, "Nome")
        p.drawString(150, y, "Modelo")
        p.drawString(250, y, "Dono")
        p.drawString(300, y, "Placa")
        p.drawString(380, y, "Entrada")
        p.drawString(500, y, "Saída")
        y -= 20

        # Para cada veículo, adiciona uma linha no PDF
        for veiculo in veiculos:
            data_entrada_local = timezone.localtime(veiculo.data_entrada).strftime("%d/%m/%Y %H:%M")
            data_saida_local = (
                timezone.localtime(veiculo.data_saida).strftime("%d/%m/%Y %H:%M")
                if veiculo.data_saida else "Em Pátio"
            )
            p.drawString(50, y, str(veiculo.nome))
            p.drawString(150, y, str(veiculo.modelo))
            p.drawString(250, y, str(veiculo.dono))
            p.drawString(300, y, str(veiculo.placa))
            p.drawString(380, y, data_entrada_local)
            p.drawString(500, y, data_saida_local)
            y -= 20

            # Cria nova página se necessário
            if y < 50:
                p.showPage()
                y = 800

        p.showPage()
        p.save()
        return response