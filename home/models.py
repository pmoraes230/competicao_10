from django.db import models
class Cliente(models.Model):
    id_cliente = models.AutoField(db_column='ID_Cliente', primary_key=True)  # Field name made lowercase.
    nome_cliente = models.CharField(db_column='Nome_Cliente', max_length=45)  # Field name made lowercase.
    cpf_cliente = models.CharField(db_column='CPF_Cliente', unique=True, max_length=14)  # Field name made lowercase.
    email_cliente = models.CharField(db_column='Email_Cliente', unique=True, max_length=80)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'cliente'
        
    def __str__(self):
        return self.nome_cliente

class Evento(models.Model):
    id_evento = models.AutoField(db_column='ID_Evento', primary_key=True)  # Field name made lowercase.
    nome_evento = models.CharField(db_column='Nome_Evento', max_length=45)  # Field name made lowercase.
    limitepessoas_evento = models.IntegerField(db_column='LimitePessoas_Evento')  # Field name made lowercase.
    data_evento = models.DateField(db_column='Data_Evento')  # Field name made lowercase.
    horario_evento = models.TimeField(db_column='Horario_Evento')  # Field name made lowercase.
    descricao_evento = models.TextField(db_column='Descricao_Evento')  # Field name made lowercase.
    imagem_evento = models.ImageField(upload_to="event")  # Field name made lowercase.
    usuario_id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='Usuario_ID_Usuario')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'evento'
        
    def __str__(self):
        return self.nome_evento

class Ingresso(models.Model):
    cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='Cliente_ID')  # Field name made lowercase.
    evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='Evento_ID')  # Field name made lowercase.
    setor = models.ForeignKey('Setor', models.DO_NOTHING, db_column='Setor_ID')  # Field name made lowercase.
    id_ingresso = models.CharField(db_column='ID_Ingresso', primary_key=True, max_length=45)  # Field name made lowercase.
    data_emissao_ingresso = models.DateTimeField(db_column='Data_Emissao_Ingresso')  # Field name made lowercase.
    status_ingresso = models.CharField(db_column='Status_Ingresso', max_length=9, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ingresso'
        
    def __str__(self):
        return f"Ingresso para o cliente {self.cliente.nome_cliente} no evento {self.evento.nome_evento}"

class Perfil(models.Model):
    id_perfil = models.AutoField(db_column='ID_Perfil', primary_key=True)  # Field name made lowercase.
    nome_perfil = models.CharField(db_column='Nome_Perfil', max_length=45)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'perfil'
    
    def __str__(self):
        return self.nome_perfil

class Setor(models.Model):
    id_setor = models.AutoField(db_column='ID_Setor', primary_key=True)  # Field name made lowercase.
    nome_setor = models.CharField(db_column='Nome_Setor', max_length=45)  # Field name made lowercase.
    limite_setor = models.IntegerField(db_column='LImite_Setor')  # Field name made lowercase.
    preco_setor = models.DecimalField(db_column='Preco_Setor', max_digits=10, decimal_places=2)  # Field name made lowercase.
    evento_id_evento = models.ForeignKey(Evento, models.DO_NOTHING, db_column='Evento_ID_Evento')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'setor'
        
    def __str__(self):
        return self.nome_setor

class Usuario(models.Model):
    id_usuario = models.AutoField(db_column='ID_Usuario', primary_key=True)  # Field name made lowercase.
    nome_usuario = models.CharField(db_column='Nome_Usuario', max_length=45)  # Field name made lowercase.
    email_usuario = models.CharField(db_column='Email_Usuario', unique=True, max_length=80)  # Field name made lowercase.
    cpf_usuario = models.CharField(db_column='CPF_Usuario', unique=True, max_length=14)  # Field name made lowercase.
    senha_usuario = models.CharField(db_column='Senha_Usuario', unique=True, max_length=130)  # Field name made lowercase.
    perfil = models.ForeignKey(Perfil, models.DO_NOTHING, db_column='Perfil_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'usuario'

    def __str__(self):
        return self.nome_usuario