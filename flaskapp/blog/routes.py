from flask import request, current_app, flash, redirect, url_for, render_template

from flaskapp.blog import bp
from flask_login import login_required

from flaskapp.blog.forms import NewBlogPostForm
from flaskapp.blog import models as MongoModels

@bp.route("/new_post", methods=["POST", "GET"])
@login_required
def new_post():
    form = NewBlogPostForm()
    if request.method == "POST" and form.validate_on_submit():
        blog_post = MongoModels.BlogPost(title=form.title.data, body=form.body.data).save()
        current_app.logger.info("Blog post added: %s", form.title.data)
        flash("Blog Post Added")
        return redirect(url_for("blog.home"))
    return render_template("blog/new_blog_post.html", form=form)

@bp.route("/")
@login_required
def home():
    return render_template("blog/home.html")


