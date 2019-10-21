from app import app,render_template


@app.errorhandler(404)
def error_404(e):
    return render_template("errors/404.html")
