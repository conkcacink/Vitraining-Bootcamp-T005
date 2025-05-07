from odoo import models

class View(models.Model):
    _inherit = 'ir.ui.view'

    def get_custom_views(self, model, view_type):
        if model == 'board.board':
            return []  # 🧨 Empty customization options
        return super().get_custom_views(model, view_type)