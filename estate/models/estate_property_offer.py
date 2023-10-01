from odoo import fields, models


class EstateProperties(models.Model):
    _name = "estate.property.offer"
    _description = "Model for Real-Estate Properties"

    price = fields.Float('Price')
    status = fields.Selection(
        string='Status',
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity (Days)', default=7)
    date_deadline = fields.Date(string='Deadline', default=lambda self: fields.Date.today())


    def action_accept_offer(self):
        self.status = 'accepted'
        for offer in self:
            property = offer.property_id
            property.selling_price = offer.price
            property.buyer = offer.partner_id

    def action_refuse_offer(self):
        self.status = 'refused'
