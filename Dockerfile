# Step 1: Use the official Python image as the base image
FROM python:3.10-slim

# Step 2: Set environment variables
ENV PYTHONUNBUFFERED 1

# Step 3: Install PostgreSQL client (for connecting to PostgreSQL from the container)
RUN apt-get update && apt-get install -y \
    postgresql-client \ 
    libpq-dev gcc


# Step 4: Set the working directory inside the container
WORKDIR /app

# Step 5: Copy the requirements file to the container
COPY requirements.txt /app/

# Step 6: Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Step 7: Copy the entire project into the container
COPY . /app/

# Step 8: Expose the port for your app (adjust the port if needed)
EXPOSE 8000

# Step 9: Run Scrapy spider (replace with your spider name)
CMD ["scrapy", "crawl", "trip"]