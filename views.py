from flask import render_template, redirect
from backend import app, cur_state
from forms import AnalyzeForm
# import json


@app.route('/')
def root():
    form = AnalyzeForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("root.html",
                           form=form,
                           title="Analyze",
                           datas=cur_state.datas_rep)


@app.route("/all")
def all():
    return render_template("all.html",
                           title="Words Rating",
                           datas=cur_state.all_rates_rep)
