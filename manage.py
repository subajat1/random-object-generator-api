from flask.cli import FlaskGroup

from app import app, db
from app.api.models.file import File

cli = FlaskGroup(app)


@cli.command('recreate_db')
def recreate_db() -> None:
    """CLI helper to recreate db"""
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command('seed_db')
def seed_db() -> None:
    """CLI helper to seed db with some data"""
    db.session.add(File(filename='seeded_file_data'))
    db.session.commit()


if __name__ == "__main__":
    cli()
