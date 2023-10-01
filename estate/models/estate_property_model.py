from odoo import api, fields, models, tools
from odoo.exceptions import UserError, AccessError, ValidationError

class EstateProperties(models.Model):
    _name = "estate.property"
    _description = "Model for Real-Estate Properties"

    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Avaialable From', copy=False, default=lambda self: fields.Datetime.today())
    expected_price = fields.Float(string='Expected Price', required=True)
    selling_price = fields.Float(string='Selling Price', copy=False, readonly=True)
    bedrooms = fields.Integer(string='Bedrooms', default=2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area')
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north','North'), ('south','South' ), ('east','East'), ('west','West')],
        help="Type is used to separate Leads and Opportunities")
    state = fields.Selection(string='Status', default='new', required='true', copy='false',
        selection = [('new','New'), ('offer received','Offer Received'), ('offer accepted','Offer Accepted'), ('sold', 'Sold'), ('canceled','Canceled') ])
    property_type_id = fields.Many2one('estate.property.type', string='Property Type')
    buyer = fields.Many2one('res.partner', string='Buyer', copy=False, readonly=True)
    salesperson = fields.Many2one('res.users', string='Salesman', default=lambda self: self.env.user)
    tag_ids = fields.Many2many('estate.property.tag')
    offer_ids = fields.One2many('estate.property.offer', 'property_id')
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float(string='Best Offer', compute='_compute_highest_offer')

    @api.depends('offer_ids.price')
    def _compute_highest_offer(self):
        for property_record in self:
            offer_prices = property_record.offer_ids.mapped('price')
            if offer_prices:
                property_record.best_price = max(offer_prices)
            else:
                property_record.best_price = 0.0

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.onchange("garden")
    def _onchange_garden_area(self):
        if self.garden:
            self.garden_area = 10;
            self.garden_orientation = 'north'
        else:
            self.garden_area = False
            self.garden_orientation = False

    def action_sold(self):
        for property in self:
            if property.state == 'canceled':
                raise UserError('A canceled property cannot be set as sold.')
            property.state = 'sold'

    def action_cancel(self):
        for property in self:
            if property.state == 'sold':
                raise UserError('A sold property cannot be canceled.')
            property.state = 'canceled'

    _sql_constraints = [
        ('positive_expected_price', 'CHECK(expected_price > 0)', 'Expected price must be strictly positive!'),
        ('positive_selling_price', 'CHECK(selling_price >= 0)', 'Selling price must be positive!'),
        ('positive_offer_price', 'CHECK(offer_ids.price > 0)', 'Offer price must be strictly positive!'),
        ('unique_property_type_tag', 'UNIQUE(property_type_id, tag_ids)', 'Property type and tags must be unique!')
    ]

    @api.constrains('expected_price', 'selling_price')
    def _check_selling_price(self):
        for record in self:
            if not tools.float_is_zero(record.expected_price, precision_digits=2):
                if tools.float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=2) == -1:
                    raise ValidationError("Selling price cannot be lower than 90% of the expected price!")
