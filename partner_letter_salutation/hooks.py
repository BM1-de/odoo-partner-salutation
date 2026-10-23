# Copyright 2026 Baumgärtner Marketing GmbH
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
"""Put the greeting line into the invoice and credit note mails, and back.

The standard templates start with „Dear <name> (<company>),“ followed by an
empty line. On installation, this greeting is replaced in every language by
the computed ``letter_greeting`` of the contact; the replaced text is kept and
put back on uninstallation, so that other changes made to the templates in the
meantime stay. A template whose first paragraph does not start with such a
greeting is left alone.

Loading the translations of a language writes the greeting of Odoo into that
language again, so the replacement runs again after every loading of
translations (``ir.module.module._load_module_terms``).
"""

import json
import re

TEMPLATES = (
    "account.email_template_edi_invoice",
    "account.email_template_edi_credit_note",
)
PARAMETER = "partner_letter_salutation.greeting.%s"
GREETING = re.compile(r"(<p\b[^>]*>)(.*?)(<br\s*/?>)", re.S)
LINE = (
    "\n        <t t-out=\"object.partner_id.letter_greeting or ''\">"
    "Dear Ms Muster,</t>\n        "
)
OUR_LINE = re.compile(
    r"\s*<t t-out=\"object\.partner_id\.letter_greeting or ''\">[^<]*</t>\s*", re.S
)


def _bodies(env, template):
    env.cr.execute("SELECT body_html FROM mail_template WHERE id = %s", [template.id])
    return env.cr.fetchone()[0] or {}


def _store(env, template, bodies):
    env.cr.execute(
        "UPDATE mail_template SET body_html = %s WHERE id = %s",
        [json.dumps(bodies), template.id],
    )
    env["mail.template"].invalidate_model(["body_html"])


def apply_greeting(env):
    """Replace Odoo's greeting by the greeting line, in every language."""
    Parameter = env["ir.config_parameter"].sudo()
    for xmlid in TEMPLATES:
        template = env.ref(xmlid, raise_if_not_found=False)
        if not template:
            continue
        bodies = _bodies(env, template)
        originals = json.loads(Parameter.get_param(PARAMETER % xmlid) or "{}")
        changed = False
        for lang, body in bodies.items():
            match = GREETING.search(body or "")
            if (
                not match
                or "letter_greeting" in body
                or "object.partner_id" not in match.group(2)
                or len(match.group(2)) > 2000
            ):
                continue
            originals[lang] = match.group(2)
            bodies[lang] = body[: match.start(2)] + LINE + body[match.end(2) :]
            changed = True
        if changed:
            Parameter.set_param(PARAMETER % xmlid, json.dumps(originals))
            _store(env, template, bodies)


def post_init_hook(env):
    apply_greeting(env)


def uninstall_hook(env):
    Parameter = env["ir.config_parameter"].sudo()
    for xmlid in TEMPLATES:
        stored = Parameter.get_param(PARAMETER % xmlid)
        Parameter.search([("key", "=", PARAMETER % xmlid)]).unlink()
        template = env.ref(xmlid, raise_if_not_found=False)
        if not stored or not template:
            continue
        originals = json.loads(stored)
        bodies = _bodies(env, template)
        for lang, body in bodies.items():
            if lang in originals and "letter_greeting" in (body or ""):
                bodies[lang] = OUR_LINE.sub(
                    lambda match, text=originals[lang]: text, body, count=1
                )
        _store(env, template, bodies)
