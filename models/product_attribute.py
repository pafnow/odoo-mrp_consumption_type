# Copyright 2020 Pafnow

from odoo import api, fields, models


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    mrp_bom_formula_factor = fields.Float(string="BOM Consumption Factor", default=1.0,
                                          help="Factor available in MRP BOM lines formula for quantity consumption calculation")
