XAuto Specification
===================

Home page
---------

I. Welcome page

    There should be a simple home page.

    Backend:

    a) ---

    Frontend:

    a) Prepare home page and plug it into the project


Users management
----------------

From the home page there should be a way to sign in and to log in.

User account has the following fields:

    * display name (required)
    * username (required)
    * email (required)
    * password (required)
    * about
    * location (required)
    * user thumbnail image
    * user hero image

1. Registration

    In order to use the app user has to be registered

    Backend:

    a) Create a registration end point, allowing registration for anonymous users. Assumption is that all fields from account are to be filled here)
    b) After registration data is received a registration confirmation email should be sent. User should click on a link in this email to activate his account

    Frontend:

    a) Add a registration popup with fields like the ones above and a service that will call backend endpoint in order to register a new user.
    b) It's possible that the data that is going to be stored in the database might be rejected by the server (for example username is already taken) so it's possible that the server will return Bad Request response with some error message - this should be handled in the frontend.


2. Log in

    In order to use the app user has to be logged in

    Backend:

    a) Create authentication end-point that will log a user in and return user's details to the browser, so that it will be able to use it to show user details (like photo and name in the top right corner)

    Frontend:

    a) Build login popup, plug the endpoint into it and also somehow force authentication on the pages that should be protected (check if user is logged in). Probably in router's resolvers.

3. Log out

    Backend:

    a) Create log out endpoint

    Frontend:

    a) Plug the endpoint into the logout function in the frontend

4. Account management

    Users should be allowed to manage their accounts so there's a page dedicated for this task

    Backend:

    a) Create endopoint (this and other endpoints will require authenticated user) to save and to receive account data

    Frontend:

    a) Plug the account management endpoint into the account page


Events
------

Events are the key component in the system.

Facts about events:

    * Everyone can add events. Everyone can follow events.
    * Event creator can manage (edit/delete) his events.
    * One event may be shown multiple times on the events list in case it has multiple dates and locations (**?**)
    * One event is shown only once on the list of events even if it has multiple dates and locations (**?**)
    * Each event has the following attributes:

        * Event Title
        * About Event
        * Short link (event ulr in xau.to)
        * Event Image
        * Event Size (how many cars)
        * Dates and locations

           * Location name (optional)
           * Geolocated address (lat/lon)
           * Address 1
           * Address 2
           * City
           * State
           * Zip/Postal Code
           * Country
           * Date
           * Start time
           * End time
           * Attendance cost
             * Free or Price range (low, high) and currency
           * Exhibition cost
             * Free or Price range (low, high) and currency

    * It must be possible to somehow determine if a stream is happening now. Might be enough to check the current
      date and time in the frontend.

1. Create / edit /delete event

    Everyone is allowed to create an event.

    Backend:

        a) add endpoint to manage event details
        b) add endpoint to manage event locations and dates
        c) add endpoint to manage event photos
        d) add endpoint to delete events

    Frontend:

        a) add page to gather event details
        b) add page to gather event locations and dates
        c) prepare popup to select event photos
        d) on edit page add photo management panel
        e) plug into the edit page the delete endpoint

2. List events

    Everyone is allowed to view, filter and follow events.

    Backend:

        a) create endpoint that will return list of events; should be able to filter events (text search in event name, headline and location; followed; streaming now), order events and to paginate them.
        b) create "follow" endpoint

    Frontend:

        a) plug the list endpoint into the events list page
        b) plug the "follow" endpoint into the page

3. View event detail

    Event data is to be shown to the app users accessing the event page.

    **What exactly is "go to"?**

    Backend:

        a) make sure that the photo management endpoint makes it possible to add photos even if user is not the event's owener
        b) add endpoint that will return all data about the event including location and dates (in case it will be different
           than endopoint used in event management).

    Frontend:

        a) Add a panel to add photos to selected event date