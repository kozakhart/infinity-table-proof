FROM python:3.11-slim

# Copy requirements.txt and install dependencies
COPY requirements.txt /
RUN pip install --upgrade pip --root-user-action=ignore
RUN pip install --upgrade -r requirements.txt --root-user-action=ignore

# Install netcat for health checks
RUN apt-get update && apt-get install -y netcat-openbsd

# Optional: List installed packages for debugging
RUN pip list > /pp.txt

# Copy the source code
COPY . /

# Copy entrypoint script and set executable permissions
COPY /entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint
CMD ["/entrypoint.sh"]
