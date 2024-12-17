import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from scrapy.http import HtmlResponse
from trip_scraper.spiders.trip import TripSpider
from trip_scraper.pipelines import TripPipeline
from sqlalchemy import create_engine
from trip_scraper.models import Base


class TestTripSpider(unittest.TestCase):

    @patch("trip_scraper.spiders.trip.random.sample")
    @patch("trip_scraper.spiders.trip.TripSpider.extract_script_data", return_value={})
    def test_parse(self, mock_extract_script_data, mock_random_sample):

        spider = TripSpider()
        mock_data = {
            "initData": {
                "htlsData": {
                    "inboundCities": [
                        {
                            "id": 1,
                        }
                    ],
                    "outboundCities": [{"id": 2}],
                }
            }
        }

        response = HtmlResponse(
            url="https://uk.trip.com/hotels/?locale=en-GB&curr=GBP",
            body=b"<html></html>",
            encoding="utf-8",
        )

        spider.extract_script_data = MagicMock(return_value=mock_data)
        result = list(spider.parse(response))

        # Calculate checkin and checkout dates

        checkin = datetime.now().strftime("%Y/%m/%d")
        checkout = (datetime.now() + timedelta(days=1)).strftime("%Y/%m/%d")

        # Verify that the URLs are being generated correctly
        self.assertEqual(
            result[0].url,
            f"https://uk.trip.com/hotels/list?city=1&checkin={checkin}&checkout={checkout}",
        )
        self.assertEqual(
            result[1].url,
            f"https://uk.trip.com/hotels/list?city=2&checkin={checkin}&checkout={checkout}",
        )

    def test_parse_hotel_list(self):
        # Test processing of hotel list
        spider = TripSpider()
        mock_hotel_data = {
            "initData": {
                "firstPageList": {
                    "hotelList": [
                        {
                            "hotelBasicInfo": {"hotelName": "Hotel 1"},
                            "commentInfo": {"commentScore": 4.5},
                        }
                    ]
                }
            }
        }

        response = HtmlResponse(
            url="https://uk.trip.com/hotels/?locale=en-GB&curr=GBP",
            body=b"<html></html>",
            encoding="utf-8",
        )

        spider.extract_script_data = MagicMock(return_value=mock_hotel_data)
        result = list(spider.parse_hotel_list(response))

        # Ensure hotel data is processed
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Hotel 1")
        self.assertEqual(result[0]["rating"], 4.5)


class TestTripPipeline(unittest.TestCase):

    @patch("trip_scraper.pipelines.sessionmaker")
    def test_process_item(self, mock_sessionmaker):
        # Setup for session mock
        mock_session = MagicMock()
        mock_sessionmaker.return_value = mock_session
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)

        # Mock an item to be processed
        item = {
            "title": "Hotel 1",
            "rating": 4.5,
            "location": "City Center",
            "latitude": 52.2053,
            "longitude": 0.1218,
            "room_type": "Deluxe",
            "price": "100",
            "image_urls": ["http://example.com/image1.jpg"],
        }

        pipeline = TripPipeline()
        pipeline.Session = mock_sessionmaker

        # Call process_item and verify the results
        result = pipeline.process_item(item, None)

        # Verify that the item was added to the session
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

        # Check if the data was correctly added to the database
        added_property = mock_session.add.call_args[0][0]
        self.assertEqual(added_property.title, "Hotel 1")
        self.assertEqual(added_property.rating, 4.5)
        self.assertEqual(added_property.location, "City Center")
        self.assertEqual(added_property.latitude, 52.2053)
        self.assertEqual(added_property.longitude, 0.1218)
        self.assertEqual(added_property.room_type, "Deluxe")
        self.assertEqual(added_property.price, "100")
        self.assertEqual(added_property.image_urls, ["http://example.com/image1.jpg"])


if __name__ == "__main__":
    unittest.main()
