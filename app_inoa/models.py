from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UsuarioManager(BaseUserManager):
    class Meta:
        db_table = 'usuarios_manager'

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O e-mail é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    class Meta:
        db_table = 'usuarios'
    
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=100, default=make_password('senha_padrao'))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Ativo(models.Model):

    class Meta:
        db_table = 'ativos'

    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    valor_maximo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    valor_minimo = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    periodo_checagem = models.IntegerField(validators=[MinValueValidator(1)], default=5)  # em minutos
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
