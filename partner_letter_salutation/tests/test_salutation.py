# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Greeting line of a contact and the invoice and credit note mails."""

from unittest.mock import patch

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon

from .. import hooks
from ..hooks import post_init_hook, uninstall_hook


@tagged("post_install", "-at_install")
class TestLetterSalutation(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Partner = cls.env["res.partner"]
        # Odoo 20 computes is_company: no parent contact and a tax ID
        cls.company_partner = Partner.create(
            {"name": "Muster GmbH", "vat": "DE123456789"}
        )
        cls.person = Partner.create(
            {"name": "Anna Beispiel", "parent_id": cls.company_partner.id}
        )
        cls.invoice_address = Partner.create(
            {
                "name": "Rechnungseingang",
                "parent_id": cls.company_partner.id,
                "type": "invoice",
            }
        )
        cls.template = cls.env.ref("account.email_template_edi_invoice")
        cls.credit_note_template = cls.env.ref("account.email_template_edi_credit_note")

    def greeting(self, partner, lang="en_US"):
        return partner.with_context(lang=lang).letter_greeting

    def test_greeting_rules(self):
        self.assertEqual(self.greeting(self.person), "Dear Anna Beispiel,")
        self.assertEqual(self.greeting(self.company_partner), "Dear Sir or Madam,")
        self.assertEqual(self.greeting(self.invoice_address), "Dear Sir or Madam,")
        self.person.letter_salutation = " Ms Beispiel "
        self.assertEqual(self.greeting(self.person), "Dear Ms Beispiel,")
        self.invoice_address.letter_salutation = "Frau Muster"
        self.assertEqual(self.greeting(self.invoice_address), "Dear Frau Muster,")

    def test_contact_without_parent_is_greeted_in_general_terms(self):
        """Without a salutation, only a contact person of a company gets its name.

        Odoo 20 computes a contact without a tax ID as a person, also an
        association, and has no first and last names: a contact without a parent
        contact is greeted in general terms, with or without a tax ID.
        """
        Partner = self.env["res.partner"]
        association = Partner.create({"name": "Sportverein Musterstadt"})
        private_customer = Partner.create({"name": "Erika Beispiel"})
        member = Partner.create(
            {"name": "Max Muster", "parent_id": association.id, "type": "contact"}
        )
        self.assertTrue(self.company_partner.is_company)
        self.assertFalse(association.is_company)
        for partner in (association, private_customer, self.company_partner):
            self.assertEqual(self.greeting(partner), "Dear Sir or Madam,")
        # contact persons are greeted by their name, also below an association
        self.assertEqual(self.greeting(member), "Dear Max Muster,")
        self.assertEqual(self.greeting(self.person), "Dear Anna Beispiel,")
        # a salutation is used for every contact
        association.letter_salutation = "Vorstand Sportverein Musterstadt"
        private_customer.letter_salutation = "Frau Beispiel"
        self.assertEqual(
            self.greeting(association), "Dear Vorstand Sportverein Musterstadt,"
        )
        self.assertEqual(self.greeting(private_customer), "Dear Frau Beispiel,")
        # the greeting follows when a contact gets or loses its parent contact
        association.letter_salutation = False
        private_customer.parent_id = association
        self.assertEqual(self.greeting(private_customer), "Dear Frau Beispiel,")
        private_customer.letter_salutation = " "
        self.assertEqual(self.greeting(private_customer), "Dear Erika Beispiel,")
        member.parent_id = False
        self.assertEqual(self.greeting(member), "Dear Sir or Madam,")

    def test_general_greeting_in_every_language(self):
        """The general greeting and the name in German, English and French."""
        for lang in ("de_DE", "fr_FR"):
            self.env["res.lang"]._activate_lang(lang)
        self.env["ir.module.module"]._load_module_terms(
            ["partner_letter_salutation"], ["de_DE", "fr_FR"], overwrite=True
        )
        association = self.env["res.partner"].create(
            {"name": "Sportverein Musterstadt"}
        )
        member = self.env["res.partner"].create(
            {"name": "Max Muster", "parent_id": association.id}
        )
        for lang, general, by_name in (
            ("de_DE", "Guten Tag,", "Guten Tag Max Muster,"),
            ("en_US", "Dear Sir or Madam,", "Dear Max Muster,"),
            ("fr_FR", "Bonjour,", "Bonjour Max Muster,"),
        ):
            self.assertEqual(self.greeting(association, lang), general)
            self.assertEqual(self.greeting(member, lang), by_name)

    def test_greeting_in_german(self):
        self.env["res.lang"]._activate_lang("de_DE")
        self.env["ir.module.module"]._load_module_terms(
            ["partner_letter_salutation"], ["de_DE"], overwrite=True
        )
        self.person.letter_salutation = "Frau Beispiel"
        self.assertEqual(
            self.greeting(self.person, "de_DE"), "Guten Tag Frau Beispiel,"
        )
        self.assertEqual(self.greeting(self.company_partner, "de_DE"), "Guten Tag,")

    def test_language_loaded_later(self):
        self.env["res.lang"]._activate_lang("fr_FR")
        self.env["ir.module.module"]._load_module_terms(
            ["account"], ["fr_FR"], overwrite=True
        )
        body = self.template.with_context(lang="fr_FR").body_html
        self.assertIn("object.partner_id.letter_greeting", body)
        self.assertEqual(body.count("letter_greeting"), 1)

    def test_translation_written_later(self):
        """A translation with Odoo's greeting gets the greeting line as well.

        Odoo 20 ships no translation of the text of the two mails yet, so the
        test writes one itself instead of relying on the files of Odoo.
        """
        self.env["res.lang"]._activate_lang("fr_FR")
        uninstall_hook(self.env)
        english = self.template.body_html
        self.assertIn("Dear", english)
        french_template = self.template.with_context(lang="fr_FR")
        french_template.body_html = english.replace("Dear", "Bonjour", 1)
        french = french_template.body_html
        self.assertIn("Bonjour", french)
        self.assertNotEqual(french, english)
        self.env["ir.module.module"]._load_module_terms(
            ["account"], ["fr_FR"], overwrite=True
        )
        for template in (self.template, french_template):
            self.assertEqual(template.body_html.count("letter_greeting"), 1)
        self.assertNotIn("Bonjour", french_template.body_html)
        # uninstalling puts the greeting of each language back
        uninstall_hook(self.env)
        self.assertEqual(french_template.body_html, french)
        self.assertEqual(self.template.body_html, english)

    def test_templates_use_the_greeting(self):
        for template in (self.template, self.credit_note_template):
            self.assertIn("object.partner_id.letter_greeting", template.body_html)
            self.assertNotIn("Dear\n", template.body_html)
        self.person.letter_salutation = "Ms Beispiel"
        invoice = self.init_invoice(
            "out_invoice", partner=self.person, amounts=[100], post=True
        )
        body = self.template._render_field("body_html", invoice.ids)[invoice.id]
        self.assertIn("Dear Ms Beispiel,", body)
        self.assertNotIn("Anna Beispiel (", body)

    def test_uninstall_restores_the_greeting(self):
        uninstall_hook(self.env)
        for template in (self.template, self.credit_note_template):
            self.assertNotIn("letter_greeting", template.body_html)
            self.assertIn("object.partner_id.name", template.body_html)
            self.assertIn("Dear", template.body_html)
        self.assertFalse(
            self.env["ir.config_parameter"]
            .sudo()
            .get_str(
                "partner_letter_salutation.greeting.account.email_template_edi_invoice"
            )
        )
        # installing again changes the templates again, only once
        post_init_hook(self.env)
        post_init_hook(self.env)
        self.assertEqual(self.template.body_html.count("letter_greeting"), 1)

    def test_changed_template_is_left_alone(self):
        uninstall_hook(self.env)
        self.template.body_html = "<div><p>Hello,<br>see attached.</p></div>"
        post_init_hook(self.env)
        self.assertNotIn("letter_greeting", self.template.body_html)
        # nothing stored for the invoice mail: uninstalling leaves it alone
        uninstall_hook(self.env)
        self.assertEqual(
            self.template.body_html, "<div><p>Hello,<br>see attached.</p></div>"
        )

    def test_template_changed_after_installation(self):
        custom = "<div><p>Hello,<br>a custom text.</p></div>"
        self.template.body_html = custom
        uninstall_hook(self.env)
        self.assertEqual(self.template.body_html, custom)
        self.assertNotIn("letter_greeting", self.credit_note_template.body_html)

    def test_missing_template(self):
        templates = hooks.TEMPLATES + ("account.no_such_template",)
        with patch.object(hooks, "TEMPLATES", templates):
            uninstall_hook(self.env)
            post_init_hook(self.env)
            self.assertIn("letter_greeting", self.template.body_html)
            uninstall_hook(self.env)
        self.assertNotIn("letter_greeting", self.template.body_html)
