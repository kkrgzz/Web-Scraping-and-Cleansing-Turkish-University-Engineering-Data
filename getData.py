from bs4 import BeautifulSoup
import requests
import pandas as pd
import os
import departments as dp
import time

start_time = time.time()

exist = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/2010.php?y="
graduate = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/2030.php?y="
instructor = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/2050.php?y="
incoming = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_2.php?y="
last_persons_score = "https://yokatlas.yok.gov.tr/content/lisans-dynamic/1000_3.php?y="

path = "./departments/"
output_path = "./departments_data/"

deps = dp.get_departments()


def control_char(data):
    if data == "-" or data == "---":
        data = 0
    data = int(data)
    return data


def control_float(data):
    if data == "-" or data == "---":
        data = 0
    else:
        data = float(data.replace(",", "."))
    return data


def get_data(dataframe, lbl):

    uni = dataframe.values.tolist()
    uni_count = len(uni)

    # uni_name = dataframe.university_name
    # uni_language = dataframe.language_of_department
    # uni_years = dataframe.years_of_department
    # uni_secondary = dataframe.is_secondary_education
    # uni_scholarship = dataframe.type_of_scholarship
    # uni_distance_learning = dataframe.is_distance_learning

    analysis = []

    i = 0
    while i < uni_count:
        # Prepare URL
        exist_link = exist + uni[i][7]
        graduate_link = graduate + uni[i][7]
        instructor_link = instructor + uni[i][7]
        incoming_link = incoming + uni[i][7]
        last_persons_score_link = last_persons_score + uni[i][7]

        # Download Website
        exist_site = requests.get(exist_link)
        graduate_site = requests.get(graduate_link)
        instructor_site = requests.get(instructor_link)
        incoming_site = requests.get(incoming_link)
        last_persons_score_site = requests.get(last_persons_score_link)

        # Get Content of Website
        exist_content = BeautifulSoup(exist_site.content, "lxml")
        graduate_content = BeautifulSoup(graduate_site.content, "lxml")
        instructor_content = BeautifulSoup(instructor_site.content, "lxml")
        incoming_content = BeautifulSoup(incoming_site.content, "lxml")
        last_persons_score_content = BeautifulSoup(last_persons_score_site.content, "lxml")

        # Attract current students
        exist_tr = exist_content.findAll("tr")
        exist_arr = []
        for tr in exist_tr:
            td = tr.findAll("td")
            for value in td:
                exist_arr.append(value.text)

        if exist_arr:
            try:
                exist_total = control_char(exist_arr[1])
            except IndexError:
                exist_total = 0
            try:
                exist_girls = control_char(exist_arr[4])
            except IndexError:
                exist_girls = 0
            try:
                exist_boys = control_char(exist_arr[7])
            except IndexError:
                exist_boys = 0

        else:
            exist_total = 0
            exist_girls = 0
            exist_boys = 0

        # Attract graduated students
        graduate_tr = graduate_content.findAll("tr")
        graduate_arr = []
        for tr in graduate_tr:
            td = tr.findAll("td")
            for value in td:
                graduate_arr.append(value.text)

        if graduate_arr:
            try:
                graduate_total = control_char(graduate_arr[1])
            except IndexError:
                graduate_total = 0
            try:
                graduate_girls = control_char(graduate_arr[3])
            except IndexError:
                graduate_girls = 0
            try:
                graduate_boys = control_char(graduate_arr[2])
            except IndexError:
                graduate_girls = 0
        else:
            graduate_total = 0
            graduate_girls = 0
            graduate_boys = 0

        # Attract instructors
        ins_tr = instructor_content.findAll("tr")
        ins_arr = []
        for tr in ins_tr:
            td = tr.findAll("td")
            for value in td:
                ins_arr.append(value.text)

        if ins_arr:
            try:
                instructor_prof = control_char(ins_arr[1])
            except IndexError:
                instructor_prof = 0
            try:
                instructor_assoc = control_char(ins_arr[3])
            except IndexError:
                instructor_assoc = 0
            try:
                instructor_dr = control_char(ins_arr[5])
            except IndexError:
                instructor_dr = 0
            try:
                instructor_total = control_char(ins_arr[7])
            except IndexError:
                instructor_total = 0

        else:
            instructor_prof = 0
            instructor_assoc = 0
            instructor_dr = 0
            instructor_total = 0

        # Attract incoming students
        incoming_tr = incoming_content.findAll("tr")
        incoming_arr = []
        for tr in incoming_tr:
            td = tr.findAll("td")
            for value in td:
                incoming_arr.append(value.text)

        if incoming_arr:
            try:
                incoming_total = control_char(incoming_arr[-1])
            except IndexError:
                incoming_total = 0
        else:
            incoming_total = 0

        # Attract last student's exam score
        last_tr = last_persons_score_content.findAll("tr")
        last_arr = []
        for tr in last_tr:
            td = tr.findAll("td")
            for value in td:
                last_arr.append(value.text)

        if last_arr:
            try:
                last_score = control_float(last_arr[3])
            except IndexError:
                last_score = 0
        else:
            last_score = 0

        result = [uni[i][0],
                  uni[i][6],
                  uni[i][7],
                  uni[i][1],
                  uni[i][2],
                  uni[i][3],
                  uni[i][4],
                  uni[i][5],
                  exist_boys,
                  exist_girls,
                  exist_total,
                  graduate_boys,
                  graduate_girls,
                  graduate_total,
                  incoming_total,
                  last_score,
                  instructor_prof,
                  instructor_assoc,
                  instructor_dr,
                  instructor_total]
        analysis.append(result)
        print(f"" + lbl + " | University Left: ", str((uni_count - (i + 1))), " - " + uni[i][0])
        i += 1

    df = pd.DataFrame(analysis, columns=["university_name",
                                         "university_yok_link",
                                         "university_yok_id",
                                         "language_of_department",
                                         "years_of_department",
                                         "is_secondary_education",
                                         "type_of_scholarship",
                                         "is_distance_learning",
                                         "existing_boys",
                                         "existing_girls",
                                         "existing_total",
                                         "graduated_boys",
                                         "graduated_girls",
                                         "graduated_total",
                                         "incoming_student_count",
                                         "last_persons_score",
                                         "professor",
                                         "associate_professor",
                                         "doctor",
                                         "total_instructor"])
    df.to_csv(output_path + "data-" + lbl + ".csv")
    print("CSV Created Successfully: " + output_path)
    df.to_pickle(output_path + "data-" + lbl + ".pkl")
    print("Pickle File Created Successfully" + output_path)


for label, value in deps.items():
    full_path = path + label + ".pkl"
    if os.path.isfile(full_path):
        df = pd.read_pickle(full_path)
        get_data(df, label)
    else:
        print("File does not exists!")

end_time = time.time()
execution_time = end_time - start_time
print("Process Successfully: " + str(execution_time) + " in seconds")