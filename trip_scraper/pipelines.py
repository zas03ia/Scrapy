from sqlalchemy.orm import sessionmaker
from trip_scraper.models import Base, Property
from sqlalchemy import create_engine


class TripPipeline:
    def __init__(self):
        engine = create_engine(
            "postgresql+psycopg2://good_luck_zasia:zasia_assignment6@postgres_trip:5432/trip_db",
            pool_size=20,
            max_overflow=30,
            pool_timeout=120,
        )
        Base.metadata.create_all(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        item = {key: value if value != "" else None for key, value in item.items()}
        image_urls = item.get("image_urls", [])
        downloaded_image_paths = [
            image.get("path", None) for image in item.get("images", [])
        ]
        session = self.Session()
        property = Property(
            title=item["title"],
            rating=item["rating"],
            location=item["location"],
            latitude=item["latitude"],
            longitude=item["longitude"],
            room_type=item["room_type"],
            price=item["price"],
        )
        property.set_image_urls(image_urls)
        property.set_downloaded_image_paths(downloaded_image_paths)
        session.add(property)
        session.commit()
        return item
