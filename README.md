# Theme Time Radio

Podcast website for "Theme Time Radio Hour" with Bob Dylan.

[https://theme-time-radio.herokuapp.com/](https://theme-time-radio.herokuapp.com/)



## Objective

Create a Podcast website for the "Theme Time Radio Hour". The site will also act as a music library so users can navigate between episodes, artists and genres.



## Features

* Stream Podcast episodes
* Play 30 seconds preview of episode songs
* Stream episode songs with Spotify player
* Discover artists biography
* Discover artists genres



## Technologies Used

### Back-End

#### Web Server

Using Python Flask I have implemented:

*  Web server that serves `jinja` templated
* API endpoint using `flask_restful` that would server data from my database in `JSON` format.

#### Database

Used Python `sqlalchemy` to create a model for storing information I am going to collect.

**Models**

- Episodes
- Tracks
- Genres
- Songs
- Artists

#### Web Scrapping

Using Python `BeautifulSoup` package, I created scripts that scrapped the following websites to get information about the episodes. The information is then stored in the database.

**[Wikipedia.org]( https://en.wikipedia.org/wiki/Theme_Time_Radio_Hour)**

* Number
* Season
* Title
* Aired date
* Tracklist

**[ThemeTimeRadioHour.com](http://www.themetimeradio.com)**

* Poster image
* Description
* Audio url

#### Music Tagger

Using Python `requests` package I created a script that queries [Spotify](https://developer.spotify.com/web-api/) and [LastFM](http://www.last.fm/api) APIs. The purpose of the script is to gather information about the "raw" scrapped tracks.

The information is then stored in the database and referenced to each track.



### Front-End

#### Styling

Implemented using `Sass` in a mobile first responsive design.

#### JavaScript

* Used `Handlebars.js` to render repetitive components. Mostly used for rendering response data from APIs.
* Used `jQuery` to communicate with my API and LastFM API.
* Used `Underscore.js` module for different data manipulation techniques.
* Created custom HTML5 `<audio>` tag controls for episode player.

