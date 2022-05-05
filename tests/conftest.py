from flask.signals import request_finished
from app import db
import pytest
from app.models.planet import Planet 

from app import create_app

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender,response, **extra):
        db.session.remove()
    
    with app.app_context():
        db.create_all() 
        yield app
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_planets(app):
    earth = Planet(name="earth", description="green and blue", has_life=True)
    mercury = Planet(name="mercury", description="extremely hot", has_life=False)

    db.session.add(earth)
    db.session.add(mercury)
    db.session.commit()