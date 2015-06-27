from flask import Flask, request, flash, url_for, redirect, render_template, abort, g, session
from functools import wraps

from flask.ext.login import login_required, current_user

from urllib import quote

from . import app
from .models import *
from .forms import *
from .auth import *

###Helpers###

def navLinks():
    pages = Page.query.all()
    links = []
    for page in pages:
        if page.title == 'index':
            continue
        links.append({'text':page.title, 'url':"/showPage/"+page.path})
    if current_user.is_authenticated():
        links.append({'text':"Page List", 'url':"/listPages"})
        links.append({'text':"Configure", 'url':"/configPage"})
        links.append({'text':"Logout", 'url':"/logout"})
    return links

def anchorLinks():
    pages = Page.query.all()
    noOfPages = range(len(pages))
    anchorLinks = "" #The index starts from 1 for pageSliding.js
    slideColors = ""
    sliderLinks = []
    slideTooltips = ""

    n=1
    first = True
    for page in pages:
        anchorLinks += "'page"+str(n)+"',"
        slideColors += "'"+page.color+"',"
        slideTooltips += "'"+page.title+"',"
        
        if first:
            sliderLinks.append("<li class='active' data-menuanchor='page"+str(n)+"'><a href=#page"+str(n)+">"+page.title+"</a></li>")
            first = False
        else:
            sliderLinks.append("<li data-menuanchor='page"+str(n)+"'><a href=#page"+str(n)+">"+page.title+"</a></li>")
        n += 1
        
    return [anchorLinks , sliderLinks, slideColors, slideTooltips ]


    
###render_template with default data embedded into page. Things like Nav bar
def _render_template(tmpl_name, **kwargs):
    siteTitle = Config.query.filter_by(config="server-name")[0].value
    return render_template(tmpl_name, links = navLinks(), title=siteTitle, **kwargs)

###Main module's views###
@app.route('/')
def index():
    #PageSlide.js
    pages = Page.query.all()
    sliderStuff = anchorLinks()
    return _render_template("pagepilling.html", pages = pages, anchorLinks = sliderStuff[0], sliderLinks = sliderStuff[1], slideColors = sliderStuff[2], slideTooltips = sliderStuff[3])
    #Standard Launcher
    #~ try:
        #~ page = Page.query.filter_by(title="index")[0]
        #~ return _render_template('index.html', page=page)
    #~ except:
        #~ return _render_template('index.html',pageTitle="Welcome!")

###Other routes###
###(Shift to individiaul blueprints if possible)###

###Page module###
@app.route('/listPages')
@login_required
def listPages():
    pages = Page.query.all()
    return _render_template("pageList.html",pages = pages, pageTitle="Page list")

@app.route('/login', methods=['GET', 'POST'])
def loginView():
    message = ""
    form = LoginForm()
    if form.validate_on_submit() and request.method == 'POST':
        user = User.get(form.username.data)
        if (user and user.password == form.password.data):
            login_user(user)
            return redirect(url_for('listPages'))
        else:
            return _render_template('login.html', form = form, message = "Wrong ID/Password")
    else:
        
        return _render_template('login.html', form = form, pageTitle="Login")
    
@app.route('/showPage/<pagePath>')
def showPage(pagePath):
    page = Page.query.filter_by(path=quote(pagePath))[0]
    if page:
        return _render_template('post.html',page=page)
    else:
        return redirect(url_for("listPages"))
    
@app.route('/submit', methods=['GET', 'POST'])
@login_required
def submitPage():
    form = pageFill()
    if form.validate_on_submit():
        page = Page()
        form.populate_obj(page)
        page.path = quote(page.title)
        db.session.add(page)
        db.session.commit()
        return redirect(url_for("listPages"))
    return _render_template('pageFill.html', form=form, pageTitle="Submit Page")

@app.route('/remove/<pagePath>')
@login_required
def removePage(pagePath):
    page = Page.query.filter_by(path=quote(pagePath))[0]
    db.session.delete(page)
    db.session.commit()
    return redirect(url_for("listPages"))

@app.route('/editPage/<pagePath>', methods=['GET', 'POST'])
@login_required
def editPage(pagePath):
    form = pageFill()
    page = Page.query.filter_by(path=quote(pagePath))[0]
    if form.validate_on_submit() and request.method == 'POST':
        form.populate_obj(page)
        db.session.commit()
        return redirect(url_for("showPage",pagePath=page.path))
    form.title.data = page.title
    form.text.data = page.text
    form.style.data = page.style
    form.color.data = page.color
    return _render_template('pageFill.html', form=form, pageTitle="Edit Page")
    
@app.route('/configPage', methods=['GET', 'POST'])
@login_required
def configPage():
    form = siteConfig()
    settings = Config.query.all()
    if form.validate_on_submit() and request.method == 'POST':
            settings = Config.query.all()
            settings[0].value = form.siteTitle.data
            db.session.commit()
            return redirect(url_for("index"))
    form.siteTitle.data = settings[0].value
    return _render_template('configPage.html', settings = settings, form = form, pageTitle="Webiste Config")

@app.errorhandler(Exception)
def defaultHandler(e):
    return _render_template("error.html")
