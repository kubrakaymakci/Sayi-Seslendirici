from flask import render_template, flash, redirect, url_for, request
from WebApp import app
from WebApp.forms import Form
import WebApp.audio as audio

i = 0

@app.route('/', methods=['GET', 'POST'])
def login():
    global i
    form = Form()
    if request.method == 'POST':
        sayi = form.sayi.data
        # flash('Bu bir flash mesajidir!', category='danger')
        i += 1
        i = i%3
        response = audio.calistir(sayi, i)
        if not response[0]:
            flash(response[1], 'danger')
            return render_template('home.html', form=form)
        else:

            return render_template('home.html', form=form, okunus=response[1], audio=f'audio{i}.wav')
    else:
        return render_template('home.html', form=form)