# Shared Invoice / Credit Note Sequence with Distinct Prefix

Lets customer invoices and their credit notes **share a single running number
sequence** while displaying a **different prefix** per document type — e.g.
invoices `F0057/2026`, credit notes `FA0058/2026`, all on **one common counter**.

Built as a thin extension of OCA
[`account_move_name_sequence`](https://github.com/OCA/account-financial-tools/tree/18.0/account_move_name_sequence).

## Why

Two requirements that are **mutually exclusive in standard Odoo 18**:

1. **One shared counter** across invoices and credit notes (… 0057, 0058, 0059 …).
2. **A different prefix** per type (`F…` for invoices, `FA…` for credit notes).

* **Native Odoo** derives the counter by parsing the document name
  (`sequence_prefix`). A different prefix splits the counter into two independent
  series — you cannot have both at once.
* **OCA `account_move_name_sequence`** moves numbering to a real `ir.sequence`
  (a standalone DB counter, decoupled from the name) — but it forbids using the
  *same* sequence for invoices and credit notes, and sharing one sequence yields
  the *same* prefix.

This module bridges the two: it keeps the **single shared `ir.sequence`** (so the
counter is common) and simply **rewrites the leading prefix on credit notes**
after the name is generated. Because the counter lives in the sequence, not in
the name, changing the displayed prefix has **zero impact on numbering**.

## What it does

* Adds two fields on the journal: **Invoice Name Prefix** and **Credit Note Name
  Prefix**.
* Extends OCA's `_compute_name_by_sequence`: once the shared sequence has produced
  the name (e.g. `F0058/2026`), for `out_refund` / `in_refund` moves it replaces
  the leading *Invoice Name Prefix* by the *Credit Note Name Prefix* →
  `FA0058/2026`.
* Invoices are never touched; the number, year and separators are kept verbatim,
  so the shared counter and the formatting are preserved.
* Idempotent: a credit note already prefixed is left untouched.

## How the two prefixes relate to the sequence

The module performs a pure find-and-replace on the **leading** characters of the
generated name:

```
final_name = Credit_Note_Name_Prefix + generated_name[len(Invoice_Name_Prefix):]
```

So **Invoice Name Prefix must equal the literal, non-dated start of the sequence
prefix** — otherwise the match fails and the credit note silently keeps the
invoice prefix.

| Sequence prefix | Invoice rendered | Invoice Name Prefix | Credit Note Name Prefix | Credit note result |
|---|---|---|---|---|
| `F` (+ suffix `/%(range_year)s`) | `F0058/2026` | `F` | `FA` | `FA0058/2026` |
| `F/%(range_year)s/` | `F/2026/0058` | `F` | `FA` | `FA/2026/0058` |

> Never put the year in *Invoice Name Prefix* (e.g. `F/2026/`): it would stop
> matching after the yearly reset. Use only the fixed part (`F`).

## Configuration

| # | Setting | Value |
|---|---|---|
| 1 | Sequence — Prefix | `F` |
| 2 | Sequence — Suffix | `/%(range_year)s` |
| 3 | Sequence — Size (padding) | `4` |
| 4 | Sequence — Use date range | ✅ (yearly reset) |
| 5 | Journal — Dedicated Credit Note Sequence | ☐ unchecked |
| 6 | Journal — Credit Note Entry Sequence | empty |
| 7 | Journal — Invoice Name Prefix | `F` |
| 8 | Journal — Credit Note Name Prefix | `FA` |

Result: `F0057/2026` → `FA0058/2026` → `F0059/2026` … on one shared counter.
The `F` series shows expected gaps wherever a credit note consumed a number
(e.g. 0058 became `FA0058`) — this is inherent to a shared counter.

## Limitation

Not compatible with journals using **inalterable hash / secure posting**
(`restrict_mode_hash_table`). OCA derives the secured sequence number by slicing
the name with the sequence prefix, so an extra prefix letter on credit notes
would break that parsing and the hash chain. A journal constraint blocks the
configuration in that case.

## Dependencies

* OCA `account_move_name_sequence` (which itself depends on `account`).

## Install

```bash
# 1. Clone into your Odoo addons path, using the module's TECHNICAL NAME as folder
git clone https://github.com/taghrastech/odoo-account-refund-name-prefix.git tt_account_refund_name_prefix

# 2. Install (v18 EE example)
cd "C:/Antigravity Projects/Odoo_Projects/odoo_18.0+e.20260227"
venv/Scripts/python.exe -m odoo -c odoo.conf -d odoo18 -i tt_account_refund_name_prefix --stop-after-init
```

> The GitHub repository is named `odoo-account-refund-name-prefix`, but the Odoo
> module technical name is `tt_account_refund_name_prefix`. Clone into a folder
> with that exact name (as shown above) so Odoo discovers the module correctly.

## Compatibility

* Odoo 18, Community & Enterprise (no edition-specific code).
* Requires OCA `account_move_name_sequence` 18.0.

## License

LGPL-3.

## Author

TaghrasTech — <https://github.com/taghrastech>
