# coding=utf8
"""
Migrate pyecharts and Flask with custom template functions.
"""
from __future__ import unicode_literals

import random
import datetime

from flask import Flask, render_template
from flask.templating import Environment

from pyecharts import HeatMap, Map
from pyecharts.engine import ECHAERTS_TEMPLATE_FUNCTIONS
from pyecharts.conf import PyEchartsConfig


# ----- Adapter ---------
class FlaskEchartsEnvironment(Environment):
    def __init__(self, *args, **kwargs):
        super(FlaskEchartsEnvironment, self).__init__(*args, **kwargs)
        self.pyecharts_config = PyEchartsConfig(jshost='/static/js')
        self.globals.update(ECHAERTS_TEMPLATE_FUNCTIONS)


# ---User Code ----

class MyFlask(Flask):
    jinja_environment = FlaskEchartsEnvironment


app = MyFlask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/heatmap/")
def heatmap():
    hm = create_heatmap()
    return render_template('heatmap.html', hm=hm)


def create_heatmap():
    begin = datetime.date(2017, 1, 1)
    end = datetime.date(2017, 12, 31)
    data = [[str(begin + datetime.timedelta(days=i)),
             random.randint(1000, 25000)] for i in
            range((end - begin).days + 1)]
    heatmap = HeatMap("日历热力图示例", "某人 2017 年微信步数情况", width=1100)
    heatmap.add("", data, is_calendar_heatmap=True,
                visual_text_color='#000', visual_range_text=['', ''],
                visual_range=[1000, 25000], calendar_cell_size=['auto', 30],
                is_visualmap=True, calendar_date_range="2017",
                visual_orient="horizontal", visual_pos="center",
                visual_top="80%", is_piecewise=True)
    return heatmap


@app.route('/fujian/')
def fujian():
    value = [20, 190, 253, 77, 65]
    attr = ['福州市', '厦门市', '南平市', '泉州市', '三明市']
    map = Map("福建地图示例", width='100%', height=600)
    map.add("", attr, value, maptype='福建', is_visualmap=True,
            visual_text_color='#000')
    return render_template('fujian_map.html', m=map)


app.run(port=10200)
