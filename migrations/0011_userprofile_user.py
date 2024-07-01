from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


def create_unique_users(apps, schema_editor):
    UserProfile = apps.get_model("DiceApp", "UserProfile")
    User = apps.get_model(settings.AUTH_USER_MODEL)

    for profile in UserProfile.objects.all():
        unique_username = f"user_profile_{profile.id}"
        unique_email = f"{unique_username}@example.com"
        user = User.objects.create(username=unique_username, email=unique_email)
        profile.user = user
        profile.save()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("DiceApp", "0010_virtualwallet"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                null=True,
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.RunPython(
            create_unique_users, reverse_code=migrations.RunPython.noop
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="user",
            field=models.OneToOneField(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
