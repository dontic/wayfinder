from wtforms.fields import DateTimeField
from flask_wtf import Form

class pathForm(Form):
    date = DateTimeField(id='datepick')

class visitsForm(Form):
    date_i = DateTimeField('Start Date', id='datepick1', format='%Y-%m-%d %H:%M:%S')
    date_f = DateTimeField(id='datepick2')