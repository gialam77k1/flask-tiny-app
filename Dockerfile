FROM python:3.9-slim

# Thiết lập thư mục làm việc
WORKDIR /app

# Copy the rest of the application
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Create the instance folder
RUN mkdir -p instance

# Initialize the database
RUN flask --app flaskr init-db

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=flaskr
ENV FLASK_ENV=production

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]