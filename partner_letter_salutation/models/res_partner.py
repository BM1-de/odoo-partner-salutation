# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Salutation of a contact and the greeting line of mails to it."""

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    letter_salutation = fields.Char(
        help="How the contact is addressed in mails, for example „Frau Muster“ or "
        "„Herr Dr. Meier“. Empty: a contact person of a company is addressed by their "
        "name, every other contact in general terms.",
    )
    letter_greeting = fields.Char(
        string="Greeting",
        compute="_compute_letter_greeting",
        help="Greeting line of mails to this contact, in the language of the mail, "
        "for example „Guten Tag Frau Muster,“ or „Dear Sir or Madam,“.",
    )

    @api.depends("letter_salutation", "name", "type", "parent_id")
    @api.depends_context("lang")
    def _compute_letter_greeting(self):
        for partner in self:
            partner.letter_greeting = partner._get_letter_greeting()

    def _is_letter_greeting_by_name(self):
        """Whether the contact is greeted by its name when it has no salutation.

        Odoo 20 has neither a switch between person and company nor first and
        last names, and computes a contact without a tax ID as a person, also an
        association or a public body. Surely a person is only a contact person of
        a company or organisation: a contact of the type "Contact" below another
        contact. Every other contact without a salutation is greeted in general
        terms: companies, contacts without a parent contact (also an association
        or a private customer) and addresses such as an invoice address.
        """
        self.ensure_one()
        return self.type == "contact" and bool(self.parent_id)

    def _get_letter_greeting(self):
        self.ensure_one()
        name = (self.letter_salutation or "").strip()
        if not name and self._is_letter_greeting_by_name():
            name = (self.name or "").strip()
        if name:
            return self.env._("Dear %(name)s,", name=name)
        return self.env._("Dear Sir or Madam,")
