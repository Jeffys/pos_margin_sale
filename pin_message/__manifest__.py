{
    'name': 'Pin Message in Chatter',
    'version': '16.0.1.0',
    'summary': 'Pin and manage important messages or log notes in the chatter',
    'description': """This module allows users to pin important messages""",
    'author': "Doodex",
    'category': 'Discuss',
    'website': "https://www.doodex.net/",
    'depends': ['web', 'base', 'mail'],
    'data': [],
    'images': [
       'static/description/banner.gif',
       'static/description/icon.png',
    ],
    'assets': {
        'web.assets_backend': [
            'pin_message/static/src/xml/message_pin.xml',
            # Models
            'pin_message/static/src/models/message.js',
            'pin_message/static/src/models/pinned_box_view.js',
            'pin_message/static/src/models/pinned_messages_view.js',
            'pin_message/static/src/models/chatter.js',
            'pin_message/static/src/models/message_view_patch.js',
            'pin_message/static/src/models/message_action_list_patch.js',
            'pin_message/static/src/models/message_action_patch.js',
            'pin_message/static/src/models/message_action_view_patch.js',
            # Components
            'pin_message/static/src/components/pinned_box/pinned_box.js',
            'pin_message/static/src/components/pinned_box/pinned_box.scss',
            'pin_message/static/src/components/pinned_messages/pinned_messages.js',
            'pin_message/static/src/components/pinned_messages/pinned_messages.scss',
            
            # XML Templates
            'pin_message/static/src/components/pinned_box/pinned_box.xml',
            'pin_message/static/src/components/pinned_messages/pinned_messages.xml',
            'pin_message/static/src/components/chatter/chatter.xml',

            # Additional styles
            'pin_message/static/src/scss/pin_message.scss',
        ],
    },
    'license': 'LGPL-3',
    'price' : 19,
    'currency' : "USD",
    'installable': True,
    'auto_install': False,
    'application': False,
}
