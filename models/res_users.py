from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    is_instructor = fields.Boolean(string="Is Instructor")
    instructor_lang_ids = fields.Many2many('res.lang', string="Instructor Languages")
    max_students_per_slot = fields.Integer(string="Max Students per Slot", default=3)