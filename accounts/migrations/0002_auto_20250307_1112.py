from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='braintumorassessment',
            old_name='uploaded_at',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='braintumorassessment',
            name='confidence',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='braintumorassessment',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='braintumorassessment',
            name='scan_image',
            field=models.ImageField(default='default.jpg', upload_to='brain_scans/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='braintumorassessment',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='braintumorassessment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='usermedicalinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='usermedicalinfo',
            name='duration',
            field=models.IntegerField(help_text='Duration of symptoms in months'),
        ),
        migrations.AlterField(
            model_name='usermedicalinfo',
            name='gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')], max_length=10),
        ),
        migrations.AlterModelOptions(
            name='braintumorassessment',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='usermedicalinfo',
            options={'verbose_name_plural': 'User Medical Information'},
        ),
    ]
