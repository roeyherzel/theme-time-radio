from flask import jsonify, render_template, request, send_file

from archive import app
from archive.models.podcast import Episodes

import re
from jinja2 import evalcontextfilter, Markup, escape

_paragraph_re = re.compile(r'(?:\r){2,}')


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'%s' % p.replace('\n', '<br>\n') for p in _paragraph_re.split(escape(value)))

    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/episodes/<int:episode_id>')
def episodes_info(episode_id):
    ep = Episodes.query.get(episode_id)
    return render_template('episodes_info.html.jinja', episode=ep)


@app.route('/')
def index():
    return render_template('index.html.jinja')
