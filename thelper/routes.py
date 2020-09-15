import random
import pandas as pd
import numpy as np
import pdfkit
from flask import url_for, make_response, render_template
from thelper import APP, DB, admin_views
from thelper import models


@APP.route("/")
def hello():
    return render_template("index.html", views=admin_views.admin_views)


@APP.route("/bingo")
def get_bingo_card():
    """generate bingo card"""
    bingo = DB.session.query(models.Bingo).all()
    selection = np.random.choice(bingo, 25, False)

    df = pd.DataFrame(np.reshape(selection, (5, 5)), columns=list("abcde"))
    df.loc[2, "c"] = "electric noises"
    return df.to_html()


@APP.route("/periods/<period_id>")
def get_period(period_id):
    period = DB.session.query(models.Period).get(period_id)
    return period.generate_groups().to_html()


@APP.route("/all_periods")
def get_all():
    """Generate pdf of all periods"""
    periods = DB.session.query(models.Period).all()
    urls = [
        f'http://localhost:5000{url_for("get_period", period_id=period.id)}'
        for period in periods
    ]
    print(urls)
    pdf = pdfkit.from_url(urls, False)
    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"

    return response
