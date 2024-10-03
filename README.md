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