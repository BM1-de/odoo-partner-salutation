# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Letter Salutation",
    "summary": "Salutation on the contact and the matching greeting in the invoice "
    "and credit note mails",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "website": "https://github.com/BM1-de/odoo-partner-salutation",
    "author": "Baumgärtner Marketing GmbH",
    "maintainers": ["bm1-phillip"],
    "license": "AGPL-3",
    "development_status": "Alpha",
    "depends": ["account"],
    "data": ["views/res_partner_views.xml"],
    "images": ["static/description/banner.png"],
    "post_init_hook": "post_init_hook",
    "uninstall_hook": "uninstall_hook",
    "installable": True,
}
