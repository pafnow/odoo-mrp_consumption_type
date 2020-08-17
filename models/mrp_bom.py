# Copyright 2020 Pafnow

from odoo import api, fields, models
from odoo.exceptions import ValidationError

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    consumption_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('variable', 'Variable'),
        ('formula', 'Formula'),
    ], default='variable', string="Comsumption Type", required=True)

    consumption_formula = fields.Char(string="Formula", compute="_compute_consumption_formula", inverse="_compute_consumption_formula", store=True,
                                      help="""Formula to calculate the quantity of line component to be consumed.
                                      Available variables:
                                      - qty_WO = Quantity of finished product on Work Order
                                      - qty_BOM = Quantity of finished product on BOM header
                                      - factor[?] = Dictionary of factors for each variant attribute value""")

    @api.depends('consumption_type')
    def _compute_consumption_formula(self):
        # ATTENTION: This function is called in both compute and inverse of the consumption_formula (experiment)
        for record in self:
            if not record.consumption_type == 'formula':
                record.consumption_formula = None

    #//TODO: Make product_qty computed so it using formula


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def explode(self, product, quantity, picking_type=False):
        """ Surcharge to take into account consumption_type """
        boms_done, lines_done = super().explode(product, quantity, picking_type)

        for line in lines_done:
            if line[0]['consumption_type'] == 'fixed':
                line[1]['qty'] = line[0]['product_qty']
            if line[0]['consumption_type'] == 'formula':
                try:
                    line[1]['qty'] = eval(line[0]['consumption_formula'], {
                        'qty_WO': line[1]['original_qty'],  # Quantity of finished product on Work Order, to be launched in production
                        'qty_BOM': line[0]['product_qty'],  # Quantity of finished product on BOM header
                        'factor': {
                            r.attribute_id.name: r.mrp_bom_formula_factor
                            for r in line[1]['product'].product_template_attribute_value_ids.product_attribute_value_id
                        },
                    })
                except Exception as ex:
                    line[1]['qty'] = 999999.999  # Unrealistic quantity to warn user then raise message to user
                    raise ValidationError(
                        """Error during calculation of consumption formula for component %s
                        Formula = %s
                        Error = %s"""
                        % (str(line[0]['product_id']['default_code']), line[0]['consumption_formula'], str(ex))
                    )

        return boms_done, lines_done
