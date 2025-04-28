from odoo import api, fields, models
from odoo.exceptions import ValidationError
import time

class Session(models.Model):
    _name = "academic.session"
    
    name = fields.Char(string="Name", required=True)
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