from sqlalchemy import Column, Integer, String, Float, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    rating = Column(Float, nullable=True)
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    room_type = Column(String, nullable=True)
    price = Column(String, nullable=True)
    image_urls = Column(JSON, nullable=True)
    downloaded_image_paths = Column(JSON, nullable=True)

    def set_image_urls(self, image_urls):
        self.image_urls = image_urls

    def set_downloaded_image_paths(self, downloaded_image_paths):
        self.downloaded_image_paths = downloaded_image_paths
