# Base image with Python 3
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy your files into the container
COPY . /app

# Install required packages
RUN pip install --no-cache-dir PyPDF2 scikit-learn

# Create a 'pdfs' folder if not present (optional)
RUN mkdir -p /app/pdfs

# Run the script
CMD ["python", "main.py"]