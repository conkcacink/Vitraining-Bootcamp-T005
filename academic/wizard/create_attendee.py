from odoo import api, fields, models

class CreateAttendeeWizard(models.TransientModel):
    _name = 'academic.create.attendee.wizard'
    
    session_id = fields.Many2one(
        comodel_name='academic.session',
        string="Session",
        # required=True,
    )
    
    session_ids = fields.Many2many(comodel_name="academic.session", string="Sessions",)
    
    partner_ids = fields.Many2many(
        comodel_name='res.partner',
        string="Partners to add to session",
        required=True
    )
    
    def action_add_attendee(self):        
        self.ensure_one()

        for session in self.session_ids:
            for partner in self.partner_ids:
                
                existing = self.env['academic.attendee'].search([
                    ('session_id', '=', session.id),
                    ('partner_id', '=', partner.id),
                ])
                
                if not existing:
                    self.env['academic.attendee'].create({
                        'session_id': session.id,
                        'partner_id': partner.id,
                        # 'name': f"{partner.name} - {self.session_id.name}",
                        'name': str(partner.id),
                    })

        return {
            # 'type': 'ir.actions.act_window_close'
            'type': 'ir.actions.act_window',
            'name': 'Sessions',
            'res_model': 'academic.session',
            'view_mode': 'tree,form',
            'target': 'current',
        }
        # pass        
        # self.ensure_one()
        # self.session_id.attendee_ids = [(0, 0, {'partner_id': partner.id}) for partner in self.partner_ids]
        # return {'type': 'ir.actions.act_window_close'}