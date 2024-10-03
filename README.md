 Calendly is a toy application to mimic the calendly.com website. It is a simple application that allows users to create events and share their event links with others. The others can then book the event by selecting a time slot.
 
The Functional Requirements of the application are as follows:
 1. User can register and login to the application.
 2. User can link their Google Calendar to the application.
 3. User can create different types of events like On-on-One, One-off Meeting etc.
 4. User can specify the duration of the event as selected slots or ranges
 5. User can share the event link with others
 6. Others can book the event by selecting a time slot
 7. Use can Create Recurring events with other users



TODO items for the application:

 1. Add the ability to link different Calendar to the application
 2. Send .ics file on successful booking of the event
 3. Handling race condition of booking an event, adding to a distributed lock
 4. Authorization of the application
 5. Testcases are not included, as this is an MVP version of the application
 6. Application code is not commented properly, need to add comments to the code
 7. Scalability/Modularity of the application is not prioritized, need to refactor the code to make it more scalable


How to Run the Application
1. Clone the repository
2. Get the client_secrents.json from the app creator and place it in the root directory
3. Run the following command to start the application
```docker compose up --build```
4. The application will be running on http://localhost:8000
5. Run ngrok to expose the application to the internet
6. ```ngrok http http://localhost:8000```
7. Configure the ngrok public url in Google Cloud console

Application Flow
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
2. Login
```commandline
curl --location 'http://127.0.0.1:8000/api/user/signin/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "username": "nisk2010@gmail.com",
  "password": "12xq!12334dff"
}'
```
3. Link Google Calendar
```commandline
curl --location 'http://127.0.0.1:8000/api/google-calendar/init/' \
--header 'Authorization: Bearer '<Token from signin>' \
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
7. View Event
```commandline
curl --location --request GET 'http://127.0.0.1:8000/api/events/8dNkdk8JURN/' \
--header 'Content-Type: application/json' \
--data '{
  "name": "Sample Event",
  "start_date": "2023-10-01T10:00:00Z",
  "end_date": "2023-10-01T12:00:00Z"
}'
```
8 Get Calendar of an event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNkdk8JURN/calendar_days' \
```
8. Get Available Slots of an event on a date
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNkdk8JURN/availabilities/2024-10-12/' \
```
9. Book an event
```commandline
curl --location 'http://127.0.0.1:8000/api/events/8dNb2L9X6CP/availabilities/2024-10-11/book/' \
--header 'Content-Type: application/json' \
--data-raw '{
  "start_time": "2024-10-11T22:30:00+05:30",
  "end_time": "2024-10-11T23:00:00+05:30",
  "attendee_email" : "attendee_email"
}'
```
