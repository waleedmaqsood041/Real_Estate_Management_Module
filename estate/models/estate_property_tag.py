from odoo import fields, models

class EstateProperties(models.Model):
    _name = "estate.property.tag"
    _description = "Model for Real-Estate Properties"

    name = fields.Char(required=True)
