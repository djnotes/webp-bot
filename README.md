# WebP Factory Bot

## How This Works
The user sends a photo or photo document to the bot and the bot converts it to webP and returns it.
While converting the bot also resizes the photo to <= 480 for height. The width is also resized accordingly to keep 
the aspect ratio


## How to Deploy to Server
This app can be run both containerized and non-containerized. It's recommended, however, to run it using containers. 
All you need to do is go to the project folder and run `docker-compose up`:  

```
git clone https://github.com/djnotes/webp-bot
cd webp-bot
cp env.ini.example env.ini
# Fill in env.ini with correct info
docker-compose up
```