from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import BooleanField, SubmitField, SelectField, RadioField
from flask_babel import lazy_gettext as _l
from ainur.forms import SliderField, ColorField


class SlideshowSettingsForm(FlaskForm):
    slide_timeout = SliderField(_l('Timeout slide'),default=10)
    transition = SelectField(_l('Transition'),choices=[('fade',_l('Fade')),('pushleft',_l('Push left')),('pushright',_l('Push right')),('pushup',_l('Push up')),('pushdown',_l('Push down'))])
    background_color = ColorField(_l('Background color image'), default="#fa8585")
    background_image = FileField(_l('Background image'))
    background_selected = RadioField(_l('Background'),choices=[('solid','Solid'),('image','Image')], default='solid')
    # title_size = SelectField('Title size',choices=[('8','8 px'),('9','9 px'),('10','10 px'),('11','11 px'),('12','12 px'),('13','13 px'),('14','14 px'),('15','15 px'),('16','16 px'),('18','18 px'),('20','20 px')])
    # description_size = SelectField('Description size',choices=[('8','8 px'),('9','9 px'),('10','10 px'),('11','11 px'),('12','12 px'),('13','13 px'),('14','14 px'),('15','15 px'),('16','16 px'),('18','18 px'),('20','20 px')])
    title_size = SliderField(_l('Title size'), default=75)
    description_size = SliderField(_l('Description size'), default=50 )
    submit = SubmitField(_l('Save'))