{
    "name": "Mindesa: Account and Purchase-related customizations",
    "summary": """Implements custom permissions for site management.""",
    "description": """Mindesa
1. 2058234
2. 2123130
3. 2226708 - AAL
""",
    "author": "Odoo Inc",
    "website": "http://odoo.com",
    "category": "Custom Development",
    "version": "1.0",
    "depends": ["purchase_mrp"],
    'license': 'OPL-1',
    "data": [
        "data/record_rules.xml",
        "data/actions.xml",
        "views/product_views.xml",
        "views/partner_view_inherit.xml"
    ]
}