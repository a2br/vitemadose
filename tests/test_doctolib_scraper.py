from scraper.doctolib.doctolib_center_scrap import (
    get_departements,
    doctolib_urlify,
    get_coordinates,
    center_type,
    parse_doctolib_business_hours,
    get_pid,
    find_place,
)

# -- Tests de l'API (offline) --
from scraper.pattern.scraper_result import GENERAL_PRACTITIONER, DRUG_STORE, VACCINATION_CENTER


def test_doctolib_departements():
    dep = get_departements()
    assert len(dep) == 100


def test_doctolib_urlify():
    url = "FooBar 42"
    assert doctolib_urlify(url) == "foobar-42"


def test_center_type():
    type = center_type("https://doctolib.fr/center/foobar-42", "Pharmacie du centre de Saint-Malo")
    assert type == DRUG_STORE
    type = center_type("https://doctolib.fr/medecin/foobar-42", "Dr Foo Bar")
    assert type == GENERAL_PRACTITIONER
    type = center_type("https://doctolib.fr/centres-vaccination/foobar-42", "Centre Foo Bar")
    assert type == VACCINATION_CENTER


def test_business_hours():
    place = {
        "opening_hours": [
            {
                "day": 1,
                "enabled": True,
                "ranges": [
                    ["12:00", "15:00"],
                    ["16:00", "17:00"],
                ],
            },
            {
                "day": 2,
                "enabled": False,
            },
        ]
    }
    emptyPlace = {
        "opening_hours": []
    }
    assert parse_doctolib_business_hours(place) == {"lundi": "12:00-15:00, 16:00-17:00", "mardi": None}
    assert parse_doctolib_business_hours(emptyPlace) == None

def test_doctolib_coordinates():
    docto = {"position": {"lng": 1.381, "lat": 8.192}}
    long, lat = get_coordinates(docto)
    assert long == 1.381
    assert lat == 8.192


def test_doctolib_get_pid():
    urlWithPid = "someURL?pid=somePid"
    urlWithoutPid = "someURL"
    assert get_pid(urlWithPid) == "somePid"
    assert get_pid(urlWithoutPid) == ""


def test_doctolib_find_place():
    places = [
            {
                "id": "0",
                "name": "someone"
            },
            {
                "id": "1",
                "name": "like you"
            },
        ]
    urlWithPid = f"someURL?pid=1"
    urlWithoutPid = "someURL"

    assert find_place(places, urlWithoutPid)["name"] == "someone";
    assert find_place(places, urlWithPid)["name"] == "like you";
