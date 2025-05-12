from django import forms
from .models import Veiculo
from django.forms import ModelForm

class VeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['nome', 'modelo', 'dono', 'placa', 'cor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'dono': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Veículo',
            'modelo': 'Modelo',
            'dono': 'Dono',
            'placa': 'Placa',
            'cor': 'Cor',
        }
class SaidaForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['data_saida']
        widgets = {
            'data_saida': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
        labels = {
            'data_saida': 'Data de Saída',
        }

class RelatorioForm(forms.Form):
    data_inicial = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
    data_final = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))

class BuscarVeiculoForm(forms.Form):
    query = forms.CharField(label='Buscar Veículo', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome ou placa do veículo'}))

class EditarVeiculoForm(ModelForm):
    class Meta:
        model = Veiculo
        fields = ['nome', 'modelo', 'dono', 'placa', 'cor']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'modelo': forms.TextInput(attrs={'class': 'form-control'}),
            'dono': forms.TextInput(attrs={'class': 'form-control'}),
            'placa': forms.TextInput(attrs={'class': 'form-control'}),
            'cor': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Veículo',
            'modelo': 'Modelo',
            'dono': 'Dono',
            'placa': 'Placa',
            'cor': 'Cor',
        }

