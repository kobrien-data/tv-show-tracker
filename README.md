# TV Show Tracker
An application used to track which season/episode of a TV show you're on to so you don't ever forget which episode was the last one you watched

## The Why
Among recent conversations around streaming services and whether we actually own digital content that we pay for, and the disappointment of going to watch your favourite show only to notice that it is no longer available on any of the services you pay for has some people returning to physical media like DVDs. 

As this is something that I myself have started doing, one problem that I've had is remembering what was the last episode I watched, especially if I've taken a break from watching the show for a while. Streaming provides a digital bookmark, you can put a physical bookmark in a book, but you can't bookmark a DVD. And that's why I wanted to make this application, so that I, and many other DVD users can easily create bookmarks for our shows, and don't have to spend time searching Wikipedia for the episode that sounds the most familiar. 

## The How
### Phase 1
To get to an MVP, I chose to just write basic python code to add and delete TV shows, and save all inputs to a JSON file. 

### Phase 2
From here, I added more functionality by integrating my app with the TMDB API so I could pull data down and use it as extra information when listing a TV show

### Phase 3
In this phase, I connected the app to MongoDB Atlas. While my original JSON file worked, I wanted to use a solution that real world applications would use, and MongoDB is a popular choice.

### Phase 4
Finally, I changed the app to use Flask so I could run it in my web browser and create a UI instead of having it just run in the terminal. 

## Deployment
The app is deployed at: https://tv-show-tracker-6yet.onrender.com/
