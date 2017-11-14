import requests
import json
#budget = float(input("Budget (GBP)\n>>> "))
#origin = str(input("Origin city or country\n>>> "))
#startDate = str(input("Start date (YYYY-MM-DD)\n>>> "))
#endDate = str(input("End date\n>>> "))


def apiCaller(budget, origin, startDate, endDate):
	#sets up the flight API call for the given start and end dates

     flightRequestLocation = 'http://partners.api.skyscanner.net/apiservices/browsequotes/v1.0/FR/gbp/en-US/' + origin + '/anywhere/' + startDate + '/' + endDate + '?apikey=ha393385273835879384162930498674'

	#makes the flight API call
     r_flights = requests.get(flightRequestLocation, json={"key": "ha393385273835879384162930498674"})

    	#parses the flight API data as JSON
     j_flights = r_flights.json()
    
    	#lookup for place info based on flight JSON - will allow comparison of PlaceId and Names
     placeDict = j_flights['Places']
    
    	#lookup for quote info based on flight JSON - to give DestinationId for comparison with placeDict
     quoteDict = j_flights['Quotes']
    
    	#lookup for carrier infor based on flight JSON
     carrierDict = j_flights['Carriers']
    
    	#dictionary of carrier names and carrier IDs
     carrierNameDict = {}

	#populate carrierDict
     for i in range(len(carrierDict)):
         carrierNameDict[carrierDict[i]['CarrierId']] = carrierDict[i]['Name']

	#dictionary of prices
     priceDict = {}

	#populate priceDict
     for i in range(len(quoteDict)):
         priceDict[i] = quoteDict[i]['MinPrice']

	#dictionary of locations and PlaceId
     locationDict = {}

	#populate locationDict
     for i in range(len(placeDict)):
         try:
             locationDict[placeDict[i]['PlaceId']] = placeDict[i]['CityName']
         except:
             locationDict[placeDict[i]['PlaceId']] = placeDict[i]['Name']

	#init sorts for carrier, price and location based on price
     sortedOutboundCarrier = []
     sortedInboundCarrier = []
     sortedPrice = []
     sortedLocation = []
     sortedOrigin = []

     #populates sortedPrice and sortedLocation
     for i in sorted(priceDict, key=priceDict.get):
         sortedPrice.append(priceDict[i])

		#looks up location names in locationDict using references from quoteDict
         sortedLocation.append(locationDict[quoteDict[i]['OutboundLeg']['DestinationId']])
         sortedOrigin.append(locationDict[quoteDict[i]['OutboundLeg']['OriginId']])
		#appends carrier info for direct flights - specifies non-direct routes are non-direct
         if quoteDict[i]['Direct'] == True:
              sortedOutboundCarrier.append(str(carrierNameDict[quoteDict[i]['OutboundLeg']['CarrierIds'][0]]))
              sortedInboundCarrier.append(str(carrierNameDict[quoteDict[i]['InboundLeg']['CarrierIds'][0]]))
         else:
              sortedOutboundCarrier.append("Non-direct route")
              sortedInboundCarrier.append("Non-direct route")



     print(i, priceDict[i], quoteDict[i]['OutboundLeg']['DestinationId'], locationDict[quoteDict[i]['OutboundLeg']['DestinationId']])


	#calculate remaining budget to be spent on hotels after paying for flights
     hotelBudget =[i - j for i, j in zip([budget]*len(sortedPrice), sortedPrice)]


	#eliminates destinations from consideration when flights have already used entire budget
     for i in range(len(hotelBudget)):
         if hotelBudget[i] < 0:
             hotelBudget = hotelBudget[:i]
             break

         print(hotelBudget)


	#list of potential holiday ideas within budget
     ideas = []


	#requests entity_id for each location that is still potentially within budget

     for i in range(len(hotelBudget)):
         try:
             entity_id = requests.get("http://gateway.skyscanner.net/autosuggest/v3/hotels?q=" + sortedLocation[i] + "&market=UK&locale=en-GB&apikey=72bc15a55170409a8c81aaafd6c6cf3b").json()['results'][0]['id']
         except KeyError:
             print("KeyError")
		#sets up API call for hotel prices
         hotelRequestLocation = "https://gateway.skyscanner.net/hotels/v1/prices/search/entity/" + entity_id + "?market=UK&locale=en-GB&checkin_date=" + startDate  + "&checkout_date=" + endDate + "&currency=GBP&adults=2&rooms=1&images=3&image_resolution=high&boost_official_partners=1&sort=-relevance&limit=30&offset=0&partners_per_hotel=3&enhanced=filters,partners,images,location,amenities,extras,query_location&apikey=72bc15a55170409a8c81aaafd6c6cf3b"

		#makes hotel API call and parses as JSON
         r_hotels = requests.get(hotelRequestLocation,headers={'x-user-agent':'N;B2B'})
         j_hotels = r_hotels.json()
         print(j_hotels.keys())



		#print(type(j_hotels['results']['hotels']), len(j_hotels['results']['hotels']))
         try:
             length = len(j_hotels['results']['hotels'])
         except:
             length = 0
         for j in range(length):

			#checks hotel prices are known and calculates remaining money in budget after hotel price is considered. If positive, adds it to ideas
            try:
                remainder = hotelBudget[i] - j_hotels['results']['hotels'][j]['offers'][0]['price']
                if remainder >= 0:
                    ideas.append(str(sortedLocation[i]) + " cost = £" + str(budget - remainder) + ". Outward flight from " + str(sortedOrigin[i]) + " with " + str(sortedOutboundCarrier[i]) +  ", return flight with " + str(sortedInboundCarrier[i]) + ". Staying at " + str(j_hotels['results']['hotels'][j]['name']))
			#some lists are empty: this catches them
            except:
                print("Error", len(j_hotels['results']['hotels'][j]['offers']))

     return ideas
 
s=apiCaller(400,'uk','2017-12-03','2017-12-15')
