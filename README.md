# toxicBot
A Toxicity bot for Discord using [Perspective API](https://www.perspectiveapi.com/) and [PyMongo](https://github.com/mongodb/mongo-python-driver)  

1. Create a [MongoDB](https://www.mongodb.com/basics/create-database) database and make a Discord bot [account](https://discordpy.readthedocs.io/en/stable/discord.html).
2. Define the environment variables in the .env file.
3. Make sure [Docker](https://docs.docker.com/engine/install/) is installed and generate a Docker image: ```docker build -t toxicBot .```
4. Then bring the bot online: ```docker run toxicBot```.
5. Lastly, invite the bot to your server with the URL printed in the terminal.
6. After some chats, use $toxicscore to show average toxicity of user.
