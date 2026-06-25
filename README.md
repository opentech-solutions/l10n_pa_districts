# Panamá - Distritos

[![Maturity](https://img.shields.io/badge/maturity-Production-green)](https://odoo-community.org/page/development-status)
[![License](https://img.shields.io/badge/license-LGPL--3-blue)](http://www.gnu.org/licenses/lgpl-3.0-standalone.html)
[![Odoo](https://img.shields.io/badge/odoo-19.0-714b67)](https://www.odoo.com/documentation/19.0/)
[![Version](https://img.shields.io/badge/version-19.0.2.0.0-orange)](https://github.com/opentech-solutions/l10n_pa_districts)
[![Author](https://img.shields.io/badge/author-OPENTECH-714b67)](https://www.opentech.solutions)
[![Depends](https://img.shields.io/badge/depends-l10n__pa__provinces-blue)](https://github.com/opentech-solutions/l10n_pa_provinces)

> ⚠️ Este archivo fue generado con asistencia de herramienta de IA.

Módulo de localización para Panamá que:

1. Carga los **83 distritos oficiales** del país como registros del
   modelo estándar `res.city` de Odoo, asociándolos a su provincia
   o comarca correspondiente.
2. Añade el campo **`cities_or_districts`** en `res.country` para
   controlar de forma genérica si un país usa "District" / "Distrito"
   o "City" / "Ciudad" como terminología administrativa.
3. Inicializa el flag en **`True` solo para Panamá** (sus
   subdivisiones son distritos); el resto del mundo queda en
   `False` (default).
4. Implementa **placeholder dinámico** en el campo `city_id` del
   formulario de contactos según el país seleccionado: muestra
   "Distrito..." / "District..." para Panamá y "Ciudad..." /
   "City..." para el resto.

---

## Tabla de contenidos

- [Descripción](#descripción)
- [Funcionalidades principales](#funcionalidades-principales)
- [Campo `cities_or_districts`](#campo-cities_or_districts)
- [Placeholder dinámico](#placeholder-dinámico)
- [Distritos por provincia](#distritos-por-provincia)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso](#uso)
- [Modelos del módulo](#modelos-del-módulo)
- [Problemas conocidos](#problemas-conocidos)
- [Hoja de ruta](#hoja-de-ruta)
- [Créditos](#créditos)
- [Licencia](#licencia)
- [Referencias](#referencias)

---

## Descripción

La República de Panamá se organiza territorialmente en **10
provincias y 4 comarcas indígenas**, subdivididas a su vez en
**83 distritos**. El distrito es la unidad administrativa
equivalente al municipio en otros países y constituye el segundo
nivel de la jerarquía político-administrativa panameña.

Este módulo:

- **Extiende `l10n_pa_provinces`** cargando los 83 distritos como
  registros `res.city` (modelo estándar de Odoo para ciudades y
  unidades administrativas equivalentes), vinculados a su
  provincia/comarca.
- **Añade el campo genérico `cities_or_districts`** en
  `res.country` (no específico de Panamá) que cualquier país puede
  usar para indicar que su subdivisión se llama "Distrito" en
  lugar de "Ciudad".
- **Implementa el patrón de placeholder dinámico** de Odoo
  v19 para mostrar el término correcto según el país.

### ¿Por qué `res.city` y no un modelo propio?

Odoo provee `res.city` como modelo estándar. Panamá usa el
término **distrito**, pero el concepto es funcionalmente
idéntico al de ciudad. Reutilizar el modelo nativo:

- Garantiza compatibilidad con todos los módulos de Odoo que
  esperan ciudades en direcciones.
- Aprovecha el widget nativo de selección con autocompletado.
- Permite agrupación, filtrado y reportes geográficos sin código
  personalizado.
- Facilita la integración con mapas y servicios de geocoding.

---

## Funcionalidades principales

- **83 distritos oficiales** cargados vía CSV.
- **Asociación jerárquica** automática a provincia/comarca.
- **Campo genérico `res.country.cities_or_districts`** (default
  `False`).
- **Inicialización automática**: solo Panamá en `True`; el resto
  se fuerza a `False` en cada `-u` del módulo.
- **Placeholder dinámico** en `res.partner.city_id`:
  "Distrito..." / "District..." para Panamá, "Ciudad..." /
  "City..." para el resto.
- **Placeholder inicial bilingüe** "Ciudad o Distrito" / "City or
  District" mientras carga el record.
- **Vista extendida** en `res.partner`: dominio filtra por país
  + provincia.
- **Idempotente**: recargas repetidas no duplican registros.

---

## Campo `cities_or_districts`

### Definición

Campo `Boolean` agregado al modelo `res.country`:

```python
cities_or_districts = fields.Boolean(
    string='Uses "Districts" terminology',
    default=False,
    help="...",
)
```

### Lógica

| Valor | Significado | Label visible | Placeholder |
|---|---|---|---|
| `True` | El país usa distritos | "District" / "Distrito" | "District..." / "Distrito..." |
| `False` | El país usa ciudades | "City" / "Ciudad" | "City..." / "Ciudad..." |

### Aplicación por defecto

Solo **Panamá** (`base.pa`) tiene el flag en `True`. Esto se
configura en `data/res_country_data.xml` y se re-aplica en cada
`-u` del módulo (para resistir cambios manuales desde la UI).
Los demás países del mundo mantienen el default `False`.

### Configuración por país

Para activar el flag en otro país que use distritos:

1. Vaya a **Contactos > Configuración > Países**.
2. Seleccione el país (ej. Liberia, Corea del Norte).
3. En el formulario, marque la casilla **Uses "Districts"
   terminology**.
4. Guarde.

A partir de ese momento, el placeholder de city_id se renderiza
como "District..." / "Distrito..." en formularios de contacto.

---

## Placeholder dinámico

### Implementación técnica

Se usa el patrón nativo de Odoo v19 con `placeholder_field`:

```xml
<field name="city_id"
       placeholder="City or District"
       options="{'placeholder_field': 'city_id_placeholder'}"
       .../>
```

El campo `city_id_placeholder` está definido en `res.partner`
como **`compute` con `store=True`**:

```python
city_id_placeholder = fields.Char(
    compute='_compute_city_id_placeholder',
    store=True,
)

@api.depends('country_id', 'country_id.cities_or_districts')
def _compute_city_id_placeholder(self):
    for partner in self:
        if partner.country_id and partner.country_id.cities_or_districts:
            partner.city_id_placeholder = 'District...'
        else:
            partner.city_id_placeholder = 'City...'
```

### Comportamiento

| Estado | Placeholder (es_PA) | Placeholder (en_US) |
|---|---|---|
| Antes de cargar record | "Ciudad o Distrito" | "City or District" |
| País = Panamá | "Distrito..." | "District..." |
| País = USA, MX, etc. | "Ciudad..." | "City..." |
| Sin país | "Ciudad..." | "City..." |

### Por qué `store=True`

El mecanismo nativo `placeholder_field` lee el valor del campo
desde `record.data` en el cliente web. Sin `store=True`, el
campo computado no se persiste como columna en la BD y
`record.data` no lo encuentra, mostrando el placeholder
estático (que era "Distrito" hardcoded en español por un
oversight de `base_address_extended`).

---

## Distritos por provincia

### Resumen

| Provincia/Comarca | Código ISO | # Distritos |
| ----------------- | ---------- | ----------- |
| Chiriquí          | PA-4       | 14          |
| Veraguas          | PA-9       | 12          |
| Ngäbe-Buglé       | PA-NB      | 9           |
| Los Santos        | PA-7       | 7           |
| Herrera           | PA-6       | 7           |
| Panamá            | PA-8       | 6           |
| Coclé             | PA-2       | 6           |
| Colón             | PA-3       | 5           |
| Panamá Oeste      | PA-10      | 5           |
| Darién            | PA-5       | 4           |
| Bocas del Toro    | PA-1       | 4           |
| Emberá            | PA-EM      | 2           |
| Naso Tjër Di      | PA-NT      | 1           |
| Guna Yala         | PA-KY      | 1           |
| **Total**         |            | **83**      |

### Lista completa por provincia/comarca

#### Bocas del Toro (PA-1) — 4 distritos

Bocas del Toro, Changuinola, Chiriquí Grande, Almirante.

#### Coclé (PA-2) — 6 distritos

Penonomé, Aguadulce, Antón, Natá, La Pintada, Olá.

#### Colón (PA-3) — 5 distritos

Colón, Portobelo, Donoso, Santa Isabel, Chagres.

#### Chiriquí (PA-4) — 14 distritos

David, Boquete, Bugaba, Alanje, Barú, Boquerón, Dolega,
Gualaca, Remedios, Renacimiento, San Félix, San Lorenzo,
Tierras Altas, Tolé.

#### Darién (PA-5) — 4 distritos

La Palma, Chepigana, Pinogana, Santa Fe.

#### Herrera (PA-6) — 7 distritos

Chitré, Las Minas, Los Pozos, Ocú, Parita, Pesé, Santa María.

#### Los Santos (PA-7) — 7 distritos

Las Tablas, Guararé, Los Santos, Macaracas, Pedasí, Pocrí, Tonosí.

#### Panamá (PA-8) — 6 distritos

Panamá, San Miguelito, Arraiján, Capira, Chame, Taboga.

#### Veraguas (PA-9) — 12 distritos

Santiago, Atalaya, Calobre, Cañazas, La Mesa, Las Palmas,
Mariato, Montijo, Río de Jesús, San Francisco, Santa Fe, Soná.

#### Panamá Oeste (PA-10) — 5 distritos

La Chorrera, Arraiján, Capira, Chame, San Carlos.

#### Emberá (PA-EM) — 2 distritos

Cémaco, Sambú.

#### Guna Yala (PA-KY) — 1 distrito

Narganá (cabecera de la comarca).

#### Ngäbe-Buglé (PA-NB) — 9 distritos

Buabidí, Mironó, Nole Duima, Nurum, Jirondai, Santa Catalina,
Kankintú, Kusapín, Besiko.

#### Naso Tjër Di (PA-NT) — 1 distrito

Bonyic.

---

## Instalación

### Requisitos previos

- Odoo 19.0 o superior.
- Módulo **`l10n_pa_provinces`** instalado previamente.
- Módulo `base_address_extended` (incluido en Odoo estándar).

### Pasos

1. Asegúrese de que `l10n_pa_provinces` está instalado:
   > Aplicaciones > buscar "Panamá - Subdivisiones" > Instalar.
2. Copie la carpeta `l10n_pa_districts` a su directorio de
   addons.
3. Actualice la lista de aplicaciones.
4. Busque "Panamá - Distritos" e instale.
5. Verifique que los 83 distritos se hayan cargado:
   > Contactos > Configuración > Ciudades/Distritos.

### Línea de comandos

```bash
docker exec -it <odoo-container> odoo \
  -c /etc/odoo/odoo.conf \
  -d <database> \
  --init=l10n_pa_districts \
  --stop-after-init
```

### Actualización

```bash
docker exec -it <odoo-container> odoo \
  -c /etc/odoo/odoo.conf \
  -d <database> \
  -u l10n_pa_districts \
  --stop-after-init
```

---

## Configuración

Tras la instalación:

1. Los 83 distritos aparecen en los formularios de dirección
   cuando se selecciona Panamá como país.
2. El campo `city_id` muestra el placeholder dinámico.
3. Verifique el flag de Panamá en:
   > Contactos > Configuración > Países > Panamá >
   > "Uses 'Districts' terminology" debe estar marcado.

### Activar para otro país

Si su empresa opera en otro país que usa distritos:

1. Vaya a **Contactos > Configuración > Países**.
2. Seleccione el país deseado.
3. Active la casilla **Uses "Districts" terminology**.
4. Guarde.

---

## Uso

### En formularios de contacto

Al editar un contacto o empresa:

1. Seleccione **País** = Panamá.
2. Verá el placeholder "Distrito..." (o "Ciudad o Distrito"
   mientras carga).
3. Seleccione **Estado/Provincia**.
4. El selector de ciudad/distrito filtra automáticamente por la
   provincia seleccionada.

### Cambio dinámico al cambiar país

Si cambia el país de Panamá a USA en un contacto existente, el
placeholder del campo city_id se actualiza automáticamente de
"Distrito..." a "Ciudad..." sin recargar el formulario (gracias
al `@api.depends('country_id', 'country_id.cities_or_districts')`).

### Integración con otros módulos

- **`base_address_extended`**: provee la jerarquía País →
  Estado → Ciudad sobre la que se aplica el filtro.
- **`l10n_pa_provinces`**: provee las provincias que filtran los
  distritos.
- **`l10n_pa_extended`**: usa estos distritos como base para sus
  posiciones fiscales (Zona Libre de Colón, SEM, etc.).
- **Módulos de facturación electrónica DGI**: requieren códigos
  geográficos normalizados.

---

## Modelos del módulo

### Modelos extendidos (herencia)

#### `res.country` (de `base`)

```python
class ResCountry(models.Model):
    _inherit = 'res.country'

    cities_or_districts = fields.Boolean(
        string='Uses "Districts" terminology',
        default=False,
        help="...",
    )

    def _l10n_pa_districts_reset_non_pa(self):
        """Forza False en todos los países distintos a Panamá.
        Pensado para ser invocado desde data XML al instalar
        o actualizar el módulo.
        """
        ...
```

#### `res.partner` (de `base`)

```python
class ResPartner(models.Model):
    _inherit = 'res.partner'

    city_id_placeholder = fields.Char(
        string='City Placeholder',
        compute='_compute_city_id_placeholder',
        store=True,
        help="...",
    )

    @api.depends('country_id', 'country_id.cities_or_districts')
    def _compute_city_id_placeholder(self):
        ...
```

### Archivos de datos

| Archivo | Descripción |
|---|---|
| `data/res.city.csv` | 83 distritos con país + provincia. |
| `data/res_country_data.xml` | Init Panamá=True + reset otros=False. |

### Vistas

| Vista | Hereda de | Propósito |
|---|---|---|
| `views/res_country_views.xml` | `base.view_country_form` | Editar `cities_or_districts`. |
| `views/res_partner_views.xml` | `base_address_extended.address_street_extended_city_form` | Placeholder dinámico + dominio. |

---

## Problemas conocidos

- **Comarcas con un solo distrito**: Guna Yala (PA-KY) y Naso
  Tjër Di (PA-NT) tienen un solo distrito cargado porque
  administrativamente funcionan como una unidad.
- **Panamá Oeste (PA-10)**: creada en 2014, reorganizó distritos
  previamente bajo Panamá. Algunas bases legacy pueden tener
  asignaciones inconsistentes.
- **Nombres con diéresis**: `Ngäbe-Buglé`, `Naso Tjër Di`,
  `Kankintú`. Requieren PostgreSQL en UTF-8.
- **Distritos urbanos vs rurales**: el módulo carga cabeceras
  de distrito, no barrios ni corregimientos.
- **Reset forzado en cada `-u`**: si el admin activa el flag en
  otro país desde la UI, el `-u` del módulo lo desactivará (a
  menos que excluya ese país en el método Python).

---

## Hoja de ruta

- [ ] Cargar corregimientos (subdivisión menor urbana).
- [ ] Geometría geográfica (latitud/longitud).
- [ ] Soporte multilingüe (inglés y lenguas indígenas).
- [ ] UI para excluir países del reset automático sin tocar
      código Python.
- [ ] Carga de barrios como subregistro de distrito.

---

## Créditos

### Autor

- **OPENTECH SOLUTIONS** — <https://www.opentech.solutions>
- **ROSERO ONE** — Desarrollo principal

### Mantenedor

Este módulo es mantenido por **OPENTECH SOLUTIONS**.

Para reportar problemas, solicitar funcionalidades o contribuir,
visite <https://www.opentech.solutions>.

### Fuentes de datos

- **Instituto Nacional de Estadística y Censo (INEC) de Panamá**
  — División político-administrativa oficial.
- **Ley No. 39 de 1949** — Establece la división en distritos.
- **Decreto Ley No. 1 de 2009** — Crea la provincia de Panamá
  Oeste.
- **Leyes de comarcas**:
  - Ley No. 16 de 1953 (Guna Yala).
  - Ley No. 5 de 1993 (Emberá-Wounaan).
  - Ley No. 10 de 1997 (Ngäbe-Buglé).
  - Ley No. 7 de 2012 (Naso Tjër Di).

---

## Licencia

Este módulo está licenciado bajo **LGPL-3** (GNU Lesser General
Public License v3.0 o posterior).

Puede obtener una copia completa de la licencia en:
<http://www.gnu.org/licenses/lgpl-3.0-standalone.html>

```
Copyright (C) 2026 OPENTECH SOLUTIONS
Todos los derechos reservados.
```

---

## Referencias

- [INEC Panamá — División Político-Administrativa](https://www.inec.gob.pa)
- [Constitución Política de Panamá](https://www.asamblea.gob.pa)
  — Artículos 5, 6 y 7 (organización territorial).
- [Ley No. 39 de 1949](https://www.gacetaoficial.gob.pa) — Ley de distrito.
- [Odoo Documentation — Address Book](https://www.odoo.com/documentation/19.0/applications/essentials/contacts.html)
  — Modelo `res.city` y jerarquía de direcciones.
- [Odoo v19 — Dynamic Placeholders](https://www.odoo.com/documentation/19.0/developer/reference/user_interface/field_widgets.html)
  — `placeholder_field` en `options`.
- Módulo relacionado: [`l10n_pa_provinces`](https://github.com/opentech-solutions/l10n_pa_provinces)
- Módulo relacionado: [`l10n_pa_extended`](https://github.com/opentech-solutions/l10n_pa_extended)
- Módulo relacionado: [`base_address_extended`](https://github.com/odoo/odoo/tree/19.0/odoo/addons/base_address_extended)

---

<p align="center">
  <img src="./static/description/banner.jpg" width="640" alt="Panamá - Distritos">
</p>