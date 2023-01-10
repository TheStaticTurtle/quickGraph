# quickGraph

quickGraph is a dead simple API to get the opengraph meta tags of a website

## API

You execute a query at `/parse` if the parameter `url` to get the parsed data.

For example a request to `/parse?url=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DytWz0qVvBZ0` will result in:
```json
{
    "url": ["https", "www.youtube.com", "/watch", "", "v=ytWz0qVvBZ0", "" ],
    "opengraph": {
        "og:site_name": "YouTube",
        "og:title": "♪ Diggy Diggy Hole",
        "og:type": "video.other",
        "og:image": "https://i.ytimg.com/vi/ytWz0qVvBZ0/maxresdefault.jpg",
        "og:url": "https://www.youtube.com/watch?v=ytWz0qVvBZ0",
        "og:image:width": "1280",
        "og:image:height": "720"
    }
}
```

## Security

This project is not meant to be public facing, with that in mind very little has been done currently, these checks are in place:
 - Is an url
 - Scheme is http or https
 - Url doesn't start with localhost
 - Url is not an IP

