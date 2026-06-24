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
        string='Uses "Districts" terminology',
        default=True,
        help=(
            "Indicates whether this country's administrative subdivision "
            "below 'state_id' should be labelled as 'District'.\n"
            "If checked (default for most countries): the subdivision is "
            "rendered as 'District' / 'Distrito' in forms and views.\n"
            "If unchecked: the subdivision is rendered as 'City' / 'Ciudad'.\n"
            "Example: Panama's 83 subdivisions are formally called "
            "'distritos' but in this module they are loaded as res.city, "
            "so the flag is initialized to False and Odoo renders them as "
            "'City' / 'Ciudad'."
        ),
    )