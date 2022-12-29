from odoo.tests import common, Form


class TestPurchaseUser(common.TransactionCase):

    def test_purchase_user_access_rights(self):

        group_purchase_user = self.env.ref('purchase.group_purchase_user')

        self.user = self.env['res.users'].create({
            'name': 'Test Purchase User',
            'login': 'test',
            'email': 'test@purchaseuser',
            'groups_id': [(6, 0, [group_purchase_user.id])],
        })

        self.vendor = self.env['res.partner'].create({
            'name': 'Test Vendor',
            'email': 'test@vendor',
        })

        self.product = self.env['product.product'].create({
            'name': 'Product',
            'standard_price': 100.0,
            'list_price': 100.0,
            'type': 'service',
        })

        purchase_order_form = Form(self.env['purchase.order'].with_user(self.user))
        purchase_order_form.partner_id = self.vendor
        with purchase_order_form.order_line.new() as line:
            line.name = self.product.name
            line.product_id = self.product
            line.product_qty = 1
            line.price_unit = 1
            field_price_unit = line._fields['price_unit']
            field_taxes_id = line._fields['taxes_id']
            self.assertTrue(field_price_unit.readonly)
            self.assertTrue(field_taxes_id.readonly)