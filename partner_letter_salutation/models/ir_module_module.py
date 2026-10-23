# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models

from ..hooks import apply_greeting


class IrModuleModule(models.Model):
    _inherit = "ir.module.module"

    def _load_module_terms(self, modules, langs, overwrite=False):
        """Loading translations writes Odoo's greeting into the mails again."""
        result = super()._load_module_terms(modules, langs, overwrite=overwrite)
        apply_greeting(self.env)
        return result
