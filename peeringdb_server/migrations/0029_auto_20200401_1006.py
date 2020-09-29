# Generated by Django 2.2.9 on 2020-04-01 10:06

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_inet.models
import re


class Migration(migrations.Migration):

    dependencies = [
        ("peeringdb_server", "0028_ixlan_remove_auto_increment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="commandlinetool",
            name="created",
            field=models.DateTimeField(
                auto_now_add=True, help_text="command was run at this date and time"
            ),
        ),
        migrations.AlterField(
            model_name="commandlinetool",
            name="status",
            field=models.CharField(
                choices=[
                    ("done", "Done"),
                    ("waiting", "Waiting"),
                    ("running", "Running"),
                ],
                default="done",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="commandlinetool",
            name="tool",
            field=models.CharField(
                choices=[
                    ("pdb_renumber_lans", "Renumber IP Space"),
                    ("pdb_fac_merge", "Merge Facilities"),
                    ("pdb_fac_merge_undo", "Merge Facilities: UNDO"),
                    ("pdb_undelete", "Restore Object(s)"),
                    ("pdb_ixf_ixp_member_import", "IX-F Import"),
                ],
                help_text="name of the tool",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="commandlinetool",
            name="user",
            field=models.ForeignKey(
                help_text="the user that ran this command",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clt_history",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="geocode_date",
            field=models.DateTimeField(
                blank=True, help_text="Last time of attempted geocode", null=True
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="geocode_error",
            field=models.TextField(
                blank=True,
                help_text="Error message of previous geocode attempt",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="geocode_status",
            field=models.BooleanField(
                default=False,
                help_text="Has this object's latitude and longitude been synchronized to its address fields",
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Latitude",
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="facility",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Longitude",
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="internetexchange",
            name="media",
            field=models.CharField(
                choices=[
                    ("Ethernet", "Ethernet"),
                    ("ATM", "ATM"),
                    ("Multiple", "Multiple"),
                ],
                max_length=128,
            ),
        ),
        migrations.AlterField(
            model_name="internetexchange",
            name="region_continent",
            field=models.CharField(
                choices=[
                    ("North America", "North America"),
                    ("Asia Pacific", "Asia Pacific"),
                    ("Europe", "Europe"),
                    ("South America", "South America"),
                    ("Africa", "Africa"),
                    ("Australia", "Australia"),
                    ("Middle East", "Middle East"),
                ],
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="ixlanprefix",
            name="protocol",
            field=models.CharField(
                choices=[("IPv4", "IPv4"), ("IPv6", "IPv6")], max_length=64
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="allow_ixp_update",
            field=models.BooleanField(
                default=False,
                help_text="Specifies whether an ixp is allowed to add a netixlan entry for this network via their ixp_member data",
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="info_never_via_route_servers",
            field=models.BooleanField(
                default=False,
                help_text="Indicates if this network will announce its routes via rout servers or not",
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="info_ratio",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Not Disclosed"),
                    ("Not Disclosed", "Not Disclosed"),
                    ("Heavy Outbound", "Heavy Outbound"),
                    ("Mostly Outbound", "Mostly Outbound"),
                    ("Balanced", "Balanced"),
                    ("Mostly Inbound", "Mostly Inbound"),
                    ("Heavy Inbound", "Heavy Inbound"),
                ],
                default="Not Disclosed",
                max_length=45,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="info_scope",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Not Disclosed"),
                    ("Not Disclosed", "Not Disclosed"),
                    ("Regional", "Regional"),
                    ("North America", "North America"),
                    ("Asia Pacific", "Asia Pacific"),
                    ("Europe", "Europe"),
                    ("South America", "South America"),
                    ("Africa", "Africa"),
                    ("Australia", "Australia"),
                    ("Middle East", "Middle East"),
                    ("Global", "Global"),
                ],
                default="Not Disclosed",
                max_length=39,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="info_traffic",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Not Disclosed"),
                    ("0-20 Mbps", "0-20 Mbps"),
                    ("20-100Mbps", "20-100Mbps"),
                    ("100-1000Mbps", "100-1000Mbps"),
                    ("1-5Gbps", "1-5Gbps"),
                    ("5-10Gbps", "5-10Gbps"),
                    ("10-20Gbps", "10-20Gbps"),
                    ("20-50 Gbps", "20-50 Gbps"),
                    ("50-100 Gbps", "50-100 Gbps"),
                    ("100+ Gbps", "100+ Gbps"),
                    ("100-200 Gbps", "100-200 Gbps"),
                    ("200-300 Gbps", "200-300 Gbps"),
                    ("300-500 Gbps", "300-500 Gbps"),
                    ("500-1000 Gbps", "500-1000 Gbps"),
                    ("1 Tbps+", "1 Tbps+"),
                    ("10 Tbps+", "10 Tbps+"),
                ],
                max_length=39,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="info_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("", "Not Disclosed"),
                    ("Not Disclosed", "Not Disclosed"),
                    ("NSP", "NSP"),
                    ("Content", "Content"),
                    ("Cable/DSL/ISP", "Cable/DSL/ISP"),
                    ("Enterprise", "Enterprise"),
                    ("Educational/Research", "Educational/Research"),
                    ("Non-Profit", "Non-Profit"),
                    ("Route Server", "Route Server"),
                ],
                default="Not Disclosed",
                max_length=60,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="policy_contracts",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Not Required", "Not Required"),
                    ("Private Only", "Private Only"),
                    ("Required", "Required"),
                ],
                max_length=36,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="policy_general",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Open", "Open"),
                    ("Selective", "Selective"),
                    ("Restrictive", "Restrictive"),
                    ("No", "No"),
                ],
                max_length=72,
            ),
        ),
        migrations.AlterField(
            model_name="network",
            name="policy_locations",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Not Required", "Not Required"),
                    ("Preferred", "Preferred"),
                    ("Required - US", "Required - US"),
                    ("Required - EU", "Required - EU"),
                    ("Required - International", "Required - International"),
                ],
                max_length=72,
            ),
        ),
        migrations.AlterField(
            model_name="networkcontact",
            name="role",
            field=models.CharField(
                choices=[
                    ("Abuse", "Abuse"),
                    ("Maintenance", "Maintenance"),
                    ("Policy", "Policy"),
                    ("Technical", "Technical"),
                    ("NOC", "NOC"),
                    ("Public Relations", "Public Relations"),
                    ("Sales", "Sales"),
                ],
                max_length=27,
            ),
        ),
        migrations.AlterField(
            model_name="networkcontact",
            name="visible",
            field=models.CharField(
                choices=[
                    ("Private", "Private"),
                    ("Users", "Users"),
                    ("Public", "Public"),
                ],
                default="Public",
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="latitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Latitude",
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Allows you to upload and set a logo image file for this organization",
                null=True,
                upload_to="logos/",
            ),
        ),
        migrations.AlterField(
            model_name="organization",
            name="longitude",
            field=models.DecimalField(
                blank=True,
                decimal_places=6,
                help_text="Longitude",
                max_digits=9,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="partnership",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Allows you to upload and set a logo image file for this partnership",
                null=True,
                upload_to="logos/",
            ),
        ),
        migrations.AlterField(
            model_name="sponsorshiporganization",
            name="logo",
            field=models.FileField(
                blank=True,
                help_text="Allows you to upload and set a logo image file for this sponsorship",
                null=True,
                upload_to="logos/",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="status",
            field=models.CharField(default="ok", max_length=254, verbose_name="status"),
        ),
        migrations.AlterField(
            model_name="user",
            name="username",
            field=models.CharField(
                help_text="Required. Letters, digits and [@.+-/_=|] only.",
                max_length=254,
                unique=True,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[\\w\\.@+-=|/]+$",
                        "Enter a valid username.",
                        "invalid",
                        flags=re.RegexFlag(32),
                    )
                ],
                verbose_name="username",
            ),
        ),
        migrations.AlterField(
            model_name="userorgaffiliationrequest",
            name="asn",
            field=django_inet.models.ASNField(
                blank=True, help_text="The ASN entered by the user", null=True
            ),
        ),
        migrations.AlterField(
            model_name="userorgaffiliationrequest",
            name="org",
            field=models.ForeignKey(
                blank=True,
                help_text="This organization in our database that was derived from the provided ASN or organization name. If this is empty it means no matching organization was found.",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="affiliation_requests",
                to="peeringdb_server.Organization",
            ),
        ),
        migrations.AlterField(
            model_name="userorgaffiliationrequest",
            name="org_name",
            field=models.CharField(
                blank=True,
                help_text="The organization name entered by the user",
                max_length=255,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userorgaffiliationrequest",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("approved", "Approved"),
                    ("denied", "Denied"),
                ],
                help_text="Status of this request",
                max_length=254,
            ),
        ),
        migrations.AlterField(
            model_name="userorgaffiliationrequest",
            name="user",
            field=models.ForeignKey(
                help_text="The user that made the request",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="affiliation_requests",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="verificationqueueitem",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="The item that this queue is attached to was created by this user",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="vqitems",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
