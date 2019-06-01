from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from domdit import app, mail, db, bcrypt, login_manager, recaptcha
from domdit.forms import Email, PortfolioForm, AdminForm, Login, TestimonialForm, ResumeForm
from domdit.models import Portfolio, User, Testimonial
from domdit.utils import portfolio_img_uploader
import shutil
import os
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.template_filter('autoversion')
def autoversion_filter(filename):
    path = 'domdit/' + filename[1:]

    try:
        timestamp = str(os.path.getmtime(path))
    except OSError:
        return filename

    newfile = "{0}?v={1}".format(filename, timestamp)
    print(newfile)
    return newfile


@app.route('/', methods=['GET', 'POST'])
def index():

    contact_form = Email()
    if request.method == 'POST':
        if request.form['contact_submit'] == 'send':
            if contact_form.validate_on_submit:
                if recaptcha.verify():
                    msg = Message("inquiry from domdit.com!", sender='customer@domdit.com', recipients=['me@domdit.com'])
                    msg.body = '''
                    From: %s <%s>
                    %s
                    ''' % (contact_form.name.data, contact_form.email.data, contact_form.message.data)
                    mail.send(msg)
                    flash('Message sent successfully!')
                else:
                    flash('Message unsuccessful, try again!')

    port_items = Portfolio.query.order_by(Portfolio.rank.asc()).limit(3).all()

    test_items = Testimonial.query.all()

    year = str(datetime.now().year)


    return render_template('index.html', title="Dominic DiTaranto - Web Design and Development",
                           contact_form=contact_form, port_items=port_items, year=year, test_items=test_items)


@app.route('/portfolio')
def view_port():

    port_items = Portfolio.query.order_by(Portfolio.rank.asc()).all()

    return render_template('view-port.html', title="Dominic DiTaranto - Portfolio", port_items=port_items)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('portfolio'))

    if form.validate_on_submit:
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('portfolio'))

    return render_template('login.html', form=form, title='Admin Login')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/admin/new_admin", methods=['GET', 'POST'])
