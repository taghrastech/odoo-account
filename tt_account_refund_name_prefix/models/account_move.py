from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _compute_name_by_sequence(self):
        # account_move_name_sequence (OCA) generates `name` from the journal
        # ir.sequence in this compute. We then swap the leading prefix for credit
        # notes so invoices and refunds share ONE counter while showing distinct
        # prefixes (e.g. F0057/2026 -> FA0058/2026).
        super()._compute_name_by_sequence()
        for move in self:
            move._tt_apply_refund_prefix()

    def _tt_apply_refund_prefix(self):
        self.ensure_one()
        journal = self.journal_id
        refund_prefix = journal.tt_refund_prefix
        invoice_prefix = journal.tt_invoice_prefix
        if not refund_prefix or not invoice_prefix:
            return
        if self.move_type not in ("out_refund", "in_refund"):
            return
        # Renaming is incompatible with inalterable (hashed) journals: OCA derives
        # the secured sequence number by slicing the name with the sequence
        # prefix, so an extra prefix letter would break that parsing.
        if self.restrict_mode_hash_table:
            return
        name = self.name
        # Not assigned yet, or already transformed (idempotent).
        if not name or name == "/" or name.startswith(refund_prefix):
            return
        if name.startswith(invoice_prefix):
            self.name = refund_prefix + name[len(invoice_prefix):]
