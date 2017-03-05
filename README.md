# Grad Mobile Server

## Routes

All routes based off `andrewsosa.com`.

### `/api`
Test route, returns `Hello world!`

### `/api/words`
POST only, accepts two params via form-data

1. `text`: Transcript to parse for keywords.
2. `keywords`: String list of keywords to parse data
    for, comma separated.
    
    > e.g. `"uhm, uh, ah"`

### `/api/sensor`
POST and GET, accepts unlimited number of fields and
values of form data. This route copies the entire form-data
dictionary into temporary in-memory storage, which resets
when the app restarts.

If you POST with `form-data` of `bpm: 85` and `bodytemp:93`, those are the values you will get encoded
as a json reponse on GET.
