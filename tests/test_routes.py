def test_get_all_planets_with_empty_db_return_empty_list(client):
    response = client.get('/planets')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == []

def test_get_one_planet(client, two_planets):
    response = client.get("/planets/1")
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "name": "earth",
        "description": "green and blue",
        "has_life": True
    }

def test_get_one_planet_empty_db_returns_404(client):
    response = client.get("/planets/1")

    assert response.status_code == 404

def test_get_all_planets(client, two_planets):
    response = client.get('/planets')
    response_body = response.get_json()

    assert response.status_code == 200
    assert response_body == [
    {
        "id": 1,
        "name": "earth",
        "description": "green and blue",
        "has_life": True
    },
    {
        "id": 2,
        "name": "mercury",
        "description": "extremely hot",
        "has_life": False
    } ]

def test_create_planet_returns_201(client):
    response = client.post('/planets', json={
        "name": "venus",
        "description": "women only",
        "has_life": False
    })
    response_body = response.get_json()

    assert response.status_code == 201
    assert response_body == {
        "id": 1,
        "name": "venus",
        "description": "women only",
        "has_life": False
    }