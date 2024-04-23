# Using Python 3.10 base image
FROM python:3.10

ENV TOKEN_ADDRESS asd
ENV SYMBOL GIGA

# Install poetry
RUN pip install poetry

# Set the working directory in the container
WORKDIR /app

# Copy necessary files from the host to the container
COPY pyproject.toml poetry.lock ./
COPY gigabot/ ./gigabot/
COPY .env ./


# Install dependencies using poetry in the project directory
RUN poetry install

# Set the command to run the application
ENTRYPOINT ["poetry", "run", "python", "-m", "gigabot.scripts.send_price"]
