from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import departments

deps = departments.get_departments()

department_url = "https://yokatlas.yok.gov.tr/lisans-bolum.php?b="
file_path = "./departments/"


def prep_url(suffix):
    url = department_url + suffix
    return url


def parse_name(name):
    english = name.find("(İngilizce)")
    german = name.find("(Almanca)")
    french = name.find("(Fransızca)")
    eng_fr = name.find("(İngilizce-Fransızca)")
    years_in_sentence = name.find("(4 Yıllık)")
    secondary_education = name.find("(İÖ)")
    scholarship = name.find("(Burslu)")
    half_scholarship = name.find("(%50 İndirimli)")
    quarter_scholarship = name.find("(%25 İndirimli)")
    paid = name.find("(Ücretli)")
    online = name.find("(Uzaktan Öğretim)")

    kktc = name.find("(KKTC Uyruklu)")
    other = name.find("(UOLP-ECAM-Lyon)")
    other2 = name.find("(UOLP-SUNY Buffalo)")
    other3 = name.find("(UOLP-Azerbaycan Mimarlık ve İnşaat Üniversitesi)")
    other4 = name.find("(UOLP-SUNY Binghamton)")
    other5 = name.find("(UOLP-Uluslararası Saraybosna Üniversitesi)")

    # Properties of Department
    language = ""
    years = 4
    isSecondaryEducation = False
    scholar = ""
    distance_learning = False

    # Language of Department
    if english != -1:
        name = name.replace("(İngilizce)", "")
        language = "english"
    elif german != -1:
        name = name.replace("(Almanca)", "")
        language = "german"
    elif french != -1:
        name = name.replace("(Fransızca)", "")
        language = "french"
    elif eng_fr != -1:
        name = name.replace("(İngilizce-Fransızca)", "")
        language = "english and french"
    else:
        language = "turkish"

    # Years of Department
    if years_in_sentence != -1:
        name = name.replace("(4 Yıllık)", "")
        years = 4
    else:
        years = 4

    # Secondary Education Information
    if secondary_education != -1:
        name = name.replace("(İÖ)", "")
        isSecondaryEducation = True
    else:
        isSecondaryEducation = False

    # Scholarship State
    if scholarship != -1:
        name = name.replace("(Burslu)", "")
        scholar = "full scholarship"
    elif half_scholarship != -1:
        name = name.replace("(%50 İndirimli)", "")
        scholar = "half scholarship"
    elif quarter_scholarship != -1:
        name = name.replace("(%25 İndirimli)", "")
        scholar = "quarter scholarship"
    elif paid != -1:
        name = name.replace("(Ücretli)", "")
        scholar = "paid"
    else:
        scholar = "state university"

    # Distance Learning
    if online != -1:
        name = name.replace("(Uzaktan Öğretim)", "")
        distance_learning = True
    else:
        distance_learning = False

    if kktc != -1:
        name = name.replace("(KKTC Uyruklu)", "")

    if other != -1:
        name = name.replace("(UOLP-ECAM-Lyon)", "")
    if other2 != -1:
        name = name.replace("(UOLP-SUNY Buffalo)", "")
    if other3 != -1:
        name = name.replace("(UOLP-Azerbaycan Mimarlık ve İnşaat Üniversitesi)", "")
    if other4 != -1:
        name = name.replace("(UOLP-SUNY Binghamton)", "")
    if other5 != -1:
        name = name.replace("(UOLP-Uluslararası Saraybosna Üniversitesi)", "")

    # Remove blank characters
    name = name.strip()

    output = [name, language, years, isSecondaryEducation, scholar, distance_learning]
    return output


def get_address(label, value):

    r = requests.get(prep_url(value))
    page = "https://yokatlas.yok.gov.tr/"

    file_name = label
    file_name_pkl = file_name + ".pkl"

    soup = BeautifulSoup(r.content, "lxml")

    links = soup.findAll("h4", {'class': 'panel-title'})

    universities = []
    arr = []
    if os.path.isfile(file_path + file_name_pkl):
        df = pd.read_pickle(file_path + file_name_pkl)
        print("exist")
        print(df)

    else:
        for link in links:
            children = link.findChildren("a", recursive=False)
            for child in children:
                main_link = page + child.get('href')
                ch = child.findChildren("div")
                uni_number = child.get('href')[-9:]
                for div in ch:
                    details = parse_name(div.text)

                    name = details[0]
                    language = details[1]
                    years = details[2]
                    isSecondaryEducation = details[3]
                    scholarship = details[4]
                    distance_learning = details[5]

                    arr = [name,
                           language,
                           years,
                           isSecondaryEducation,
                           scholarship,
                           distance_learning,
                           main_link,
                           uni_number]

                    universities.append(arr)

        df = pd.DataFrame(universities, columns=["university_name",
                                                 "language_of_department",
                                                 "years_of_department",
                                                 "is_secondary_education",
                                                 "type_of_scholarship",
                                                 "is_distance_learning",
                                                 "university_link",
                                                 "university_id"])
        df.to_pickle(file_path + file_name_pkl)


def main():
    for label, value in deps.items():
        get_address(label, value)


main()
