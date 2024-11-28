FROM python:3.12

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    libncurses5 \
    firebird2.5-classic \
    firebird-dev

# Create symbolic links for the Firebird client library
RUN ln -s /usr/lib/x86_64-linux-gnu/libfbclient.so.2.5 /usr/lib/libfbclient.so

# Set the environment variable
ENV LD_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu:/usr/lib

# Set the working directory
WORKDIR /bot

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Command to run your application
CMD ["python", "main.py"]