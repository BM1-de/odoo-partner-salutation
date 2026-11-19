## 20.0.1.0.0 (2026-11-19)

- Migration to Odoo 20.
- Odoo 20 has no switch between person and company any more and counts a
  contact without a tax ID as a person. Without a salutation, only a contact
  person below another contact is greeted by their name now; every contact
  without a parent contact gets the general greeting, also an association or
  a private customer without a tax ID („Guten Tag,“ instead of „Guten Tag
  Sportverein Musterstadt,“). A salutation greets such a contact personally.

## 19.0.1.0.0

- First version for Odoo 19, built on the salutation that Baumgärtner
  Marketing GmbH has used in its invoice mails since September 2026.
