#Python- Devashish Thakur
#WebScrapping using BeautifulSoup and Python
from tkinter import  *
import requests
from bs4 import BeautifulSoup
def Analyse(Data):
    Pointrating = []
    LatestMovieDate = int(((Data[0])['date'])[0] + ((Data[0])['date'])[1])
    LatestMovieMonth = ((Data[0])['date'])[3:6]
    for Movie in Data:
        points = 0
        if Movie['rating'] >= 4.5:
            points = points + 10
        elif Movie['rating'] >= 4 and Movie['rating'] < 4.5:
            points = points + 8
        elif Movie['rating'] >= 3.5 and Movie['rating'] < 4:
            points = points + 4
        elif Movie['rating'] >= 2 and Movie['rating'] < 3.5:
            points = points + 1
        else:
            points = points + 0


        if Movie['time'] < 120:
            points = points + 5
        elif Movie['time'] < 150 and Movie['time'] >= 120:
            points = points + 3
        else:
            points = points + 1

        if (Movie['date']):

            if (LatestMovieDate - int((Movie['date'])[0] + (Movie['date'])[1]) < 7 and LatestMovieMonth == (Movie['date'])[3:6]):
                points = points + 10
            elif (int((Movie['date'])[0] + (Movie['date'])[1]) - LatestMovieDate < 14 and int((Movie['date'])[0] + (Movie['date'])[1]) - LatestMovieDate >= 7 and LatestMovieMonth == (Movie['date'])[3:6]):
                points = points + 5
            else:
                points = points + 1
        else:
            points = points + 0
        Pointrating.append(points)

        #print(Movie['name']," : " ,points)

    print("Best movie you can watch is : ",end = " ")

    maxScore = 0
    index = 0
    for i in range(len(Pointrating)):
        if Pointrating[i] > maxScore:
            maxScore = Pointrating[i]
            index = i
    print((Data[index])['name'],end = " ")
    print("With a Score of ",maxScore,"/ 25 (Considering Movie Rating, Duration and Release Date")
    #print(Data[index])
    print("\n")
    print("MOVIE NAME       : ",(Data[index])['name'])
    print("MOVIE RATING     : ", (Data[index])['rating'])
    print("MOVIE DATE       : ", (Data[index])['date'])
    print("MOVIE DURATION   : ", (Data[index])['time']," mins")

    result.config(text = "with a score of "+str((maxScore/25)*100)+"%"+" (Considering ratings,duration and release date)\n"
                                                          "\n\nMOVIE NAME     : "+(Data[index])['name']+"\n"
                                                            "MOVIE RATING     : "+ str((Data[index])['rating'])+"\n"
                                                            "MOVIE DATE       : "+ str((Data[index])['date']))
def movie_spider():
    url = 'https://timesofindia.indiatimes.com/entertainment/hindi/movie-reviews'
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    contain = soup.findAll("div", {"class", "FIL_right"})
    allData = []
    for element in contain:
        TempDictionary = {}
        title = element.a.h3
        link = "https://timesofindia.indiatimes.com" + element.a.get('href')

        #print("Name of Movie : " + title.string)
        # print(element.h4.string.strip())
        TempDictionary['name'] = title.string
        DateAndTime = str(element.h4.string.strip())
        Date = ""
        if ('|' in DateAndTime):
            for i in DateAndTime:
                if (i != "|"):
                    Date = Date + i
                else:
                    break
            #print("Date : " + Date)

        TempDictionary['date'] = Date
        '''
        We are calculating time in mins using below block
        '''

        time = 0
        if (len(DateAndTime) > 14):
            if (int(DateAndTime[15]) == 1):
                time = time + 60
            elif (int(DateAndTime[15]) == 2):
                time = time + 120

            time = time + int(DateAndTime[20] + DateAndTime[21] + DateAndTime[22])
            #print("Time in mins : ", time)

        TempDictionary['time'] = time
        '''
        Using to get Rating for that movie
        '''
        Criticrating = element.findAll("span", {"class", "star_count"})
        rating = float(str(Criticrating[0].text.strip()))
        #print("Rating : ", rating)
        TempDictionary['rating'] = rating
        allData.append(TempDictionary)
    #print(allData)

    #for i in allData:
    #   print(i)

    Analyse(allData)



root = Tk()
result = Label(root)
result.pack()
button1 = Button(root,text = "Analyze",command = movie_spider)
button1.pack()
root.mainloop()

