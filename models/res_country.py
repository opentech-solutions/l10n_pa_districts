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
from odoo import api, fields, models


class ResCountry(models.Model):
    _inherit = 'res.country'

    cities_or_districts = fields.Boolean(
        string='Uses "Districts" terminology',
        default=False,
        help=(
            "Indicates whether this country's administrative subdivision "
            "below 'state_id' is called a 'District' instead of a 'City'.\n"
            "If checked: the city_id field is rendered with the label "
            "'District' and placeholder 'District...'.\n"
            "If unchecked (default, like most countries): the city_id field "
            "is rendered with the label 'City' and placeholder 'City...'.\n"
            "Use this for countries whose subdivisions below the "
            "province/state are formally called districts. Example: "
            "Panama (PA), where the 83 subdivisions are 'distritos'."
        ),
    )

    def _l10n_pa_districts_reset_non_pa(self):
        """Forza cities_or_districts=False para todos los países distintos
        a Panamá. Pensado para ser invocado desde data XML al instalar
        o actualizar el módulo.

        Panamá queda intacto (True, asignado por el <record> en el XML).
        """
        pa_id = self.env.ref('base.pa', raise_if_not_found=False)
        if not pa_id:
            return
        countries = self.search([('id', '!=', pa_id.id)])
        countries.write({'cities_or_districts': False})
        return countries

    def _l10n_pa_districts_enforce_cities(self):
        """Fuerza enforce_cities=True para Panamá y =False para el resto.

        Este método se invoca desde data XML al instalar o actualizar
        el módulo. Sirve como respaldo del <record id="base.pa"> cuando
        el país ya existía con enforce_cities=False (Odoo no actualiza
        records externos si solo tienen campos booleanos).
        """
        pa_id = self.env.ref('base.pa', raise_if_not_found=False)
        if not pa_id:
            return
        # Panamá: enforce_cities=True (forzar dropdown de distritos).
        pa_id.write({'enforce_cities': True})
        # Resto del mundo: enforce_cities=False (default, pero lo
        # aseguramos explícitamente).
        other_countries = self.search([('id', '!=', pa_id.id)])
        other_countries.write({'enforce_cities': False})
        return pa_id


class ResPartner(models.Model):
    _inherit = 'res.partner'

    city_id_placeholder = fields.Char(
        string='City Placeholder',
        compute='_compute_city_id_placeholder',
        store=True,
        help=(
            "Dynamic placeholder for the city_id field. Set to 'District...' "
            "when the country uses districts (cities_or_districts=True), "
            "otherwise 'City...'."
        ),
    )

    @api.depends('country_id', 'country_id.cities_or_districts')
    def _compute_city_id_placeholder(self):
        """Compute the placeholder for city_id based on the country.

        Es critical el @api.depends: si Odoo no sabe qué campos disparan
        el recálculo, el placeholder queda stale al cambiar el país.
        """
        city_label = self.env._('City...')
        district_label = self.env._('District...')
        for partner in self:
            if partner.country_id and partner.country_id.cities_or_districts:
                partner.city_id_placeholder = district_label
            else:
                partner.city_id_placeholder = city_label