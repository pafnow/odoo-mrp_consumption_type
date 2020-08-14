# Copyright 2020 Pafnow

from odoo import api, fields, models

class MrpBomLine(models.Model):
    _inherit = 'mrp.bom.line'

    consumption_type = fields.Selection([
        ('fixed', 'Fixed'),
        ('variable', 'Variable'),
        ('formula', 'Formula'),
    ], default='variable', string="Comsumption Type", required=True)


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def explode(self, product, quantity, picking_type=False):
        """ Surcharge to take into account consumption_type """
        boms_done, lines_done = super().explode(product, quantity, picking_type)

        for line in lines_done:
            if line[0]['consumption_type'] == 'fixed':
                line[1]['qty'] = line[0]['product_qty']

        return boms_done, lines_done
