{
    'name': 'Pin Message in Chatter',
    'version': '18.0.1.0',
    'summary': 'Pin and manage important messages or log notes in the chatter',
    'description': """This module allows users to pin important messages""",
    'author': "Doodex",
    'category': 'Discuss',
    'website': "https://www.doodex.net/",
    'depends': ['web', 'base', 'mail'],
    'data': [
    ],
    'images': [
       'static/description/banner.gif',
       'static/description/icon.png',
    ],
    "assets": {
        "web.assets_backend":
            [
                'pin_message/static/src/css/style.css',
                'pin_message/static/src/xml/pinnedMessages.xml',
                'pin_message/static/src/xml/message_card_list.xml',
                'pin_message/static/src/js/pinMessage.js',
                'pin_message/static/src/js/chatter.js',
                'pin_message/static/src/js/message.js'
            ],
        'web.assets_tests': [
            'pin_message/static/tests/tours/**/*',
        ],
    },
    'license': 'LGPL-3',
    'price' : 19,
    'currency' : "USD",
    'installable': True,
    'auto_install': False,
    'application': False,
}
