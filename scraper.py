import requests
from bs4 import BeautifulSoup

all_href = []
athlete_database = [] # [Name,School, Times...Times, Average, Personal Best, # of Results Found]

# Making a GET request
r = requests.get('https://www.tfrrs.org/lists/4228/Big_West_Outdoor_Performance_List')

# Parsing the HTML
soup = BeautifulSoup(r.content, 'html.parser')

# find all the anchor tags with "href"
for link in soup.find_all('a'):
	all_href.append(link.get('href'))
all_href = list(filter(lambda item: item is not None, all_href))#remove all 'none' values

#goes through a list of href links and returns list of all links that point to individual athletes
athlete_links = []    
for link in all_href:
    if link[0:30] == 'https://www.tfrrs.org/athletes':
        athlete_links.append(link)

hurdle_links = []
onetens = athlete_links[370:395] #for the 2023 Performance Lists, 370:395 yeilds the top 25 110m Mens Hurdlers
for hurdler in onetens:
    h = requests.get(hurdler + '#progression')
    hsoup = BeautifulSoup(h.content, 'html.parser') #tab-content.pt-20.col-lg-12
    hurdle_links.append(hsoup)
    
    count=39 #add each hurdler to athlete database 
    temp_school = ''
    while(hurdler[count]!='/'):
        temp_school+=hurdler[count:count+1]
        count+=1
    athlete_database.append([hurdler[count+1::],temp_school])
    
#for ath in athlete_database:
    #print(ath)

history = []
numbers = []
ath_index = 0
for ath in hurdle_links:#for every 110 hurdle athlete
    history = []#empty history
    numbers=[]#emtpy numbers
    known_times = [] 
    for time in ath.findAll("a"):#get all text with html tag 'a'
        history.append(time.get_text())#add to history
    for line in history:
        start = 0
        end = 0
       
        while end<len(line):#this loop finds all numbers in the text and adds them to the list numbers
            if not (line[end].isnumeric()):#if index end of line isnt a number, increment end
                end+=1
            else:
                start = end
                while (end < len(line) and (line[end].isnumeric() or line[end] == "." or line[end] == ':')):  
                    end+=1
                
                try:
                    if (end < len(line) and line[end] == 'm'):#confirm that number is a time and not a distance (m = meters)
                        pass
                    else:
                        numbers.append(float(line[start:end]))#add time to numbers list as a float
                except:
                    pass
    for time in numbers:
        if time > 13.0 and time < 17.0:#confirm number is in the realistic range for a hurdle time to exclude all non-hurdle times
            if time not in known_times:
                athlete_database[ath_index].append(time)#add all times to their respective athlete
                known_times.append(time)
            else:
                pass
    ath_index+=1

display = []
temp_ath = []
for person in athlete_database:
    temp_ath = []
    index = 2 
    avg = 0
    pb = person[2]
    count = 0
    while (index < len(person)):
        avg += person[index]
        count+=1
        if person[index] < pb:
            pb = person[index]
        index+=1
    temp_ath.append(person[0])
    temp_ath.append(person[1])
    temp_ath.append("Average Time: " + str(round(avg/(len(person)-2), 2)))
    temp_ath.append("Personal Best: " + str(pb))
    temp_ath.append(str(count) + " Results Found")
    display.append(temp_ath)

#rank by time
pr_rank = 1
for athlete in display:
   athlete.append("PR Rank: " + str(pr_rank))
   pr_rank+=1
   
#rank by average
sort_temp = []#bubble sort
rng = len(display) #bubble sort to place list in order from lowest avg time to highest avg time
for i in range(rng):
    for j in range(rng-i-1):
        if display[j][2] > display[j+1][2]:
            display[j],display[j+1]=display[j+1],display[j]
avg_rank = 1
for athlete in display:
   athlete.append("AVG Rank: " + str(avg_rank))
   avg_rank+=1
   print(athlete)

graphit = False;#change to true if you want graphs of all athlete results
if (graphit):
    for athlete in athlete_database:
        plt.plot(athlete[2::])
        plt.show()
###Team Vs. Team Scoring Based on PR's### 1st Place: 5pts, 2nd Place: 3pts, 3rd Place: 1pt
team1 = "UC_Irvine" #Enter Team 1 (Replace Spaces with "_")
team2 = "UC_Santa_Barbara" #Enter Team 2 (Replace Spaces with "_")
Head2Head = []
for athlete in display:
    temp_athlete = []
    if (athlete[1] == team1 or athlete[1] == team2):#if athlete is from a competing team
        temp_athlete.append(athlete[1])
        temp_athlete.append(athlete[-4])
        temp_athlete.append(athlete[-5])
    if (temp_athlete != []):#if temp_athlete was modified, add to head2head
        Head2Head.append(temp_athlete)

sort_temp = []#bubble sort
rng = len(Head2Head) #bubble sort to place list in order from lowest time to Highest time
for i in range(rng):
    for j in range(rng-i-1):
        if Head2Head[j][1] > Head2Head[j+1][1]:
            Head2Head[j],Head2Head[j+1]=Head2Head[j+1],Head2Head[j]
team1_score = 0.0
team2_score = 0.0

for i in range(3):
    if (len(Head2Head)>i):
        if len(Head2Head) >= (i+1) and float(Head2Head[i+1][1][-5:]) == float(Head2Head[i][1][-5:]):
           if i==2:
               team1_score+=0.5
               team2_score+=0.5
               break
           elif i==1:
               team1_score+=2
               team2_score+=2
               break
           elif i == 0:
               team1_score+=4
               team2_score+=4
               i+=1
               pass
        elif Head2Head[i][0] == team1:
           if i==2:
               team1_score+=1
           elif i==1:
               team1_score+=3
           elif i == 0:
               team1_score+=5
        elif Head2Head[i][0] == team2:
           if i==2:
               team2_score+=1
           elif i==1:
               team2_score+=3
           elif i == 0:
               team2_score+=5 
print(team1_score)
print(team2_score)
