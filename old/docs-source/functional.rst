XAuto Specification
===================

Home page
---------

I. Welcome page

    There should be a simple home page.

    Frontend:

    a) Prepare home page and plug it into the project


Image uploads
-------------

    It is always possible for mobile users to upload photos (always visible upload button). Every uploaded image is
    automatically assigned to an event using: datetime and lat/lon.

    In case there are multiple matches then user is allowed to choose the right one.

    In case there's no match the image is only assigned to the user and shown in his profile.

    Backend:

        a) image upload endpoint (that makes use of Amazon AWS and is smart enough to return list of matching events
           in case it's more than one matching lat/lon and datetime)

    Frontend

        a) make it possible for end-users to take and upload photos
        b) implement selection of the event in case there are multiple events matching lat/lon and datetime


Users management
----------------

From pages accessible for anonymous users there should be a way to sign in and to log in.

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

    In order to use features like creating new events, adding photos, following events or profiles user has to be registered

    Backend:

    a) Create a registration endpoint, allowing registration for anonymous users. Assumption is that all fields from account are to be filled here)
    b) After registration data is received a registration confirmation email should be sent. User should click on a link in this email to activate his account
    c) Create endpoint to check username availability

    Frontend:

    a) Add a registration popup with fields like the ones above and a service that will call backend endpoint in order to register a new user.
    b) It's possible that the data that is going to be stored in the database might be rejected by the server
       (for example username is already taken) so it's possible that the server will return Bad Request response with some error message - this should be handled in the frontend.
    c) plug into the page checking for username availability


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
    * One event is shown only once on the list of events even if it has multiple dates and locations (those are shown
      in the dropdown from the event detail page.
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

    Every authenticated user is allowed to create an event and to manage his own events.

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

2. List of my events

    A user can browse events he created. List shows basic details about the events like image, name, location, number
    of followers, number of images. It's also possible to delete an event or to get into edit event page.

    .. image:: images/events_my_list.png

    Frontend
        a) attach list of my events to rest endpoint (probably the same endpoint as for general list of events might be
           used here


3. List of events

    Everyone is allowed to view, filter and follow events. A lot of details about particular events are shown for each
    event: name, date, price, organizer, number of photos, number of followers (with ability to follow the event),
    image, location, headline, description, information if stream is currently active.

    .. image:: images/event_on_the_list.png

    Backend:

        a) create endpoint that will return list of events; should be able to filter events (text search in event name,
           headline and location; followed; streaming now), order events and to paginate them. That endpoint should also
           be used by the global search box.
        b) create "follow" endpoint

    Frontend:

        a) plug the list endpoint into the events list page
        b) plug the "follow" endpoint into the page

.. _event_details:

4. View event details

    Event data is to be shown to the application users accessing the event page.

    From that page:

    a) mobile users can use "go to" function to open navigation app and check how to get to the event.
    b) users can add photos to the selected event date. This would be used, for example, by a professional photographer
       who is uploading pictures from a non-mobile camera at home, or at time after the expiration of the event.
    c) follow event
    d) view other event dates and locations
    e) view event's image stream. Each image may be marked as favorite (by authenticated users), shared with other people
       or reported as inappropriate. images are grouped by dates
    f) it's possible to share album for specific date and event

    .. image:: images/event_details.png

    Backend:

        a) make sure that the photo management endpoint makes it possible to add photos even if user is not the event's
           owner
        b) add endpoint that will return all data about the event including location and dates (in case it will be
           different than endopoint used in event management).
        c) for the image stream implement some solution that will provide data (might be something AJAX based or
           WebSockets based like SockJS + Tornado)
        d) add endpoint for fav'ing images
        e) add endpoint for flagging images as inappropriate
        f) album / date sharing (**this probably means that there should also be a dedicated page to view shared album?**)

    Frontend:

        a) Use real event data
        b) Add a panel to add photos to selected event date
        c) Add calls to backend to the follow button
        d) Add support for "Go to" button
        e) Make the image stream alive (use some client library like sockjs or socketio)
        f) plug favorite and flag endpoints into the frontend


Profiles
--------

    Profiles is a section where it is possible to browse profiles of registered users, to view their photos and to
    follow them.

1. List of profiles

    Everyone is allowed to view, filter and follow profiles. List shows profiles. Each has the following data shown:
    image, full name, twitter/username (**what is this @LewHamF1 on the profile list?**), location, information about user,
    amount of photos, amount of followers and amount of followed people (**events too?**), link to user webpage.
    It's also possible to follow a user.

    List is filterable and has predefined categories: all, followers, following

    .. image:: images/profile_list.png

    Backend:

        a) create endpoint that will return list of profiles; should be able to filter profiles (text search in user full name,
           about and location), order (there's no ordering of neither events nor profiles in the layout)
           profiles and to paginate them. That endpoint should also be used by the global search box.
        b) create "follow" endpoint for following users

    Frontend:

        a) plug the list endpoint into the events list page
        b) plug the "follow" endpoint into the page

.. _profile_details:

2. User details

    Page shows details of user and his photo-stream. It's allowed to follow a user.
    Except for user details (image, full name, twitter/username (**what is this @LewHamF1 on the profile list?**), location, information about user,
    amount of photos, amount of followers and amount of followed people (**events too?**), link to user webpage) there
    is also a photo stream

    .. image:: images/profile_details.png


    Backend:

        a) endpoint to retrieve single user's details
        b) stream of user photos

    Frontend:

        a) plug the user details endpoint into the page
        b) plug the stream of photos


Streams
-------

   The image streams appear in few places accross the site. Those are:

   * event details (described :ref:`above <event_details>`)
   * user profile details (described :ref:`above <profile_details>`)
   * my photos
   * stream

1. My photos
    A place where user can manage his own photos


    Backend:
        a) endpoint ot list user photos (this is not a stream)
        b) endpoint to delete user photos

    Frontend:
        a) plug the endpoints into the gui

2. Stream
    Real-time images from followed events and profiles

    Backend:

        a) set up endpoint to serve realtime images

    Frontend:

        b) connect to server to get and display images