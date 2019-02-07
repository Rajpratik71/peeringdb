import os
import json
import pytest
import peeringdb_server.models as models
import peeringdb_server.views as pdbviews
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, Client, RequestFactory

import peeringdb_server.inet as pdbinet
from util import SettingsCase

ERR_COULD_NOT_GET_RIR_ENTRY = "RDAP Lookup Error: Test Not Found"
ERR_BOGON_ASN = "RDAP Lookup Error: ASNs for documentation/private purposes " \
                     "are not allowed in this environment"

RdapLookup_get_asn = pdbinet.RdapLookup.get_asn


def setup_module(module):

    # RDAP LOOKUP OVERRIDE
    # Since we are working with fake ASNs throughout the api tests
    # we need to make sure the RdapLookup client can fake results
    # for us

    # These ASNs will be seen as valid and a prepared json object
    # will be returned for them (data/api/rdap_override.json)
    #
    # ALL ASNs outside of this range will raise a RdapNotFoundError
    ASN_RANGE_OVERRIDE = range(9000000, 9000999)

    with open(
            os.path.join(
                os.path.dirname(__file__), "data", "api",
                "rdap_override.json"), "r") as fh:
        pdbinet.RdapLookup.override_result = json.load(fh)

    def get_asn(self, asn):
        if asn in ASN_RANGE_OVERRIDE:
            r = pdbinet.RdapAsn(self.override_result)
            r._parse()
            r._parsed["name"] = "AS%d" % asn
            r._parsed["org_name"] = "ORG AS%d" % asn
            return r
        elif pdbinet.asn_is_bogon(asn):
            return RdapLookup_get_asn(self, asn)
        else:
            raise pdbinet.RdapNotFoundError("Test Not Found")

    pdbinet.RdapLookup.get_asn = get_asn


def teardown_module(module):
    pdbinet.RdapLookup.get_asn = RdapLookup_get_asn


class AsnAutomationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # create user and guest group
        guest_group = Group.objects.create(name="guest")
        user_group = Group.objects.create(name="user")

        with open(
                os.path.join(
                    os.path.dirname(__file__), "data", "api",
                    "rdap_override.json"), "r") as fh:
            data = json.load(fh)
            cls.rdap_63311 = pdbinet.RdapAsn(data)
            cls.rdap_63311_no_name = pdbinet.RdapAsn(data)
            cls.rdap_63311_no_name._parse()
            cls.rdap_63311_no_name._parsed["org_name"] = None
            cls.rdap_63311_no_name._parsed["name"] = None

        cls.ticket = {}

        for ticket_name in [
                "asnauto-9000001-org-net-created.txt",
                "asnauto-9000001-user-granted-ownership.txt",
                "asnauto-9000002-user-requested-ownership.txt"
        ]:
            with open(
                    os.path.join(
                        os.path.dirname(__file__), "data", "deskpro",
                        ticket_name), "r") as fh:
                cls.ticket[ticket_name] = fh.read()

        cls.base_org = models.Organization.objects.create(
            name="ASN Automation Tests")

        for username, email in [("user_a", "neteng@20c.com"),
                                ("user_b", "neteng@other.com"),
                                ("user_c", "other@20c.com")]:
            setattr(cls, username,
                    models.User.objects.create_user(username, email, username))
            getattr(cls, username).set_password(username)
            cls.base_org.usergroup.user_set.add(getattr(cls, username))
            user_group.user_set.add(getattr(cls, username))

    def setUp(self):
        self.factory = RequestFactory()

    def test_org_create_from_rdap(self):
        org, created = models.Organization.create_from_rdap(
            self.rdap_63311, 63311)
        self.assertEqual(org.name, "20C, LLC")
        org_2, created = models.Organization.create_from_rdap(
            self.rdap_63311, 63311)
        self.assertEqual(org_2.id, org.id)
        org, created = models.Organization.create_from_rdap(
            self.rdap_63311_no_name, 63311)
        self.assertEqual(org.name, "AS63311")

    def test_net_create_from_rdap(self):
        net, created = models.Network.create_from_rdap(self.rdap_63311, 63311,
                                                       self.base_org)
        self.assertEqual(net.name, "AS-20C")

        net, created = models.Network.create_from_rdap(self.rdap_63311, 63312,
                                                       self.base_org)
        self.assertEqual(net.name, "AS-20C !")

        net, created = models.Network.create_from_rdap(self.rdap_63311_no_name,
                                                       63313, self.base_org)
        self.assertEqual(net.name, "AS63313")

    def test_validate_rdap_relationship(self):
        b = self.user_a.validate_rdap_relationship(self.rdap_63311)
        self.assertEqual(b, True)
        b = self.user_b.validate_rdap_relationship(self.rdap_63311)
        self.assertEqual(b, False)
        b = self.user_c.validate_rdap_relationship(self.rdap_63311)
        self.assertEqual(b, False)

    def test_affiliate(self):
        """
        tests affiliation with non-existant asn
        """
        asn_ok = 9000001
        asn_ok_b = 9000002
        asn_fail = 890000

        # test 1: test affiliation to asn that has no RiR entry
        request = self.factory.post("/affiliate-to-org", data={
            "asn": asn_fail
        })
        request.user = self.user_a
        request._dont_enforce_csrf_checks = True
        resp = json.loads(pdbviews.view_affiliate_to_org(request).content)
        self.assertEqual(resp.get("asn"), ERR_COULD_NOT_GET_RIR_ENTRY)

        # test 2: test affiliation to asn that has RiR entry and user relationship
        # can be validated (ASN 9000001)
        request = self.factory.post("/affiliate-to-org", data={"asn": asn_ok})
        request.user = self.user_a
        request._dont_enforce_csrf_checks = True
        resp = json.loads(pdbviews.view_affiliate_to_org(request).content)
        self.assertEqual(resp.get("status"), "ok")

        # check that support tickets were created
        ticket = models.DeskProTicket.objects.get(
            subject=
            "[test][ASNAUTO] Organization 'ORG AS9000001', Network 'AS9000001' created"
        )
        self.assertEqual(ticket.body,
                         self.ticket["asnauto-9000001-org-net-created.txt"])

        ticket = models.DeskProTicket.objects.get(
            subject=
            "[test][ASNAUTO] Ownership claim granted to Org 'ORG AS9000001' for user 'user_a'"
        )
        self.assertEqual(
            ticket.body,
            self.ticket["asnauto-9000001-user-granted-ownership.txt"])

        net = models.Network.objects.get(asn=asn_ok)
        self.assertEqual(net.name, "AS%d" % asn_ok)
        self.assertEqual(net.org.name, "ORG AS%d" % asn_ok)
        self.assertEqual(
            self.user_a.groups.filter(
                name=net.org.admin_usergroup.name).exists(), True)
        self.assertEqual(net.status, "ok")
        self.assertEqual(net.org.status, "ok")

        # test 3: test affiliation to asn that hsa RiR entry and user relationship
        # cannot be verifiedi (ASN 9000002)
        request = self.factory.post("/affiliate-to-org", data={
            "asn": asn_ok_b
        })
        request.user = self.user_b
        request._dont_enforce_csrf_checks = True
        resp = json.loads(pdbviews.view_affiliate_to_org(request).content)
        self.assertEqual(resp.get("status"), "ok")

        # check that support tickets were created
        ticket = models.DeskProTicket.objects.get(
            subject=
            "[test]User user_b wishes to request ownership of ORG AS9000002")
        self.assertEqual(
            ticket.body,
            self.ticket["asnauto-9000002-user-requested-ownership.txt"])

        net = models.Network.objects.get(asn=asn_ok_b)
        self.assertEqual(net.name, "AS%d" % asn_ok_b)
        self.assertEqual(net.org.name, "ORG AS%d" % asn_ok_b)
        self.assertEqual(
            self.user_b.groups.filter(
                name=net.org.admin_usergroup.name).exists(), False)
        self.assertEqual(net.status, "ok")
        self.assertEqual(net.org.status, "ok")

    def test_affiliate_to_bogon_asn(self):
        """
        tests affiliation with non-existant asn
        """
        asns = []
        for a,b in pdbinet.BOGON_ASN_RANGES:
            asns.extend([a,b])

        for asn in asns:
            request = self.factory.post("/affiliate-to-org", data={
                "asn": asn})

            request.user = self.user_a
            request._dont_enforce_csrf_checks = True
            resp = json.loads(pdbviews.view_affiliate_to_org(request).content)
            self.assertEqual(resp.get("asn"), ERR_BOGON_ASN)


    def test_claim_ownership(self):
        """
        tests ownership to org via asn RiR validation
        """
        org = models.Organization.objects.create(
            status="ok", name="test_claim_ownership ORG")
        net = models.Network.objects.create(
            status="ok", name="test_claim_ownership NET", asn=9000100, org=org)

        request = self.factory.post("/request-ownership", data={"id": org.id})
        request.user = self.user_a
        request._dont_enforce_csrf_checks = True

        resp = json.loads(pdbviews.view_request_ownership(request).content)
        self.assertEqual(resp.get("status"), "ok")
        self.assertEqual(resp.get("ownership_status"), "approved")
        self.assertEqual(
            self.user_a.groups.filter(name=org.admin_usergroup.name).exists(),
            True)

    def test_claim_ownership_validation_failure(self):
        """
        test failure to claim ownership to org via asn RiR validation
        """
        org = models.Organization.objects.create(
            status="ok", name="test_claim_ownership ORG")
        net = models.Network.objects.create(
            status="ok", name="test_claim_ownership NET", asn=9000100, org=org)

        request = self.factory.post("/request-ownership", data={"id": org.id})
        request.user = self.user_b
        request._dont_enforce_csrf_checks = True

        resp = json.loads(pdbviews.view_request_ownership(request).content)
        self.assertEqual(resp.get("status"), "ok")
        self.assertEqual(resp.get("ownership_status"), "pending")
        self.assertEqual(
            self.user_b.groups.filter(name=org.admin_usergroup.name).exists(),
            False)

class TestTutorialMode(SettingsCase):
    settings = {"TUTORIAL_MODE":True}

    def setUp(self):
        super(TestTutorialMode, self).setUp()
        self.factory = RequestFactory()

    def test_affiliate_to_bogon_asn(self):
        """
        tests affiliation with non-existant bogon asn
        with tutorial mode enabled those should be allowed
        """
        user = get_user_model().objects.create_user("user_a", "user_a@localhost", "user_a")
        asns = []
        for a,b in pdbinet.BOGON_ASN_RANGES:
            asns.extend([a,b])

        for asn in asns:
            request = self.factory.post("/affiliate-to-org", data={
                "asn": asn})

            request.user = user
            request._dont_enforce_csrf_checks = True
            resp = json.loads(pdbviews.view_affiliate_to_org(request).content)
            self.assertEqual(resp.get("status"), "ok")


