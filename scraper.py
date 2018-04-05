from bs4 import BeautifulSoup
import requests
import re
import json

page = requests.get("https://odusapps.princeton.edu/StudentOrg/new/directory.php")
soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[3]
body = list(html.children)[3]
clubs = body.find_all('div', class_='jumbotron')

print('[')
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
		skip = False;
		for j in range(len(club_info)):
			if (skip):
				skip = False;
				continue;
			if (type(club_info[j]).__name__ == "NavigableString"):
				add = club_info[j]
				if (add == "E-mail: "):
					info_str += (add + club_info[j+1]['href'].split(':')[1] + "; ")
				else:
					name = club_info[j+1].get_text()
					email = club_info[j+1]['href'].split(':')[1]
					info_str += (add + name + ", " + email + "; ")
				skip = True;
			elif (type(club_info[j]).__name__ == "Tag" and club_info[j].name == 'a'):
				link_type = list(club_info[j].children)[0]['title']
				if (link_type == "Website"):
					link = club_info[j]['href']
					info_str += "Website: " + link + "; "
	else:
		club_category = ""
		skip = False;
		for k in range(4, len(club_data)):
			if (skip):
				skip = False;
				continue;
			if (type(club_data[k]).__name__ == "NavigableString"):
				add = club_data[k]
				if (add == "E-mail: "):
					info_str += (add + club_data[k+1]['href'].split(':')[1] + "; ")
				else:
					name = club_data[k+1].get_text()
					email = club_data[k+1]['href'].split(':')[1]
					info_str += (add + name + ", " + email + "; ")
				skip = True;
			elif (type(club_data[k]).__name__ == "Tag" and club_data[k].name == 'a'):
				link_type = list(club_data[k].children)[0]['title']
				if (link_type == "Website"):
					link = club_data[k]['href']
					info_str += "Website: " + link + "; "
	club_category = club_category[10:]
	club_category = club_category.split(',')
	if ("" in club_category):
		club_category.remove("")

	info_str = info_str.split(';')
	if (" " in info_str):
		info_str.remove(" ")

	leaders = []
	email = ""
	site = ""
	for i in range(0, len(info_str)):
		array = info_str[i].split(':')
		for j in range(0, len(array)):
			if (array[j][0] == " "):
				array[j] = array[j][1:]
			if (array[j] == "E-mail"):
				email = array[j+1][1:]
			elif (array[j] == "President" or array[j] == "Co-President" or array[j] == "Treasurer"):
				leader_info = array[j+1].split(',')
				leader = {}
				leader["leader_name"] = leader_info[0][1:]
				leader["leader_title"] = array[j]
				leader["leader_email"] = leader_info[1][1:]
				leaders.append(leader)
			elif (array[j] == "Website"):
				site = array[j+1][1:]+':'+array[j+2]


	course = json.dumps({
    	'name': club_name,
    	'desc': club_description,
    	'category': club_category,
    	'email': email,
    	'leaders': [le for le in leaders],
    	'website': site,
	})
	print(course)

print(']')