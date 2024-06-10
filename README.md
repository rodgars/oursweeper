# oursweeper

Minesweeper game built in Django & React

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

This project require npm, docker and docker compose to run the app. Make sure you install them.

As recommended, install Docker Desktop for your OS. (Author of this project used version 4.30.0)

https://docs.docker.com/compose/install/#installation-scenarios

After installing, check the version of them:

```
docker --version
```

Docker version 26.1.1, build 4cf5afa

```bash
docker-compose --version
```

Docker Compose version v2.27.0-desktop.2

### Running the App

A step by step series of examples that tell you how to get a development environment running:

1. Clone the repository:

   ```
   git clone https://github.com/rodgars/oursweeper.git
   ```

2. Navigate to the server directory:

   ```
   cd server
   ```

3. Build the Docker images:

   ```
   docker-compose up --build -d
   ```

4. Run the migration to create the tables in Postgres:

   ```
   docker-compose exec api python manage.py migrate
   ```

5. Navigate to the client directory:

   ```
   cd ..
   cd client
   ```

6. Run the frontend app:

   ```
   npm start
   ```

Now, the server should be running at `http://localhost:5000` and the client should be running at `http://localhost:3000`.

Visit http://localhost:3000 to start playing.

### How to Play

After visiting http://localhost:3000, the land page of the game shows up.

-- Img here

Select one level of dificulty by clicking on the respective button. In this example, let's click on Easy.

It will create a game and redirect you to the game http://localhost:3000/game/xxxxx

First time, it prompts to you to inform an username. This feature is just to help identify who played what move in a game with more players. Since there is no authentication the game is storing this username is your browser localstorage.

-- Img here

After prompting the username, you can play the game.

-- Img here

You can leave the game and be back to this url whenever you want. The game state is persisted in the backend.

To simulate more people playing the game, open an Incognito browser and enter a different username. Now you can play together.

Video demo:

-- Video here

To generate another game, you have to manually go back to http://localhost:3000.

## Development

While developing in the backend, you can leverage dev tools like black and mypy.

Navigate to the server directory:

```
cd server
```

And run the setup.sh script. It will create the python virtual environment and install all packages you need.

```
source setup.sh
```

To run black, you can:

```
black .
```

to format the code

```
black check
```

to check for inconsistencies

For the frontend, navigate to client folder and run:

```
npm run format
```

to format the code

## Architecture

TODO

## Limitations

This is just an example, this app is not Production Ready.

It requires a lot of improvements and better set up.

Some enhancements to be done:

- Refactoring sync code to be async in backend to leverage all advantages of ASGI.
- Use Redis cache to store connected users in a distributed way. The current version is using the memory of the web server instance (which works fine for testing since there is just one instance).
- Also use Channels Redis to store the channels and groups in Redis.
- Adding unit tests. There is none
- Improve UX, but adding more navigation controls and show list of events by user.
- Integrate secret managers for prevent leaking keys and security values

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [React](https://reactjs.org/) - The frontend library used
- [Docker](https://www.docker.com/) - Containerization platform
- [Celery](https://docs.celeryq.dev/en/stable/django/index.html) - Fire and Forget tasks
- [Django-Channels](https://channels.readthedocs.io/en/latest/installation.html) - For real time communication using web sockets

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
