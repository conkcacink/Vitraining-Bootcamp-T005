from odoo import api, fields, models
from odoo.exceptions import ValidationError
import time

class Session(models.Model):
    _name = "academic.session"
    
    name = fields.Char(string="ID", required=True)
    course_id = fields.Many2one(comodel_name="academic.course", string="Course", required=True)
    instructor_id = fields.Many2one(comodel_name="res.partner", string="Instructor", required=True)
    start_date = fields.Date(string="Start Date", default=lambda self:time.strftime("%Y-%m-%d"))
    duration = fields.Integer("Duration")
    seats = fields.Integer(string="Seats")
    active = fields.Boolean(string="Active", default=True)
    
    attendee_ids = fields.One2many(
        comodel_name="academic.attendee",
        inverse_name="session_id",
        string="Attendees"   
    )
    
    taken_seats = fields.Float(string="Taken Seats", compute="_calc_taken_seats")
    
    image_small = fields.Binary("Image Small")
    
    state = fields.Selection(
        string="State", selection=[('draft','Draft'),('open','Open'),('done','Done')], required=True, readonly=True, default='draft'
    )
    
    def action_draft(self):
        self.state = 'draft'
    
    def action_open(self):
        self.state = 'open'
        
    def action_done(self):
        self.state = 'done'
    
    @api.depends('seats', 'attendee_ids')
    def _calc_taken_seats(self):
        for rec in self:
            if rec.seats > 0:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.seats
            else:
                rec.taken_seats = 0.0
                
    @api.onchange('seats','attendee_ids')
    def onchange_seats(self):
        for rec in self:
            if rec.seats > 0:
                rec.taken_seats = 100.0 * len(rec.attendee_ids) / rec.seats
            else:
                rec.taken_seats = 0.0
                
    @api.constrains('instructor_id', 'attendee_ids')
    def _cek_instructor(self):
        for session in self:
            partner_ids = [att.partner_id.id for att in session.attendee_ids]
            if session.instructor_id.id in partner_ids:
                raise ValidationError('Instructor tidak boleh menjadi peserta!')
            
    def copy(self, default=None):
        self.ensure_one()
        d = dict(
            default or {},
            name = f"Copy of {self.name}"
        )
        return super(Session, self).copy(default=d)
    
    def open_wizard(self):
        view = self.env.ref('academic.create_attendee_form')
        wizard = self.env['academic.create.attendee.wizard'].create({
            # 'session_id':self.id
            'session_ids' : [(4,id) for id in self.ids]
        })
        
        return{
            'name' : 'Add Attendee',
            'type' : 'ir.actions.act_window',
            'view_type' : 'form',
            'view_mode' : 'form',
            'res_model' : 'academic.create.attendee.wizard',
            'views' : [(view.id , 'form')],
            'view_id' : view.id,
            'target' : 'new',
            'res_id' : wizard.id,
            'context' : self.env.context,
        }