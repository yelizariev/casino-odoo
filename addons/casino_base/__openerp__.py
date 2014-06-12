{
    'name' : 'Backend for casino',
    'version' : '1.0.0',
    'author' : 'Ivan Yelizariev',
    'category' : 'Casino',
    'website' : 'https://it-projects.info',
    'description': '''

    Accounting stuff for casino:
    * property_account_expense_categ - accounting chips (internal money)
    * property_account_income_categ - accounting income (e.g. rake in poker)
    * casino_base.game_account - accounting chips in game (e.g. stack in poker)

    ''',
    'depends' : ['account'],
    'data':[
        'views.xml',
        'data.xml',
        ],
    'demo':[
        ],
    'installable': True
}
