from django.db import models

class Veiculo(models.Model):
    nome = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    dono = models.CharField(max_length=100, default="")
    placa = models.CharField(max_length=7, unique=True)
    cor = models.CharField(max_length=50)
    data_entrada = models.DateTimeField(auto_now_add=True)
    data_saida = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.modelo} ({self.dono})"
    
    @property
    def veiculo_info(self):
        return f"{self.nome} - {self.modelo} ({self.dono}) - {self.placa} - {self.cor}"
    
    def esta_no_patio(self):
        return self.data_saida is None