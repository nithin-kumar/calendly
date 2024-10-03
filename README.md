 Calendly is a toy application to mimic the calendly.com website. It is a simple application that allows users to create events and share their event links with others. The others can then book the event by selecting a time slot.
 
The Functional Requirements of the application are as follows:
 1. User can register and login to the application.
 2. User can link their Google Calendar to the application.
 3. User can create different types of events like On-on-One, One-off Meeting etc.
 4. User can specify the duration of the event as selected slots or ranges
 5. User can share the event link with others
 6. Others can book the event by selecting a time slot
 7. User can Create Recurring events



TODO items for the application:

 1. Add the ability to link different Calendar to the application
 2. Send .ics file on successful booking of the event
 3. Authorization of the application
 4. Testcases are not included, as this is an MVP version of the application
 5. Application code is not commented properly, need to add comments to the code
 6. Scalability/Modularity of the application is not prioritized, need to refactor the code to make it more scalable


How to Run the Application
1. Clone the repository
2. Get the client_secrents.json from the app creator and place it in the root directory
3. Run the following command to start the application
```docker compose up --build```
4. The application will be running on http://localhost:8000
5. Run ngrok to expose the application to the internet
6. ```ngrok http http://localhost:8000```
7. Configure the ngrok public url in Google Cloud console

**Application Flow**
1. Sign Up
```commandline
curl --location 'http://127.0.0.1:8000/api/user/signup/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "nit",
  "password": "12xq!12334dff",
  "password2": "12xq!12334dff",
  "email": "newuser@example.com",
  "first_name": "Nithin",
  "last_name": "KV"
}'
```
Response
```commandline
{
    "username": "nisk2010@gmail.com",
    "email": "nisk2010@gmail.com",
    "first_name": "Nithin",
    "last_name": "KV"
}
```
2. Login
```commandline
curl --location 'http://127.0.0.1:8000/api/user/signin/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "nisk2010@gmail.com",
  "password": "12xq!12334dff"
}'
```
Response
```commandline
{
    "username": "nisk2010@gmail.com",
    "password": "12xq!12334dff",
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzI3OTY5MjY5LCJpYXQiOjE3Mjc5Njg5NjksImp0aSI6Ijk2ZDg1ZTEzNTNjZjRiNWZiNDQwYzQ5OTQwMzUxNTkyIiwidXNlcl9pZCI6MX0.2oQqc2dvud1hQaA7pjzexhK68cWMoEV7-A_lYbPM6rM"
}
```

3. Link Google Calendar
```commandline
curl --location 'http://127.0.0.1:8000/api/google-calendar/init/' \
--header 'Authorization: Bearer '<Token from signin>' \
```
Response
```commandline
 302 Redirect to Consent Screen
```

