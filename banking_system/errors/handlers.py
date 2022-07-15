from flask import Blueprint, render_template

errors = Blueprint('errors', __name__)

@errors.app_errorhandler(404)
def error_404(error):
    """
        error 404
        render the template to show this error
        template: 404.html
    """
    return render_template('errors/404.html'), 404

@errors.app_errorhandler(403)
def error_403(error):
    """
        error 403
        render the template to show this error
        template: 403.html
    """
    return render_template('errors/403.html'), 403

@errors.app_errorhandler(500)
def error_500(error):
    """
        error 500
        render the template to show this error
        template: 500.html
    """
    return render_template('errors/500.html'), 500
