import json
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from flask import Flask, Blueprint, jsonify, render_template


def create_app(config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, template_folder='.', static_folder='resources')

    if config:
        app.config.update(config)

    # Configure logging
    log_handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    log_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s in %(module)s: %(message)s')
    log_handler.setFormatter(formatter)
    app.logger.addHandler(log_handler)

    # Blueprint for main pages
    main_bp = Blueprint('main', __name__)

    @main_bp.route('/')
    def home():
        return render_template('index.html')

    @main_bp.route('/acerca')
    def about():
        return render_template('acerca-de.html')

    @main_bp.route('/contacto')
    def contact():
        return render_template('contacto.html')

    @main_bp.route('/oferta')
    def offer():
        return render_template('oferta-educativa.html')

    @main_bp.route('/estadisticas')
    def statistics():
        return render_template('estadisticas.html')

    @main_bp.route('/preguntas')
    def faq():
        return render_template('preguntas-frecuentes.html')

    app.register_blueprint(main_bp)

    # Blueprint for API routes
    api_bp = Blueprint('api', __name__, url_prefix='/api')
    data_file = Path('data/courses.json')

    @api_bp.route('/courses')
    def list_courses():
        if data_file.exists():
            with data_file.open('r', encoding='utf-8') as f:
                courses = json.load(f)
        else:
            courses = []
        return jsonify(courses)

    app.register_blueprint(api_bp)

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):  # pylint: disable=unused-argument
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def server_error(error):  # pylint: disable=unused-argument
        app.logger.exception('Server error: %s', error)
        return render_template('500.html'), 500

    return app


if __name__ == '__main__':
    application = create_app({'JSON_AS_ASCII': False})
    application.run(debug=True)