4. Create One-On-One Event - Between 2 dates
```commandline
curl --location 'http://127.0.0.1:8000/api/events/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <Token>' \
--data '{
    "name": "Resume Review",
    "event_type": "OO",
    "event_occurrence_type": "BD",
    "start_date": "2024-10-11",
    "end_date": "2024-10-12",
    "duration": 60
}'
```
Response
```commandline
{
    "event": {
        "id": "8dOFciR6icT",
        "name": "Resume Review",
        "event_type": "OO",
        "start_date": "2024-10-11",
        "end_date": "2024-10-12",
        "duration": 60,
        "event_occurrence_type": "BD",
        "event_dates": null,
        "recurring_event_time": null,
        "description": "This is a first Resume Reciew",
        "location": null,
        "created_at": "2024-10-03T15:59:53.344164Z",
        "updated_at": "2024-10-03T15:59:53.344206Z"
    },
    "url": "127.0.0.1:8000/api/events/8dOFciR6icT/"
}
``` 
5. Create One-On-One Event - Provide list of dates
```commandline
curl --location 'http://127.0.0.1:8000/api/events/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <Token>' \
--data '{
    "name": "System Design Discussion",
    "event_type": "OO",
    "event_occurrence_type": "LD",
    "duration": 30,
    "event_dates": ["2024-10-11", "2024-10-12"]
}'
```
Response
```commandline
{
    "event": {
        "id": "8dOFfXYlB2G",
        "name": "System Design Discussion",
        "event_type": "OO",
        "start_date": null,
        "end_date": null,
        "duration": 30,
        "event_occurrence_type": "LD",
        "event_dates": [
            "2024-10-11",
            "2024-10-12"
        ],
        "recurring_event_time": null,
        "description": null,
        "location": null,
        "created_at": "2024-10-03T16:00:31.595015Z",
        "updated_at": "2024-10-03T16:00:31.595053Z"
    },
    "url": "127.0.0.1:8000/api/events/8dOFfXYlB2G/"
}
```
6. Create One-off  Event - Provide slots for the event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <Token>' \
--data '{
    "name": "Resume Review 4",
    "event_type": "OF",
    "event_occurrence_type": "BD",
    "duration": 30,
    "event_dates": [{"date": "2024-10-12", "time_keys": ["2024-10-12T00:00:00_2024-10-12T00:30:00", "2024-10-12T00:30:00_2024-10-12T01:00:00"]}]

}'
```
Response
```commandline
{
    "event": {
        "id": "8dOFmKHyjL6",
        "name": "Resume Review 4",
        "event_type": "OF",
        "start_date": null,
        "end_date": null,
        "duration": 30,
        "event_occurrence_type": "BD",
        "event_dates": [
            {
                "date": "2024-10-12",
                "time_keys": [
                    "2024-10-12T00:00:00_2024-10-12T00:30:00",
                    "2024-10-12T00:30:00_2024-10-12T01:00:00"
                ]
            }
        ],
        "recurring_event_time": null,
        "description": null,
        "location": null,
        "created_at": "2024-10-03T16:02:03.491581Z",
        "updated_at": "2024-10-03T16:02:03.491631Z"
    },
    "url": "127.0.0.1:8000/api/events/8dOFmKHyjL6/"
}
```
7. Create Recurring Event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/' \
--header 'Content-Type: application/json' \
--header 'Authorization: Bearer <Token>' \
--data '{
    "name": "Resume Review Recurrinng",
    "event_type": "OO",
    "event_occurrence_type": "RE",
    "duration": 30,
    "event_dates": ["2024-10-11", "2024-10-12"],
    "recurring_event_time": "15:30:00"
}'
```
Response
```commandline
{
    "event": {
        "id": "8dOBuctQdX7",
        "name": "Resume Review Recurrinng",
        "event_type": "OO",
        "start_date": null,
        "end_date": null,
        "duration": 30,
        "event_occurrence_type": "RE",
        "event_dates": [
            "2024-10-11",
            "2024-10-12"
        ],
        "recurring_event_time": "15:30:00",
        "description": null,
        "location": null,
        "created_at": "2024-10-03T15:07:57.419902Z",
        "updated_at": "2024-10-03T15:07:57.419941Z"
    },
    "url": "127.0.0.1:8000/api/events/8dOBuctQdX7/"
}
```
8. View Event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dOBuctQdX7/' \
--header 'Content-Type: application/json' \
```
Response
```commandline
{
    "event": {
        "id": "8dOBuctQdX7",
        "name": "Resume Review Recurrinng",
        "event_type": "OO",
        "start_date": null,
        "end_date": null,
        "duration": 30,
        "event_occurrence_type": "RE",
        "event_dates": [
            "2024-10-11",
            "2024-10-12"
        ],
        "recurring_event_time": "15:30:00",
        "description": null,
        "location": null,
        "created_at": "2024-10-03T15:07:57.419902Z",
        "updated_at": "2024-10-03T15:07:57.419941Z"
    }
}
```
9. Get Calendar of an event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNkdk8JURN/calendar_days' \
```
Response
```commandline
{
    "dates": [
        "2024-10-11",
        "2024-10-12"
    ]
}
```
10. Get Available Slots of an event on a date
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNkdk8JURN/availabilities/2024-10-12/' \
```
Response
```commandline
{
    "availabilities": [
        {
            "start": "2024-10-12T15:30:00+05:30",
            "end": "2024-10-12T16:00:00+05:30",
            "key": "2024-10-12T15:30:00_2024-10-12T16:00:00"
        }
    ]
}
```
11. Book an event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNb2L9X6CP/availabilities/2024-10-11/book/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "start_time": "2024-10-11T22:30:00+05:30",
  "end_time": "2024-10-11T23:00:00+05:30",
  "attendee_email" : "attendee_email"
}'
```
Response 
```commandline
{
    "event": {
        "kind": "calendar#event",
        "etag": "\"3455942903146000\"",
        "id": "u6eisuqkq8nfp7lkt7p4ce26b4",
        "status": "confirmed",
        "htmlLink": "https://www.google.com/calendar/event?eid=dTZlaXN1cWtxOG5mcDdsa3Q3cDRjZTI2YjQgbmlzazIwMTBAbQ",
        "created": "2024-10-03T16:04:11.000Z",
        "updated": "2024-10-03T16:04:11.573Z",
        "summary": "Resume Review Recurrinng",
        "creator": {
            "email": "nisk2010@gmail.com",
            "self": true
        },
        "organizer": {
            "email": "nisk2010@gmail.com",
            "self": true
        },
        "start": {
            "dateTime": "2024-10-12T15:30:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "end": {
            "dateTime": "2024-10-12T16:00:00+05:30",
            "timeZone": "Asia/Kolkata"
        },
        "iCalUID": "u6eisuqkq8nfp7lkt7p4ce26b4@google.com",
        "sequence": 0,
        "attendees": [
            {
                "email": "kv.nithin.90@gmail.com",
                "responseStatus": "accepted"
            }
        ],
        "reminders": {
            "useDefault": false,
            "overrides": [
                {
                    "method": "email",
                    "minutes": 1440
                },
                {
                    "method": "popup",
                    "minutes": 10
                }
            ]
        },
        "eventType": "default"
    }
}
```
