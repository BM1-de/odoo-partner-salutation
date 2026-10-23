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
        cls.company_partner = Partner.create(
            {"name": "Muster GmbH", "is_company": True}
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
            .get_param(
                "partner_letter_salutation.greeting.account.email_template_edi_invoice"
            )
        )
        # installing again changes the templates again, only once
        post_init_hook(self.env)
        post_init_hook(self.env)
        self.assertEqual(self.template.body_html.count("letter_greeting"), 1)

    def test_changed_template_is_left_alone(self):
        uninstall_hook(self.env)
        self.template.body_html = "<div><p>Hello,<br/>see attached.</p></div>"
        post_init_hook(self.env)
        self.assertNotIn("letter_greeting", self.template.body_html)
        # nothing stored for the invoice mail: uninstalling leaves it alone
        uninstall_hook(self.env)
        self.assertEqual(
            self.template.body_html, "<div><p>Hello,<br/>see attached.</p></div>"
        )

    def test_template_changed_after_installation(self):
        custom = "<div><p>Hello,<br/>a custom text.</p></div>"
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
