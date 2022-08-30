# Mattermost Meugnon slash command

![fly.io deploy](https://github.com/paulden/meugnon-mattermost-slash-command/actions/workflows/main.yml/badge.svg)

Simple Flask API returning meugnons links (courtesy of Imgur) to setup a Mattermost Slash command.

## Run locally

- Generate an Imgur client ID (you need an account) here: https://api.imgur.com/oauth2/addclient
- (optional) Generate a Mattermost token when registering your Slash command.
- Run using Docker, in standalone mode or with docker-compose if you want to start a local Mattermost instance.

### Using Docker

- Build and run API:

```
$ docker build -t meugnon-api .
$ docker run -e IMGUR_CLIENT_ID=<your-token> -p 8000 meugnon-api
$ curl localhost:8000/healthz      
{
  "message": "Tutto bene!"
}
```

### Standalone

- Create a `.env` file with the Mattermost tokens and the Imgur client ID as described in `.env.template` (if the
`MATTERMOST_TOKENS` is empty or not set, token validation will be skipped)
- Install required Python dependencies with a tool such as `virtualenv`:

```
$ virtualenv ./venv -p python3.8
$ source venv/bin/active
$ pip install -r requirements.txt
```

- Run and test API is up

```
$ python run.py
$ curl localhost:8000/healthz      
{
  "message": "Tutto bene!"
}
$ curl localhost:8000                              
{
  "response_type": "in_channel", 
  "text": "https://i.imgur.com/DPVf0HB.jpg"
}

```

### Run with docker-compose using a local Mattermost instance

Based on https://github.com/mattermost/mattermost-bot-sample-golang

- Start containers with `docker-compose up`.
- Run script to add users with `./add_users.sh`.
- Go to your local Mattermost instance on http://localhost:8065 and log in with `bill@example.com` / `Password1.`.
- Create a test team and authorize untrusted connections to your API by going to `System console > Environment > Developer`
and adding `meugnon-api_meugnon_1` in `Allow untrusted internal connections to`.
- Enable link preview to easily get your meugnonnerie in `System Console > Site Configuration > Posts > Enable website link previews`.
- Create your Slash command on `Integrations > Slash Commands > Add Slash Commands` and set request method to `GET`, and
request URL to `http://meugnon-api_meugnon_1:8000` (rest is your choice).

## TODO

- Tests
- Filter out MP4 links (not previewed in Mattermost :( )
- Build "cache" object with links to avoid useless calls to API
