Adds the field *Letter Salutation* to the contact, for example „Frau Muster“
or „Herr Dr. Meier“, and a greeting line computed from it in the language of
the mail:

- with a salutation: „Guten Tag Frau Muster,“, „Dear Frau Muster,“ or
  „Bonjour Frau Muster,“;
- without one, persons by their name: „Guten Tag Anna Beispiel,“;
- companies and addresses such as an invoice address in general terms:
  „Guten Tag,“, „Dear Sir or Madam,“ or „Bonjour,“.

Odoo 19 has no title field on contacts any more, and its invoice mail starts
with „Dear Anna Beispiel (Muster GmbH),“, or with the name of an
invoice address. On installation, the invoice and the credit note mail use the
new greeting line instead, in every language; uninstalling puts the original
greeting back.
