# Start from a base image (e.g., debian with a specific architecture, amd64)
FROM debian:latest

# Set environment variables
ENV PATH=/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV LANG=C.UTF-8
ENV GPG_KEY=E3FF2839C048B25C084DEBE9B26995E310250568
ENV PYTHON_VERSION=3.9.21
ENV PYTHON_SHA256=3126f59592c9b0d798584755f2bf7b081fa1ca35ce7a6fea980108d752a05bb1

# Install Python and other dependencies (from the provided image layers)
RUN /bin/sh -c set -eux; \
    apt-get update && apt-get install -y \
    python3=${PYTHON_VERSION} \
    python3-pip \
    && apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies
RUN /bin/sh -c pip3 install -r requirements.txt

# Copy the remaining application files into the container
COPY . .

# Run the helper script (from your layers)
RUN /bin/sh -c python langchain_helper.py

# Expose port 5000 (or the port your application will run on)
EXPOSE 5000

# Define the default command to run when the container starts
CMD ["python", "api.py"]
