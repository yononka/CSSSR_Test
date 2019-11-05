import requests
import pytest
import json


base_URL = "https://superhero.qa-test.csssr.com/"

birthday_value = "2019-05-22"
city_value = "London"
fullName_value = "Tom Smith"
gender_value = "M"
mainSkill_value = "Hunting"
phone_value = "+74991111111"

superhero_obj = {
    "birthDate": birthday_value,
    "city": city_value,
    "fullName": fullName_value,
    "gender": gender_value,
    "mainSkill": mainSkill_value,
    "phone": phone_value
}


def test_get_all_superheroes():
    res = requests.get(base_URL + "superheroes")
    assert res.status_code == 200, "Status code is not 200"
    assert len(res.json()) != 0, "The response has no items"


@pytest.mark.parametrize("birthday_param, expected_code", [(birthday_value, 200),
                                                           ("", 400),
                                                           ("0000-00-00", 400),
                                                           ("10/01/2019", 400),
                                                           ("texttest", 400)])
def test_post_birthDate(birthday_param, expected_code):
    superhero_obj["birthDate"] = birthday_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["birthDate"] == birthday_param



@pytest.mark.parametrize("city_param, expected_code", [(city_value, 200),
                                                           ("", 400),
                                                           (" ", 400),
                                                           ("!@#$%^&*()_:\"?><", 200)])
def test_post_city(city_param, expected_code):
    superhero_obj["city"] = city_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["city"] == city_param


@pytest.mark.parametrize("fullName_param, expected_code", [(fullName_value, 200),
                                                           ("", 400),
                                                           (" ", 400),
                                                           ("Некто#$%^&*()\n_:\"?><", 200)])
def test_post_fullName(fullName_param, expected_code):
    superhero_obj["fullName"] = fullName_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["fullName"] == fullName_param
        
        
@pytest.mark.parametrize("gender_param, expected_code", [(gender_value, 200),
                                                         ("F", 200),
                                                         ("", 400),
                                                         (" ", 400),
                                                         ("MM", 400),
                                                         ("!@#$%^&*()_:\"?><", 400)])
def test_post_gender(gender_param, expected_code):
    superhero_obj["gender"] = gender_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["gender"] == gender_param


@pytest.mark.parametrize("mainSkill_param, expected_code", [(mainSkill_value, 200),
                                                           ("", 400),
                                                           (" ", 400),
                                                           ("!@#$%^&*()_:\"?><", 200)])
def test_post_mainSkill(mainSkill_param, expected_code):
    superhero_obj["mainSkill"] = mainSkill_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["mainSkill"] == mainSkill_param



@pytest.mark.parametrize("phone_param, expected_code", [(phone_value, 200),
                                                           ("", 200),
                                                           ("!@#$%^&*()_:\"?><", 200)])
def test_post_phone(phone_param, expected_code):
    superhero_obj["phone"] = phone_param
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == expected_code
    if res.status_code == 200:
        res_data = res.json()
        assert res_data["phone"] == phone_param


def test_get_superhero_Id():
    res_data = create_superhero()
    heroid = res_data["id"]

    gethero_res = requests.get(base_URL + "superheroes/" + str(heroid))
    assert gethero_res.status_code == 200
    assert len(gethero_res.json()) != 0, "The response has no items"
    hero_data = gethero_res.json()

    assert hero_data["birthDate"] == "2019-05-22"
    assert hero_data["city"] == "London"
    assert hero_data["fullName"] == "Tom Smith"
    assert hero_data["gender"] == "M"
    assert (hero_data["id"] != None) and (hero_data["id"] != "") and (hero_data["id"] != []);
    assert hero_data["mainSkill"] == "Hunting"
    assert hero_data["phone"] == "+74991111111"


def test_put_superhero_Id():
    res_data = create_superhero()
    heroid = res_data["id"]

    newsuperhero_obj = {
        "birthDate": "2019-12-25",
        "city": "Rome",
        "fullName": "Just Hero",
        "gender": "F",
        "mainSkill": "Cooking",
        "phone": "+74991111133"
    }

    changehero_res = requests.put(base_URL + "superheroes/" + str(heroid), json=newsuperhero_obj)
    assert changehero_res.status_code == 200
    getnewhero_res = requests.get(base_URL + "superheroes/" + str(heroid))
    assert getnewhero_res.status_code == 200
    assert len(getnewhero_res.json()) != 0, "The response has no items"
    newhero_data = getnewhero_res.json()

    assert newhero_data["birthDate"] == "2019-12-25"
    assert newhero_data["city"] == "Rome"
    assert newhero_data["fullName"] == "Just Hero"
    assert newhero_data["gender"] == "F"
    assert newhero_data["mainSkill"] == "Cooking"
    assert newhero_data["phone"] == "+74991111133"


def test_delete_superhero_Id():
    res_data = create_superhero()
    heroid = res_data["id"]

    delhero_res = requests.delete(base_URL + "superheroes/" + str(heroid))
    assert delhero_res.status_code == 200

    res = requests.get(base_URL + "superheroes")
    assert res.status_code == 200

    allids = []
    res_data = res.json()
    json_data = json.dumps(res_data)
    item_dict = json.loads(json_data)
    for element in item_dict:
        allids.append(element['id'])

    assert heroid not in allids




def create_superhero():
    res = requests.post(base_URL + "superheroes", json=superhero_obj)
    assert res.status_code == 200
    res_data = res.json()
    return res_data
