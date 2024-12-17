# Trip Scraper

This project is a web scraping application built using Scrapy that extracts hotel data from the Trip.com website. It fetches hotel details, including hotel names, ratings, locations, room types, and prices for different cities. The project also stores the scraped data in a PostgreSQL database and downloads hotel images.

## Prerequisites

To run this project, make sure you have the following software installed:

- **Python 3.x** (Recommended: Python 3.8 or higher)
- **PostgreSQL** (For storing the scraped data)
- **Scrapy** (For web scraping)
- **SQLAlchemy** (For database interactions)
- **Psycopg2** (For PostgreSQL integration)
- **Docker** (If you want to run PostgreSQL inside a container)

## Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/zas03ia/trip_scraper.git
    cd trip_scraper
    ```

2. **Create a virtual environment**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
    ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up the PostgreSQL database**:

    - Ensure you have PostgreSQL running on your machine or use Docker to start a PostgreSQL container.

    - **Docker** (Optional):

        If you want to run PostgreSQL in Docker, use the following commands to spin up a container:

        ```bash
        docker run --name trip_postgres -e POSTGRES_USER=<> -e POSTGRES_PASSWORD=<> -e POSTGRES_DB=trip_db -p 5432:5432 -d postgres
        ```

  
        ```

5. **Run the spider**:

    Once everything is set up, you can run the Scrapy spider to start scraping hotel data:

    ```bash
    scrapy crawl trip
    ```

    This will initiate the web scraping process and store the extracted data in your PostgreSQL database.

6. **Run tests**:

   ```bash
    pip install coverage
    coverage run -m unittest discover
    coverage report
    ```

7. **Access Database**:

   ```bash
   docker exec -it <container_name> psql -U <username> -d <database_name>
   SELECT * FROM properties;
   ```

## Project Structure

The project is structured as follows:

```
trip_scraper/
├── tests/
├── trip_scraper/
│   ├── spiders/
│   │   └── trip.py              # Spider for scraping hotel data
│   ├── pipelines.py             # Pipeline for saving data to the database
│   ├── models.py                # SQLAlchemy models for the database
│   ├── settings.py              # Scrapy settings and configurations
│   ├── middlewares.py           # Custom middlewares
│   └── __init__.py              # Package initialization
│
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration for PostgreSQL
└── README.md                    # This README file
```

## Scrapy Spider

The `TripSpider` class is responsible for scraping hotel data. It starts by fetching city data, then retrieves hotel details for randomly selected cities, and processes hotel data, including:

- Hotel name
- Rating
- Location
- Latitude and Longitude
- Room type
- Price
- Hotel images

The spider saves the data to a PostgreSQL database using the `TripPipeline`.

## Database Model

The SQLAlchemy model `Property` defines the structure of the data stored in the PostgreSQL database. The fields include:

- `title`: Hotel name
- `rating`: Hotel rating
- `location`: Hotel location/address
- `latitude`: Latitude coordinate
- `longitude`: Longitude coordinate
- `room_type`: Type of room
- `price`: Room price
- `image_urls`: URLs of hotel images
- `downloaded_image_paths`: Paths of downloaded images

## Pipelines

The `TripPipeline` handles saving scraped hotel data to the PostgreSQL database. It processes each item, ensuring the data is valid and then stores it in the `properties` table.


## Settings
- **Image Downloading**: The `scrapy.pipelines.images.ImagesPipeline` is used to download hotel images and save them in the `images/` directory.

## Troubleshooting

- If the spider fails to run, check the log messages for errors such as connection issues to the database or invalid data extraction.
- Ensure the PostgreSQL database is up and running before attempting to crawl the website.
- Verify the XPath selectors for extracting JSON data in case Trip.com's HTML structure has changed.

