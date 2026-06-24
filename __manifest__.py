# -*- coding: utf-8 -*-
{
    'name': 'Panamá - Distritos',
    'version': '19.0.1.0.0',
    'category': 'Localization/Geographic Data',
    'summary': 'Carga los distritos de Panamá como ciudades (res.city) con etiqueta "Distrito".',
    'description': """
        Módulo de localización para Panamá que carga los 83 distritos
        oficiales del país como registros del modelo estándar
        `res.city`, asociados a su provincia o comarca
        (ISO 3166-2:PA) y al país Panamá (`base.pa`).

        Para Panamá, el concepto administrativo equivalente a
        "ciudad/municipio" es el "distrito", por lo que este módulo:

            * Carga los 83 distritos oficiales (cabeceras de distrito).
            * Hereda la etiqueta "Ciudad" del modelo `res.city` y la
              reemplaza por "Distrito" en español, mediante
              traducción `i18n/es.po`.
            * Depende de `l10n_pa_provinces` (provincias y comarcas),
              por lo que ambos módulos deben estar instalados.

        Después de instalar, los distritos aparecen en los formularios
        de Contactos y Empresa al asociar una dirección en Panamá.
    """,
    'author': 'OPENTECH SOLUTIONS by ROSERO ONE',
    'website': 'https://www.opentech.solutions',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'base_address_extended',
        'l10n_pa_provinces',
    ],
    'data': [
        'data/res.city.csv',
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/icon.png',
        'static/description/banner.jpg',
        'static/description/assets/tick.png',
        'static/description/assets/close.png',
        'static/description/assets/screenshots/list.png',
        'static/description/assets/screenshots/form.png',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}
