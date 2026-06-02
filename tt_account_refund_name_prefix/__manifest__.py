{
    'name': 'Shared Invoice/Credit Note Sequence with Distinct Prefix',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Share one number sequence between invoices and credit notes '
               'while keeping a distinct prefix on credit notes (e.g. F / FA).',
    'description': """
Shared Invoice/Credit Note Sequence with Distinct Prefix
========================================================

Extends OCA ``account_move_name_sequence`` so that customer invoices and their
credit notes can share a **single running number sequence** (one ``ir.sequence``)
while still showing a **different prefix** per document type.

Example (one shared counter, yearly reset):

* Invoice    -> ``F0057/2026``
* Credit note -> ``FA0058/2026``
* Invoice    -> ``F0059/2026``

How it works
------------
* The shared number is produced by the journal ``ir.sequence`` (OCA), so the
  counter is a standalone DB counter, fully decoupled from name parsing.
* The credit-note name is computed by ``_compute_name_by_sequence`` (OCA); this
  module extends it to replace the leading invoice prefix by the configured
  credit-note prefix for ``out_refund`` / ``in_refund`` moves.
* Because numbering does not depend on the displayed prefix, invoices and
  credit notes keep ONE common counter.

Configuration (per journal)
----------------------------
* Set the journal *Entry Sequence* to the shared ``ir.sequence``.
* Uncheck *Dedicated Credit Note Sequence* and clear *Credit Note Entry
  Sequence* (so refunds reuse the same sequence).
* Set *Invoice Name Prefix* (e.g. ``F``) — required, must match the sequence prefix.
* Set *Credit Note Name Prefix* (e.g. ``FA``).

Limitation
----------
Not compatible with journals using inalterable hash / secure posting
(``restrict_mode_hash_table``): renaming credit notes would break the secured
sequence number derived by ``account_move_name_sequence``. A constraint blocks
the configuration in that case.
    """,
    'author': 'TaghrasTech',
    'website': 'https://github.com/taghrastech',
    'license': 'LGPL-3',
    'depends': [
        'account_move_name_sequence',
    ],
    'data': [
        'views/account_journal_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
