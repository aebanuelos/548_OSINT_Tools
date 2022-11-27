
import requests     #pip install requests   
import googlemaps   #pip install googlemaps
import pandas as pd #pip install pandas
import time         #can you install time tho :bigthink:?
import openpyxl     #pip install openpyxl

#https://www.youtube.com/watch?v=YwIu2Rd0VKM  <---- Tutorial


API_KEY = open('API_KEY.txt', 'r').read() #Do not post the key in the repo, it could be used illegally
map_client = googlemaps.Client(API_KEY) #Spawn an API instance with our api key




#=========Define/Insert all the search parameters here:=================
location = (40.74787101548576, -73.98719068032894)  #Google maps coords
search_string = 'Police' #What we are looking for, Google uses its own mumbo jumbo to actually find it
distance = 1000 #Distance in meters from the location DONT OVERSET THIS OR YOU RISK USING UP ALL API CREDITS!!!!



#============This gets all the data==================

business_list = [] #This will contain all of our data
gmaps_response = map_client.places_nearby( #We feed our above variables to this google maps method
    location = location,
    keyword = search_string,
#    name = 'ramen',          #If we want a certain string in the name of a place we can use the name variable
    radius = distance
)

business_list.extend(gmaps_response.get('results'))  #Whatever it gets from the API it will append to the business list
next_page_token = gmaps_response.get('next_page_token')
while next_page_token:      #The API actually returns only one page of results, we need this loop to make sure we get data from all pages
    time.sleep(1)   #The API has a limit
    gmaps_response = map_client.places_nearby(
        location = location,
        keyword = search_string,
#        name = 'ramen',
        radius = distance
    )
    business_list.extend(gmaps_response.get('results'))
    next_page_token = gmaps_response.get('next_page_token')





df = pd.DataFrame(business_list)
df['url'] = 'www.google.com/maps/place/?q=place_id:' + df['place_id']

print(df)
writer = pd.ExcelWriter( search_string + '.xlsx')
df.to_excel(writer)
writer.save()
