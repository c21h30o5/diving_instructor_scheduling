from odoo import models, fields

class InstructorLeave(models.Model):
    _name = 'instructor.leave'
    _description = 'Instructor Leave Record'
    _order = 'leave_date desc'

    instructor_id = fields.Many2one('res.users', string='Instructor', required=True)
    leave_date = fields.Date(string='Leave Date', required=True)
    leave_slot = fields.Selection([
        ('morning', 'Morning'),
        ('afternoon', 'Afternoon'),
        ('night', 'Night Dive'),
        ('full', 'Full Day')
    ], string='Leave Period', required=True, default='full')