from flask import Flask,url_for, render_template, session, redirect, request, g, jsonify,flash
from config import Config
#from app import app
from forms import LoginForm


app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Magiel'}
    return render_template('base.html',user = user)


@app.route('/list')
def list():
    user = {'username': 'Magiel'}
    shoplist = ['12/5 eiers 2 doz , M', '12/5 brood 2, M', '12/5 Suiker 2kg, S']
    return  render_template('shoplist.html',user = user, slist = shoplist)

@app.route('/login_alternate',methods = ['POST','GET'])
def login_alternate():
    form = LoginForm()
    if form.validate_on_submit():
        flash('login request for user {}, remember me = {}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('/index')) #use funtion name in url_for
    return render_template('login_alt.html',title = 'Sign In', form = form)




if __name__ == "__main__":
    app.run(port=4800, debug=True)
