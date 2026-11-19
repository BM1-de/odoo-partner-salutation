

# Briefanrede für Odoo
<!-- /!\ Non OCA Context : Set here the badge of your runbot / runboat instance. -->
[![Pre-commit Status](https://github.com/BM1-de/odoo-partner-salutation/actions/workflows/pre-commit.yml/badge.svg?branch=19.0)](https://github.com/BM1-de/odoo-partner-salutation/actions/workflows/pre-commit.yml?query=branch%3A19.0)
[![Build Status](https://github.com/BM1-de/odoo-partner-salutation/actions/workflows/test.yml/badge.svg?branch=19.0)](https://github.com/BM1-de/odoo-partner-salutation/actions/workflows/test.yml?query=branch%3A19.0)
[![codecov](https://codecov.io/gh/BM1-de/odoo-partner-salutation/branch/19.0/graph/badge.svg)](https://codecov.io/gh/BM1-de/odoo-partner-salutation)
<!-- /!\ Non OCA Context : Set here the badge of your translation instance. -->

<!-- /!\ do not modify above this line -->

Ein Feld *Briefanrede* am Kontakt („Frau Muster“, „Herr Dr. Meier“) und die passende
Grußzeile in der Sprache der Mail – in den Rechnungs- und Gutschriftmails sofort, in
anderen Vorlagen auf Wunsch.

> **Alpha:** So beginnen die Rechnungsmails der Baumgärtner Marketing GmbH seit September
> 2026, als Modul ist es neu. Die Software wird ohne Gewährleistung bereitgestellt
> (AGPL-3.0, Abschnitte 15 und 16).

![Kontakt mit Briefanrede](docs/screenshots/kontakt.png)

## Was das Modul tut

- Mit Briefanrede: „Guten Tag Frau Muster,“, englisch „Dear Frau Muster,“, französisch
  „Bonjour Frau Muster,“.
- Ohne Briefanrede: Personen mit ihrem Namen („Guten Tag Anna Beispiel,“), Firmen und Adressen
  wie eine Rechnungsadresse allgemein („Guten Tag,“ bzw. „Dear Sir or Madam,“).
- Die Rechnungs- und die Gutschriftmail beginnen nach der Installation in allen Sprachen
  mit dieser Grußzeile. Im Standard von Odoo 19 stünde dort „Guten Tag Anna Beispiel
  (Muster GmbH),“ oder der Name einer Rechnungsadresse.
- Bei der Deinstallation kommt die ursprüngliche Begrüßung zurück.

![Rechnungsmail mit Briefanrede](docs/screenshots/mail.png)

## Einrichtung

- Die Briefanrede am Kontakt neben der Position eintragen; Kontakte ohne Briefanrede
  brauchen nichts.
- Andere Mailvorlagen können die Grußzeile ebenfalls nutzen:
  `<t t-out="object.partner_id.letter_greeting"/>` statt der eigenen Begrüßung.

## Grenzen

- Nur Deutsch, Englisch und Französisch; andere Sprachen bekommen die englische
  Grußzeile.
- Eine schon geänderte Rechnungs- oder Gutschriftmail, deren erster Absatz nicht mit
  Odoos Begrüßung beginnt, bleibt unverändert.

## Mehr Dokumentation

Die Beschreibung des Moduls (englisch) steht in
[partner_letter_salutation/README.rst](partner_letter_salutation/README.rst).

*English: A letter salutation on the contact („Frau Muster“) and the matching greeting line
in the language of the mail, used by the invoice and credit note mails. Alpha, no
warranty.*

<!-- /!\ do not modify below this line -->

<!-- prettier-ignore-start -->

[//]: # (addons)

Available addons
----------------
addon | version | maintainers | summary
--- | --- | --- | ---
[partner_letter_salutation](partner_letter_salutation/) | 19.0.1.0.0 | <a href='https://github.com/bm1-phillip'><img src='https://github.com/bm1-phillip.png' width='32' height='32' style='border-radius:50%;' alt='bm1-phillip'/></a> | Salutation on the contact and the matching greeting in the invoice and credit note mails

[//]: # (end addons)

<!-- prettier-ignore-end -->

## Licenses

This repository is licensed under [AGPL-3.0](LICENSE).

However, each module can have a totally different license, as long as they adhere to Baumgärtner Marketing GmbH
policy. Consult each module's `__manifest__.py` file, which contains a `license` key
that explains its license.

----
<!-- /!\ Non OCA Context : Set here the full description of your organization. -->

<!-- bm1-verweise:start (scripts/readme-bm1.py, nicht von Hand ändern) -->

## Weitere Odoo-Projekte von BM1

| Projekt | Zweck |
| ------- | ----- |
| [Cc und Bcc](https://github.com/BM1-de/odoo-mail-cc-bcc) | Cc und Bcc beim Mailversand, eine einzige E-Mail an alle Empfänger |
| [Namenszusatz](https://github.com/BM1-de/odoo-partner-name-addition) | Zweite Namenszeile am Kontakt, gedruckt in jeder Anschrift |
| [Stundennachweis auf der Rechnung](https://github.com/BM1-de/odoo-timesheet-invoice) | Abgerechnete Zeiteinträge auf der Rechnung, je Aufgabe summiert |
| [Arbeitszeitgesetz](https://github.com/BM1-de/odoo-l10n-germany-arbzg) | Gesetzliche Pausen und Höchstarbeitszeit bei Anwesenheiten, Arbeitszeitkonto ab Odoo 20 |
| [Deutsche EÜR](https://github.com/BM1-de/odoo-l10n-germany-euer) | Einnahmenüberschussrechnung mit Anlage EÜR, AVEÜR und Anlagenverzeichnis |
| [Papierkram-Import](https://github.com/BM1-de/odoo-papierkram-import) | Kontakte, Rechnungen, Belege, Zahlungen und Zeiten aus Papierkram übernehmen |
| [Zeiterfassung für Odoo (macOS)](https://github.com/BM1-de/timesheets-for-odoo) | Menüleisten-App für Zeiten und Anwesenheit |
| [Zeiterfassung für Odoo (Windows)](https://github.com/BM1-de/timesheets-for-odoo-windows) | App im Infobereich für Zeiten und Anwesenheit |

## Über BM1

<a href="https://bm1.de"><picture><source media="(prefers-color-scheme: dark)" srcset="docs/bm1/logo-bm1-negativ.svg"><img src="docs/bm1/logo-bm1.svg" alt="BM1" width="180"></picture></a>

Entwickelt und gepflegt von [BM1](https://bm1.de), der Baumgärtner Marketing GmbH aus
Bayreuth: Agentur für [Websites](https://bm1.de/websites/),
[Webentwicklung](https://bm1.de/webentwicklung/), [SEO](https://bm1.de/seo/) und
[individuelle digitale Lösungen](https://bm1.de/digitale-spezial-themen/). Wir arbeiten selbst
jeden Tag mit Odoo und bauen, was uns dort fehlt. Wenn Sie Unterstützung bei Odoo, einer
Website oder einer Anbindung brauchen, die es nicht von der Stange gibt:
[sprechen Sie uns an](https://bm1.de/kontakt/).

<!-- bm1-verweise:end -->
