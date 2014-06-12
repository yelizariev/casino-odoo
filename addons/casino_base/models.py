# -*- coding: utf-8 -*-
from openerp.osv import osv,fields
from openerp import SUPERUSER_ID

class res_partner(osv.Model):
    _inherit = 'res.partner'

    def _get_deposit(self, cr, uid, ids, field_name, arg, context=None):
        prop = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category', context=context)
        deposit_account_id = prop and prop.id or False

        game_account_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'casino_base', 'game_account')[1]

        cr.execute("""SELECT l.partner_id, l.account_id, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      WHERE l.account_id IN %s
                      AND l.partner_id IN %s
                      GROUP BY l.partner_id, l.account_id
                      """,
                   ((deposit_account_id, game_account_id), tuple(ids),))
        res = {}
        for id in ids:
            res[id] = {'deposit':0, 'deposit_in_game':0}
        for id,acc,val in cr.fetchall():
            if acc==deposit_account_id:
                res[id]['deposit'] = -(val or 0)
            else:
                res[id]['deposit_in_game'] = +(val or 0)
        return res

    def move_deposit_to_game(self, cr, uid, ids, amount, game, context=None):
        deposit_line = {
            'debit':amount
        }
        game_line = {
            'debit':amount
        }
        return self._game_move(cr, uid, ids, deposit_line, game_line, game, context)

    def _game_move(self, cr, uid, ids, deposit_line, game_line, game, context=None):
        game_journal_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'casino_base', 'game_journal')[1]
        game_account_id = self.pool.get('ir.model.data').get_object_reference(cr, uid, 'casino_base', 'game_account')[1]
        prop = self.pool.get('ir.property').get(cr, uid, 'property_account_expense_categ', 'product.category', context=context)
        deposit_account_id = prop and prop.id or False


        move_obj = self.pool.get('account.move')
        for partner in self.browse(cr, uid, ids, context=context):
            line = [(0,0,deposit_line.update({
                'name':'-',
                'account_id':deposit_account_id,
            })),(0,0,game_line.update({
                'name':'-',
                'account_id':game_account_id,
            }))]

            move = {
                'ref':game,
                'journal_id':game_journal_id,
                'line_id':line
            }
            move_obj.create(cr, uid, move, context)

    _columns = {
        'deposit':fields.function(_get_deposit, type='float', string='Debosit money', multi='deposit'),
        'deposit_in_game':fields.function(_get_deposit, type='float', string='Money in game', multi='deposit'),
    }


#property_account_income_categ #доход
#property_account_receivable #расчеты с покупателями
#property_account_expense_categ #товары на складах
