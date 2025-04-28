from odoo import api, fields, models
from odoo.exceptions import ValidationError

class Attendee(models.Model):
    _name = "academic.attendee"
    
    name = fields.Char(string="ID") #string label diganti ID karena pada video #40 dan #41 ada event onchange partner to angka ID
    session_id = fields.Many2one(comodel_name="academic.session", string="Session")
    partner_id = fields.Many2one(comodel_name="res.partner", string="Partner")
    
    @api.onchange('partner_id')
    def onchange_partner(self):
        self.name = self.partner_id.id
    
    _sql_constraints = [
        ('partner_session_unik','UNIQUE(session_id,partner_id)','Multiple same attendees detected!')
    ]
    
    @api.constrains('session_id', 'partner_id')
    def _check_unique_partner_session(self):
        for rec in self:
            existing = self.env['academic.attendee'].search([
                ('session_id', '=', rec.session_id.id),
                ('partner_id', '=', rec.partner_id.id),
                ('id', '!=', rec.id),
            ], limit=1)
            if existing:
                raise ValidationError('Duplicate attendee for this session is not allowed!')