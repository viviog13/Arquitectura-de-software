# services/users/manage.py


import unittest
import coverage

from flask.cli import FlaskGroup

from project import create_app, db   # <-- nuevo
from project.api.models import User  # <-- nuevo

# configurando informes de covertura con coverage 4.5.1
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()


app = create_app()  # <-- nuevo
cli = FlaskGroup(create_app=create_app)  # <-- nuevo

@cli.command()
def cov():
    """Ejecuta las pruebas unitarias con covertura."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Resumen de covertura:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1
    

@cli.command()
def recreate_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def test():
    """ Ejecuta las pruebas sin cobertura de codigo"""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def seed_db():
    """Seeds the database."""
    db.session.add(User(username='fredy', email="abelthf@gmail.com"))
    db.session.add(User(username='abel', email="abel.huanca@upeu.edu.pe"))
    db.session.commit()


if __name__ == '__main__':
    cli()
