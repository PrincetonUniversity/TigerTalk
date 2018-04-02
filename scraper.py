from bs4 import BeautifulSoup
import requests
import re

page = requests.get("https://odusapps.princeton.edu/StudentOrg/new/directory.php")
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[3]
body = list(html.children)[3]
clubs = body.find_all('div', class_='jumbotron')


for i in range(1, len(clubs)):
	club_data = list(clubs[i].children)
	club_name = club_data[0].get_text()
	club_data[2] = club_data[2].replace('\n', '')
	club_data[2] = club_data[2].replace('\r', '')
	club_description = club_data[2]
	club_category = club_data[4]
	info_str = ""
	if (re.search(r"Category:", club_category, re.IGNORECASE) != None):
		club_info = list(club_data[5].children)
		for j in range(len(club_info)):
			if (type(club_info[j]).__name__ == "Tag" and club_info[j].get_text() != "" and club_info[j].get_text() != " "):
				info_str += (club_info[j].get_text() + ", ")
			elif (type(club_info[j]).__name__ == "NavigableString"):
				info_str += (club_info[j] + ", ")
	else:
		club_category = ""
		for k in range(4, len(club_data)):
			if (type(club_data[k]).__name__ == "Tag" and club_data[k].get_text() != "" and club_data[k].get_text() != " "):
				info_str += (club_data[k].get_text() + ", ")
			elif (type(club_data[k]).__name__ == "NavigableString"):
				info_str += club_data[k] + ", "
	#print(club_data)
	print("%s; %s; %s; %s" % (club_name, club_description, club_category, info_str))