@login_required
def new_admin():

    form = AdminForm()
    if request.method == 'POST':
        if form.validate_on_submit:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            email = form.email.data
            user = User(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('New administrative account created', 'success')
            return redirect(url_for('new_admin'))

    return render_template('new_user.html', title='Manage Admins - DOMDIT.COM',
                           form=form)


@app.route('/admin/portfolio', methods=['GET', 'POST'])
@login_required
def portfolio():

    form = PortfolioForm()

    if request.method == 'POST':

        print(form.errors)

        if form.validate_on_submit:
            portfolio_item = Portfolio(name=form.name.data,
                                       languages=form.languages.data,
                                       short_description=form.short_description.data,
                                       description=form.description.data,
                                       url=form.url.data,
                                       git=form.git.data,
                                       folder=form.folder.data
                                       )

            if form.thumb.data:
                portfolio_img_uploader(form.thumb.data, 'thumbnail', form.folder.data, 'port')

            if form.img1.data:
                portfolio_img_uploader(form.img1.data, 'img1', form.folder.data, 'port')

            if form.img2.data:
                portfolio_img_uploader(form.img2.data, 'img2', form.folder.data, 'port')

            if form.img3.data:
                portfolio_img_uploader(form.img3.data, 'img3', form.folder.data, 'port')

            db.session.add(portfolio_item)
            portfolio_item.rank = portfolio_item.id
            db.session.commit()

            flash('You successfully added a new portfolio item!', 'success')

    items = Portfolio.query.order_by(Portfolio.rank.asc()).all()

    return render_template('portfolio.html', form=form, items=items)


@app.route('/admin/resume', methods=['GET', 'POST'])
@login_required
def resume():
    form = ResumeForm()
    if request.method == 'POST':
        if form.validate_on_submit():

            file_path = os.path.join(current_app.root_path, '/static/Dominic DiTaranto - Resume')

            if os.path.isfile(file_path):
                os.remove(file_path)

            file = request.files['file']

            file_folder = os.path.join(current_app.root_path, 'static/')

            file.save(os.path.join(file_folder, 'Dominic_DiTaranto_-_Resume.pdf'))

            flash('Resume successfully uploaded!')

            return redirect(url_for('resume'))

    return render_template('resume.html', form=form)


@app.route('/admin/portfolio/edit/<int:item_id>', methods=['GET', 'POST'])
@login_required
def edit_portfolio(item_id):
    form = PortfolioForm()
    item = Portfolio.query.get_or_404(item_id)

    form.name.data = item.name
    form.languages.data = item.languages
    form.short_description.data = item.short_description
    form.description.data = item.description
    form.url.data = item.url
    form.git.data = item.git
    form.folder.data = item.folder

    if request.method == 'POST':
        if form.validate_on_submit:

            form = PortfolioForm()

            item.name = form.name.data
            item.languages = form.languages.data
            item.short_description = form.short_description.data
            item.description = form.description.data
            item.url = form.url.data
            item.git = form.git.data
            item.folder = form.folder.data

            if form.thumb.data:
                portfolio_img_uploader(form.thumb.data, 'thumbnail', form.folder.data, 'port')

            if form.img1.data:
                portfolio_img_uploader(form.img1.data, 'img1', form.folder.data, 'port')

            if form.img2.data:
                portfolio_img_uploader(form.img2.data, 'img2', form.folder.data, 'port')

            if form.img3.data:
                portfolio_img_uploader(form.img3.data, 'img3', form.folder.data, 'port')

            print(form.description.data)

            db.session.commit()

            flash('You successfully updated your portfolio item!', 'success')

            return redirect(url_for('portfolio'))

    items = Portfolio.query.order_by(Portfolio.rank.asc()).all()

    return render_template('portfolio.html', form=form, items=items)


@app.route('/admin/testimonial', methods=['GET', 'POST'])
@login_required
def testimonial():

    form = TestimonialForm()

    if request.method == 'POST':

        print(form.errors)

        if form.validate_on_submit:
            testimonial_item = Testimonial(name=form.name.data,
                                           site_name=form.site_name.data,
                                           portfolio_id=form.portfolio_id.data,
                                           text=form.text.data,
                                           url=form.url.data,
                                           folder=form.folder.data
                                           )

            if form.img.data:
                portfolio_img_uploader(form.img.data, 'img', form.folder.data, 'test')

            db.session.add(testimonial_item)
            db.session.commit()

    test_items = Testimonial.query.all()

    return render_template('testimonial.html', form=form, test_items=test_items)


@app.route("/rearrange/<int:item_id>/<direc>")
def rearrange(item_id, direc):

    if direc == 'right':

        item = Portfolio.query.get_or_404(item_id)
        other_item_rank = item.rank + 1
        other_item = Portfolio.query.filter_by(rank=other_item_rank).first()
        buffer = item.rank
        item.rank = other_item.rank
        other_item.rank = buffer

    elif direc == 'left':
        item = Portfolio.query.get_or_404(item_id)

        if not item.rank == 1:
            other_item_rank = item.rank - 1
            other_item = Portfolio.query.filter_by(rank=other_item_rank).first()
            buffer = item.rank
            item.rank = other_item.rank
            other_item.rank = buffer
        else:
            pass

    db.session.commit()
    return redirect(url_for('portfolio'))

@app.route("/item/<int:item_id>/<table>/<location>/delete", methods=['GET', 'POST'])
def delete_item(item_id, table, location):

    if table == 'PortfolioItem':
        item = Portfolio.query.get_or_404(item_id)
        path = os.path.join(current_app.root_path, 'static/img/portfolio', item.folder)
        shutil.rmtree(path)
        msg = "You Portfolio Item has been successfully deleted!"
    elif table == 'TestItem':
        item = Testimonial.query.get_or_404(item_id)
        msg = "You Testimonial Item has been successfully deleted!"


    else:
        flash('Delete failed, try again', 'danger')
        return redirect(url_for(location))

    db.session.delete(item)
    db.session.commit()
    flash(msg, 'success')
    return redirect(url_for(location))

@app.route("/jefimovas")
def jef():
    return render_template('jef.html')
