# Generated by Django 3.0.5 on 2020-04-06 12:45

import apps.user.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0011_update_proxy_permissions"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        error_messages={
                            "unique": "Já existe um usuario cadastrado com este email."
                        },
                        help_text="Obrigatório. 150 caracteres ou menos. São permitidos números, letras e @ /. / + / - / _ .",
                        max_length=150,
                        unique=True,
                        verbose_name="email",
                    ),
                ),
                ("name", models.CharField(max_length=150, verbose_name="Nome")),
                (
                    "date_joined",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="data de cadastro"
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Arquivo vazio. Você precisa submeter um arquivo.",
                        null=True,
                        upload_to="",
                        verbose_name="upload de foto",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Define se esse usuário pode logar no site admin",
                        verbose_name="Staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Define se o usuário está ativo ou não. Desmarque este campo ao invés de deletar a conta do usuário.",
                        verbose_name="Ativo",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.Permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "usuário",
                "verbose_name_plural": "usuários",
            },
            managers=[
                ("objects", apps.user.models.UserManager()),
            ],
        ),
    ]
