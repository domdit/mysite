from flask import render_template, request, flash, redirect, url_for, current_app
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from domdit import app, mail, db, bcrypt, login_manager, recaptcha
from domdit.forms import Email, PortfolioForm, AdminForm, Login, TestimonialForm, NewBlogPost, CommentForm, Search
from domdit.models import Portfolio, User, Testimonial, Blog, Tag, Comment
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

    port_items = Portfolio.query.all()

    test_items = Testimonial.query.all()

    year = str(datetime.now().year)


    return render_template('index.html', title="Dominic DiTaranto - Web Design and Development",
                           contact_form=contact_form, port_items=port_items, year=year, test_items=test_items)


@app.route('/sand')
def sand():
    return render_template('sand.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    if current_user.is_authenticated:
        return redirect(url_for('portfolio'))

    elif form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('portfolio'))
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form, title='Admin Login')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/admin/new_admin", methods=['GET', 'POST'])
@login_required
def new_admin():

    form = AdminForm()
    if form.validate_on_submit():
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

        if form.validate_on_submit():
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
            db.session.commit()

            flash('You successfully added a new portfolio item!', 'success')

    items = Portfolio.query.all()

    return render_template('portfolio.html', form=form, items=items)


@app.route('/admin/testimonial', methods=['GET', 'POST'])
@login_required
def testimonial():

    form = TestimonialForm()

    if request.method == 'POST':

        print(form.errors)

        if form.validate_on_submit():
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

@app.route("/admin/new_blog_post", methods=['GET', 'POST'])
@login_required
def new_blog_post():

    form = NewBlogPost()

    if request.method == 'POST':

        x = datetime.now()
        date = x.strftime("%x %I:%M")

        print(form.errors)

        if form.validate_on_submit():
            blog_post = Blog(name=form.post_name.data,
                             date=date,
                             text=form.content.data,
                             tags=form.tags.data,
                             category=form.category.data
                             )

            db.session.add(blog_post)
            db.session.commit()

            return redirect(url_for('post', post_id=blog_post.blog_id))

    return render_template('new_blog_post.html', form=form, legend="New Blog Post")

@app.route("/admin/post/<int:post_id>/update", methods=['GET', 'POST'])
def update(post_id):

    if not current_user.is_authenticated:
        redirect(url_for('login'))

    form = NewBlogPost()
    post = Blog.query.get_or_404(post_id)

    if form.validate_on_submit():
        post.name = form.post_name.data
        post.text = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post_id))

    form.post_name.data = post.name
    form.content.data = post.text

    return render_template('new_blog_post.html', form=form, legend="Update Blog Post")



@app.route("/blog", methods=['GET', 'POST'])
def blog():

    page = request.args.get('page', 1, type=int)
    posts = Blog.query.order_by(Blog.date.desc()).paginate(page=page, per_page=5)

    # for the sidebar
    recent_posts = Blog.query.order_by(Blog.date.desc()).limit(3).all()
    categories = Blog.query.group_by(Blog.category).limit(5).all()
    tags = Tag.query.group_by(Tag.name).limit(25).all()
    search_form = Search()
    if search_form.validate_on_submit():
        return redirect(url_for('query', term=search_form.term.data))



    return render_template('blog.html', posts=posts, title="Blog - Dominic DiTaranto", search_form=search_form,
                           recent_posts=recent_posts, categories=categories, tags=tags)

@app.route("/blog/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Blog.query.get_or_404(post_id)

    prev = post_id - 1
    next = post_id + 1

    prev_post = False
    next_post = False

    if Blog.query.get(prev):
        prev_post = Blog.query.get_or_404(prev)

    if Blog.query.get(next):
        next_post = Blog.query.get_or_404(next)

    form = CommentForm()

    x = datetime.now()
    date = x.strftime("%x %I:%M")

    if request.method == 'POST':
        if form.comment_submit.data:
            if recaptcha.verify():
                if form.validate_on_submit():


                    comment = Comment(name=form.name.data,
                                      date=date,
                                      email=form.email.data,
                                      text=form.text.data,
                                      post_id=post_id
                                      )
                    db.session.add(comment)
                    db.session.commit()

                    msg = Message("New comment from domdit.com!", sender='customer@domdit.com', recipients=['me@domdit.com'])
                    msg.body = '''
                                        From: %s <%s>
                                        %s
                                        %s
                                        ''' % (form.name.data, form.email.data, form.text.data, url_for('post', post_id=post_id, _external=True))

                    mail.send(msg)

                    flash("Thank you for the comment! Check back for a reply!")

                    return redirect(url_for('post', post_id=post_id))

    comments = Comment.query.filter(Comment.post_id == post_id).order_by(Comment.date.desc()).all()

    count = 0
    for i in comments:
        count += 1

    # for the sidebar
    recent_posts = Blog.query.order_by(Blog.date.desc()).limit(3).all()
    categories = Blog.query.group_by(Blog.category).limit(5).all()
    tags = Tag.query.group_by(Tag.name).limit(25).all()

    search_form = Search()
    if search_form.search_submit.data and search_form.validate():
        return redirect(url_for('query', term=search_form.term.data))

    return render_template('post.html', post=post, prev_post=prev_post, next_post=next_post,
                           title=post.name, search_form=search_form, form=form, comments=comments, count=count,
                           recent_posts=recent_posts, categories=categories, tags=tags)


@app.route('/blog/query/<term>', methods=['GET', 'POST'])
def query(term):

    tag_query = Tag.query.filter_by(name=term).all()
    text_query = Blog.query.filter((Blog.text.contains(term)) | (Blog.name.contains(term)) | Blog.category.contains(term)).all()

    id_list = []
    tag_posts = []


    if tag_query:
        got_tags = tag_query[0].post_tags.all()
        for tags in got_tags:
            if tags.blog_id in id_list:
                pass
            else:
                id_list.append(tags.blog_id)

    if text_query:
        for post in text_query:
            if post.blog_id in id_list:
                pass
            else:
                id_list.append(post.blog_id)

    id_list.sort(reverse=True)


    for id in id_list:
        tag_posts.append(Blog.query.filter_by(blog_id=id).all())

    # for the sidebar
    recent_posts = Blog.query.order_by(Blog.date.desc()).limit(3).all()
    categories = Blog.query.group_by(Blog.category).limit(5).all()
    tags = Tag.query.group_by(Tag.name).limit(25).all()
    search_form = Search()
    if search_form.validate_on_submit():
        return redirect(url_for('query', term=search_form.term.data))


    return render_template('query.html', tag_posts=tag_posts, search_form=search_form,
                           recent_posts=recent_posts, categories=categories, tags=tags)


@app.route("/item/<int:item_id>/<table>/<location>/delete", methods=['GET', 'POST'])
def delete_item(item_id, table, location):

    if table == 'PortfolioItem':
        item = Portfolio.query.get_or_404(item_id)
        path = os.path.join(current_app.root_path, 'static/img/portfolio', item.folder)
        shutil.rmtree(path)
        msg = "You Portfolio Item has been successfully deleted!"
    elif table == 'Blog':
        item = Blog.query.get_or_404(item_id)
        msg = "Your blog post has been successfully deleted!"
    elif table == 'Comment':
        item = Comment.query.get_or_404(item_id)
        msg = "The comment has been deleted successfully"
        db.session.delete(item)
        db.session.commit()
        flash(msg)
        return redirect(url_for('post', post_id=location))
    else:
        flash('Delete failed, try again', 'danger')
        return redirect(url_for(location))

    db.session.delete(item)
    db.session.commit()
    flash(msg, 'success')
    return redirect(url_for(location))

