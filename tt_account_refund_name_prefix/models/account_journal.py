from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    tt_invoice_prefix = fields.Char(
        string="Invoice Name Prefix",
        help="Leading part of the document number that will be replaced on "
             "credit notes. Must match the prefix produced by the journal "
             "sequence. Required when a Credit Note Name Prefix is set.\n"
             "Example: 'F' for invoices numbered 'F0057/2026'.",
    )
    tt_refund_prefix = fields.Char(
        string="Credit Note Name Prefix",
        help="When set, credit notes keep the shared sequence number but their "
             "leading prefix is replaced by this value.\n"
             "Example: 'FA' so the shared number 0058 is displayed as "
             "'FA0058/2026' while invoices stay 'F0057/2026'.",
    )

    @api.constrains("tt_invoice_prefix", "tt_refund_prefix", "restrict_mode_hash_table")
    def _check_tt_refund_prefix(self):
        for journal in self:
            if journal.tt_refund_prefix and not journal.tt_invoice_prefix:
                raise ValidationError(_(
                    "Journal '%s': set the Invoice Name Prefix when a Credit "
                    "Note Name Prefix is defined, otherwise credit notes cannot "
                    "reliably reuse the shared sequence number.",
                    journal.display_name,
                ))
            if journal.tt_refund_prefix and journal.restrict_mode_hash_table:
                raise ValidationError(_(
                    "Journal '%s': the Credit Note Name Prefix cannot be used on "
                    "a journal with inalterable hash (secure posting) enabled. "
                    "Renaming credit notes would break the secured sequence "
                    "number computed by account_move_name_sequence.",
                    journal.display_name,
                ))
