import os
from json import dump as json_dump, load as json_load

from flask import render_template, abort, Blueprint, flash, request
from flask_login import login_required
from flask_babel import lazy_gettext as _l

from ainur.adminmodules.slideshow.forms import SlideshowSettingsForm
from ainur.utils import validate_groups

exportmodule = Blueprint('admin_slideshowmodule', __name__,template_folder='templates')

@exportmodule.route('/', methods=['GET', 'POST'])
@validate_groups(['teachers','admins'])
@login_required
def slideshow():
    form = SlideshowSettingsForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            flash(_l('Config saved'))
            if form.background_image.data != None:
                f = form.background_image.data
                f.save(os.path.join(app.instance_path,'rsrc','slideshow_background'))
            with open('/etc/lliurex-news/slideshow.conf','w') as fd:
                config = form.data
                config.pop('background_image')
                config.pop('submit')
                config.pop('csrf_token')
                json_dump(config, fd, indent=4)
    else:
        if os.path.exists('/etc/lliurex-news/slideshow.conf'):
            try:
                with open('/etc/lliurex-news/slideshow.conf','r') as fd:
                    obj = json_load(fd)
                    form = SlideshowSettingsForm(**obj)
            except :
                pass
    return render_template('admin/slideshow/slideshow_admin.html', title='admin slideshow',form=form)