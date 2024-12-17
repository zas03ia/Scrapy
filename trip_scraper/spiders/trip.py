import scrapy
import random
import re
import json
from datetime import datetime, timedelta


class TripSpider(scrapy.Spider):
    name = "trip"
    start_urls = ["https://uk.trip.com/hotels/?locale=en-GB&curr=GBP"]

    def parse(self, response):

        json_data = self.extract_script_data(response)
        # Extract inbound and outbound cities
        cities = json_data["initData"]["htlsData"].get("inboundCities", []) + json_data[
            "initData"
        ]["htlsData"].get("outboundCities", [])

        if not cities:
            self.log("No cities found in the JSON data.")
            return

        # Select 3 random cities
        no_of_cities = len(cities)
        if no_of_cities < 3:
            self.log(f"Less than 3 cities found: {no_of_cities}")
            random_cities = cities
        else:
            random_indexes = random.sample(range(no_of_cities), 3)
            random_cities = [cities[i] for i in random_indexes]

        # Extract and process hotels from each city
        for city in random_cities:
            city_id = city.get("id", None)
            if not city_id:
                self.log(f"City ID not found for city: {city}")
                continue

            # Generate check-in and check-out dates
            checkin = datetime.now().strftime("%Y/%m/%d")
            checkout = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")

            # Create the URL
            hotel_list_url = (
                f"https://uk.trip.com/hotels/list?city={city_id}"
                f"&checkin={checkin}&checkout={checkout}"
            )

            # Yield a request to follow this URL for further parsing
            yield scrapy.Request(url=hotel_list_url, callback=self.parse_hotel_list)

    def extract_script_data(self, response):
        # Extract the script content containing the JSON data
        script_content = response.xpath(
            '//script[contains(text(), "window.IBU_HOTEL")]/text()'
        ).get()

        if not script_content:
            self.log("Script content not found. Check the XPath selector.")
            return

        # Extract JSON-like object using regex
        match = re.search(
            r"window.IBU_HOTEL\s*=\s*(\{.*?\});", script_content, re.DOTALL
        )
        if not match:
            self.log("No match for window.IBU_HOTEL. Check if the page has changed.")
            return

        try:
            json_data = json.loads(match.group(1))
            return json_data
        except json.JSONDecodeError as e:
            self.log(f"JSON Decode Error: {e}")
            return {}

    def parse_hotel_list(self, response):

        json_data = self.extract_script_data(response)
        # Extract hotels in a given city
        hotels = json_data["initData"]["firstPageList"].get("hotelList", [])
        # Limit to 10
        hotels = hotels[: min(10, len(hotels))]
        for hotel in hotels:
            yield from self.parse_location(hotel)

    def parse_location(self, hotel):

        yield {
            "title": hotel.get("hotelBasicInfo", {}).get("hotelName", "N/A"),
            "rating": hotel.get("commentInfo", {}).get("commentScore", "N/A"),
            "location": hotel.get("hotelBasicInfo", {}).get("hotelAddress", "N/A"),
            "latitude": hotel.get("positionInfo", {})
            .get("coordinate", {})
            .get("lat", "N/A"),
            "longitude": hotel.get("positionInfo", {})
            .get("coordinate", {})
            .get("lng", "N/A"),
            "price": hotel.get("hotelBasicInfo", {}).get("price", "N/A"),
            "room_type": hotel.get("roomInfo", {}).get("physicalRoomName", "N/A"),
            "image_urls": [
                image[0].get("url", None)
                for image in hotel.get("hotelBasicInfo", {}).get("hotelMultiImgs", [])
            ],
        }
