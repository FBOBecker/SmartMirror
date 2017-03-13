# -*- coding: utf-8 -*-
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def index():
    return render_template("home.html", shiet=(1, 2, 3, 4))
