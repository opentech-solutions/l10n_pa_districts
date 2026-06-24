# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenTech Solutions - Localización para Panamá.
#    Copyright (C) 2026 OPENTECH SOLUTIONS (<https://www.opentech.solutions>)
#
#    Puede modificarlo bajo los términos de la GNU LESSER GENERAL PUBLIC
#    LICENSE (LGPL v3), Versión 3.
#
#    Este programa se distribuye con la esperanza de que sea útil,
#    pero SIN NINGUNA GARANTÍA; ni siquiera la garantía implícita de
#    COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Consulte
#    la GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) para más detalles.
#
###############################################################################
from odoo import fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    cities_or_districts = fields.Boolean(
        string='Use "Districts" terminology',
        default=True,
        help=(
            "If checked (default), the standard Odoo terminology is used "
            "and the subdivision below 'state_id' is rendered as 'City'.\n"
            "If unchecked, the subdivision is rendered as 'District' "
            "(or its equivalent translation, e.g. 'Distrito' in Spanish). "
            "Use this for countries whose administrative divisions below "
            "the province/state are formally called districts "
            "(e.g. Panama, where the unit is the 'distrito')."
        ),
    )