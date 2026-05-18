{
    'name': 'Diving Instructor Scheduling',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Manage diving instructors and course bookings',
    'depends': ['base','web'],
    'data': [
    'security/ir.model.access.csv',
    'data/instructor_data.xml',
    'views/diving_booking_views.xml',    # ตัวนี้มี menu_diving_root
    'views/res_users_views.xml',
    'views/instructor_leave_views.xml',  # ตัวนี้มาเกาะ parent menu
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}