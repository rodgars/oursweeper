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

![Screenshot 2024-06-10 at 1 47 24 AM](https://github.com/rodgars/oursweeper/assets/20528688/f59f1f5f-339f-4b77-a0ce-12e96b349c3c)

Select one level of dificulty by clicking on the respective button. In this example, let's click on Easy.

It will create a game and redirect you to the game http://localhost:3000/game/xxxxx

First time, it prompts to you to inform an username. This feature is just to help identifing which player did what move in a game with more players. Since there is no authentication the game is storing this username in your browser localstorage.

![Screenshot 2024-06-10 at 1 48 46 AM](https://github.com/rodgars/oursweeper/assets/20528688/1a697cea-c709-458a-8b5f-6f7b567bf63b)

After prompting the username, you can play the game.

![Screenshot 2024-06-10 at 1 48 58 AM](https://github.com/rodgars/oursweeper/assets/20528688/02cba52b-e53c-41fa-9f82-5d100af8c981)

You can leave the game and be back to this url whenever you want. The game state is persisted in the backend to avoid cheating.

To simulate more people playing the game, open an Incognito browser and enter a different username. Now you can play together.

![Screenshot 2024-06-10 at 1 49 47 AM](https://github.com/rodgars/oursweeper/assets/20528688/ccf93592-b598-46bb-88ff-c1e8897dadaf)

![Screenshot 2024-06-10 at 1 50 24 AM](https://github.com/rodgars/oursweeper/assets/20528688/fff6fcb0-815b-46b6-ac52-8f1b1be9b777)

Video demo:

[-- Video here](https://github.com/rodgars/oursweeper/assets/20528688/a2101fc1-d16c-453d-97cb-d5c5111a143a)

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

The project incorporates two main backend approaches: HTTP and WebSockets.

For certain features, such as creating a new game, communication between the web client and web server uses simple HTTP, where the client sends a POST request to the server, which then executes commands on the database. This represents a synchronous flow.

Conversely, more complex methods are used to allow multiple users to play a game simultaneously.

Below is the flow when a user clicks on a cell. This sequence diagram simplifies the process slightly.

This diagram illustrates a single client sending a message, but all clients connected to the same channel group will receive an updated game map.

![Screenshot 2024-06-10 at 2 06 43 AM](https://github.com/rodgars/oursweeper/assets/20528688/6b92112e-3d41-4bf7-9a08-ac07ae5d51d6)


## Limitations

This is just an example; this app is not production-ready.

It requires significant improvements and better setup.

Some enhancements to be made include:

- Refactoring synchronous code to be asynchronous in the backend to fully leverage ASGI benefits.
- Using Redis cache to store connected users in a distributed manner. The current version uses the web server instance's memory, which is adequate for testing with a single instance.
- Utilizing Channels Redis to store channels and groups in Redis.
- Adding unit tests, as there are currently none.
- Improving the UX by adding more navigation controls and displaying a list of events per user.
- Integrating secret managers to prevent the leakage of keys and security values.
- Handling reconnections in case the WebSocket connection fails on the frontend.
- Investigating the use of Redis cache to store the game state for faster communication with the client. A method is needed to asynchronously sync cache data with the database.
- Exploring the use of a NoSQL database, considering the high volume of write operations in this game scenario.
- Improve the retry mechanism in Celery workers and enhance error handling in case of failures.
- Remove the username prompt in the frontend and use an authentication provider instead.

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [React](https://reactjs.org/) - The frontend library used
- [Docker](https://www.docker.com/) - Containerization platform
- [Celery](https://docs.celeryq.dev/en/stable/django/index.html) - Fire and Forget tasks
- [Django-Channels](https://channels.readthedocs.io/en/latest/installation.html) - For real time communication using web sockets

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
