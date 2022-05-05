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