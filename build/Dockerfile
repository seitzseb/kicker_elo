FROM python:3.11-slim

# Set the working directory inside the container

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Define the default command
CMD ["python", "../update_elo.py"]
