"""sqlaclhemy models for tracker and class"""
import random
import pandas as pd
import numpy as np
import pdfkit
from flask import url_for, make_response, render_template, request
from thelper import APP, DB, admin_views
from thelper import models


@APP.route("/")
def hello():
    periods = DB.session.query(models.Period).all()
    return render_template("base.html", views=admin_views.admin_views, periods=periods)


@APP.route("/bingo")
def get_bingo_card():
    """generate bingo card"""
    bingo = DB.session.query(models.Bingo).all()
    selection = np.random.choice(bingo, 25, False)

    df = pd.DataFrame(np.reshape(selection, (5, 5)), columns=list("abcde"))
    df.loc[2, "c"] = "electric noises"
    return df.to_html(classes=["table table-condensed"])


@APP.route("/periods/<period_id>")
def get_period(period_id):
    periods = DB.session.query(models.Period).all()
    period = DB.session.query(models.Period).get(period_id)
    if period:
        return render_template(
            "class_schedule.html",
            period=period,
            views=admin_views.admin_views,
            periods=periods,
        )
    else:
        return "period not found"


@APP.route("/all_periods")
def get_all():
    """Generate pdf of all periods"""
    periods = DB.session.query(models.Period).all()
    urls = [
        f'http://{request.host}{url_for("get_period", period_id=period.id)}'
        for period in periods
    ]
    print(urls)
    print(request.url)
    options = {"javascript-delay": "3000"}
    pdf = pdfkit.from_url(urls, False, options=options)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"

    return response
