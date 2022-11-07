from flask import render_template, flash, redirect, url_for
from app.auth.forms import RegistrationForm, LoginForm, ScrapyForm
from app.auth import authentication
from app.auth.models import User
from flask_login import login_user, logout_user, login_required, current_user
from bs4 import BeautifulSoup
import requests
from lxml import etree
import logging # es como el logger

@authentication.route("/register", methods=["GET", "POST"])
def register_user():
    if current_user.is_authenticated:
        flash("You are already logged in the system I")
        return redirect(url_for("authentication.homepage"))
    form=RegistrationForm()
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash("Registration Done...")
        return redirect(url_for("authentication.log_in_user"))
    return render_template("registration.html", form=form)

@authentication.route("/")
def index():
    return render_template("index.html")

@authentication.route("/login", methods=["GET", "POST"])
def log_in_user():
    if current_user.is_authenticated:
        flash("You are already logged in the system II")
        return redirect(url_for("authentication.homepage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_email=form.email.data).first()
        if not user or not user.check_password(form.password.data):
            flash("Invalid credentials...")
            return redirect(url_for("authentication.log_in_user"))

        login_user(user, form.stay_loggedin.data)
        return redirect(url_for("authentication.homepage"))
    return render_template("login.html", form=form)

@authentication.route("/homepage")
def homepage():
    return render_template("homepage.html")

@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user():
    logout_user()
    return redirect(url_for("authentication.log_in_user"))

@authentication.route("/scrapy_data", methods=["GET", "POST"])
@login_required
def scrapy_data():
    form = ScrapyForm() # Este es el formulario creado en forms.py
    if form.validate_on_submit(): # Valida que el formulario este lleno
        search = form.search_article.data
        url = f"https://listado.mercadolibre.com.co/{search}#D[A:{search}]"

        logging.error("url="+url)
        
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        dom = etree.HTML(str(soup))
        #data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']//div[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a/@href")
        data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']//div[@class='ui-search-item__group ui-search-item__group--title shops__items-group']//a/@href")
        #data_articles = dom.xpath("//ol[@class='ui-search-layout ui-search-layout--stack shops__layout']")
        #find('div', {'class': "ValidatorInfo_statusBadge__PBIGr"})

        #data_articles = [1,2,3,4]
        data = {"links": data_articles}

        return render_template("scrapy_data.html", **data) #data=data
    return render_template("scrapy_data.html", form=form)

@authentication.app_errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404
