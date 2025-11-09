# NOTE: here's the command for launching the containter:
# sudo docker run -p 8000:8000 backend-test

FROM ubuntu:latest

RUN yes | apt update
RUN apt install -y python3-pip
RUN apt install -y python3.12-venv

WORKDIR /backend

COPY ./requirements.txt . 

# RUN pip install --no-cache-dir -r requirements.txt
# Create and activate a virtual environment, then install dependencies
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# Ensure venv Python and pip are used by default
ENV PATH="/opt/venv/bin:$PATH"

COPY ./src ./src
COPY ./boards ./boards
COPY ./images ./images


CMD ["fastapi", "run", "src/main.py", "--port", "8000"]
# CMD ["ls"]

# If running behind a proxy like Nginx or Traefik add --proxy-headers
# CMD ["fastapi", "run", "app/main.py", "--port", "80", "--proxy-headers"]