# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Salutation of a contact and the greeting line of mails to it."""

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    letter_salutation = fields.Char(
        help="How the contact is addressed in mails, for example „Frau Muster“ or "
        "„Herr Dr. Meier“. Empty: persons are addressed by their name, companies and "
        "addresses such as an invoice address in general terms.",
    )
    letter_greeting = fields.Char(
        string="Greeting",
        compute="_compute_letter_greeting",
        help="Greeting line of mails to this contact, in the language of the mail, "
        "for example „Guten Tag Frau Muster,“ or „Dear Sir or Madam,“.",
    )

    @api.depends("letter_salutation", "name", "is_company", "type")
    @api.depends_context("lang")
    def _compute_letter_greeting(self):
        for partner in self:
            partner.letter_greeting = partner._get_letter_greeting()

    def _get_letter_greeting(self):
        self.ensure_one()
        name = (self.letter_salutation or "").strip()
        if not name and not self.is_company and self.type == "contact":
            name = (self.name or "").strip()
        if name:
            return self.env._("Dear %(name)s,", name=name)
        return self.env._("Dear Sir or Madam,")
