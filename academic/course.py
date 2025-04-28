from odoo import api, fields, models

class Course(models.Model):
    _name = 'academic.course'
    
    name = fields.Char('Name')
    description = fields.Text(string="Description", required=True)
    responsible_id = fields.Many2one(comodel_name="res.users", string="Responsible")
    
    session_ids = fields.One2many(
        comodel_name="academic.session",
        inverse_name="course_id",
        string="Sessions",
        ondelete="cascade",
    )
    
    _sql_constraints = [
        ('check_name_unique','UNIQUE(name)','Field name harus unik!'),
        ('check_name_desc','CHECK(name <> description)', 'Name dan Description tidak boleh sama!')
    ]