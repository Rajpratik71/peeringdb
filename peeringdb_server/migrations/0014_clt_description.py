# Generated by Django 1.11.4 on 2018-06-05 06:25


from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("peeringdb_server", "0013_user_locale"),
    ]

    operations = [
        migrations.AddField(
            model_name="commandlinetool",
            name="description",
            field=models.CharField(
                blank=True,
                help_text="Descriptive text of command that can be searched",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="commandlinetool",
            name="tool",
            field=models.CharField(
                choices=[
                    (b"pdb_renumber_lans", "Renumber IP Space"),
                    (b"pdb_fac_merge", "Merge Facilities"),
                    (b"pdb_fac_merge_undo", "Merge Facilities: UNDO"),
                ],
                help_text="name of the tool",
                max_length=255,
            ),
        ),
    ]
