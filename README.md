# Discord Midjourney Wallpaper Slideshow

## installing

> python -m venv venv \
> source venv/bin/activate \
> pip3 install --upgrade pip \
> pip3 install -r requirements.txt

## configuring

Duplicate `.env-template` to `.env` and define

- `ALLOWED_KEYS` Valid http `Authorisation` values for write operations
- `APP_KEY` Flask session key. Random values are fine.
- `IMAGE_ROOT_FOLDER` When image binary data is requested, this is the base path they are served from. Possibly vulnerable to path attacks
- `WEBAPP_ROOT_FOLDER` Base folder for serving static webapp content from (ie your frontend react app)

This is hardly secure, dont run this publicly/out of a sandboxed environment

## running

> python app.py

## Running whole stack

Have a look at the `docker-compose.yml` file to start the server, redis and the scraper all at once.
Note you will need to have a build directory present for the web components
