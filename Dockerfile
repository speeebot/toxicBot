FROM python:3
FROM gorialis/discord.py

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/toxicBot
RUN  python -m pip install 'pymongo[srv]'
RUN  python3 -m pip install python-dotenv
RUN  python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

WORKDIR /usr/src/toxicBot

COPY . .

CMD [ "python3", "-u", "toxicBot.py" ]
