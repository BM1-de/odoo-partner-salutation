Adds the field *Letter Salutation* to the contact, for example „Frau Muster“
or „Herr Dr. Meier“, and a greeting line computed from it in the language of
the mail:

- with a salutation: „Guten Tag Frau Muster,“, „Dear Frau Muster,“ or
  „Bonjour Frau Muster,“;
- without one, a contact person of a company or organisation (a contact of
  the type „Contact“ below another contact) by their name: „Guten Tag Anna
  Beispiel,“;
- every other contact without a salutation in general terms: „Guten Tag,“,
  „Dear Sir or Madam,“ or „Bonjour,“. These are companies, contacts without a
  parent contact such as an association or a private customer, and addresses
  such as an invoice address.

Odoo 20 has neither a switch between person and company nor first and last
names, and counts every contact without a tax ID as a person, also an
association or a public body. Whether a name is the name of a person, it cannot
tell; only a contact person below another contact is surely one.

Odoo has no title field on contacts any more, and its invoice mail starts
with „Dear Anna Beispiel (Muster GmbH),“, or with the name of an
invoice address. On installation, the invoice and the credit note mail use the
new greeting line instead, in every language; uninstalling puts the original
greeting back.
