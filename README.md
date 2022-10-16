# YOK scraping for Electrics and Electronics Engineering Major

"Data is the key!"

&emsp;The website that I scrape the data is [YÖK Atlas](https://yokatlas.yok.gov.tr/). I just scrape the Electrics-Electronics Engineering data from this link [YÖK Atlas - Universities with Electrics-Electronics Engineering Major](https://yokatlas.yok.gov.tr/lisans-bolum.php?b=10056).

### View of Website
![View of Website](https://user-images.githubusercontent.com/52218326/145977279-4a7e3866-8c44-4464-881e-5abda3ba21e7.png)

# Data
&emsp;Since all the data on the page is not necessary for processing, it is necessary to extract the data. For this reason, we need to monitor the network traffic of the website. Because the retrieved data is not kept statically in the HTML page. Data is pulled by the server when interacting with the drop-down menus.

![loading](https://user-images.githubusercontent.com/52218326/145978744-1ed4188e-6160-49e6-81d9-c972c6dca7eb.png)
![data](https://user-images.githubusercontent.com/52218326/145978781-7de17446-c26d-43bb-b527-976dea4832f2.png)

&emsp;`BeautifulSoup` framework cant interact with website. Hence, we should find the target webpage which include the queries of this data. For this reason, we should examine the network traffic.

![network_traffic](https://user-images.githubusercontent.com/52218326/145979194-ced96ad4-d88d-4161-aa58-9cd849804b0b.png)

&emsp;As we can see, there is a query which seen like `2010.php?y=105710042`. Therefore, that means target webpage is written in `PHP` and there is a `GET` data. `GET` data stands for university id. So when we type the another university id, page will fetch data about university which we typed yet. Webpage address is: `https://yokatlas.yok.gov.tr/content/lisans-dynamic/2010.php?y=105710042`. Then, when we scrape the webpage, we will just change the `$_GET['y']` value.

![target_website](https://user-images.githubusercontent.com/52218326/145979979-4a100358-9f1f-40dc-907e-0924a8d4a964.png)

Data presented in the table.

# Process
&emsp;Necessary data is listed below:
- University Informations
  - Name of the University
  - Language of Department
  - Years of Department
  - Is Department Secondary Education
  - Type of Scholarship
  - Is Department Distance Learning
  - Web Link of University
  - YÖK ID of University
- Current Student Information
  - Current Male Student
  - Current Female Student
  - Current Student
- Graduates Information
  - Number of Graduated Boys
  - Number of Graduated Girls
  - Number of Graduates
- New Students Information
  - Number of New Students
  - Exam Score of the Last Student
- Instructors Information
  - Number of Professors
  - Number of Assoc. Profs.
  - Number of Doctors
  - Total Number of Instructors
