# Zinc - ANS (Address Naming Service)

![Zinc](https://i.ibb.co/h1MgGqP/Screen-Shot-2022-09-17-at-10-57-48-PM.png)

## Inspiration

Relocation/moving is a messy, frenetic process. When moving from address A to B,  the ultimate task of notifying people and companies of a new address stands in the way of all. For example, [moving.com](https://www.moving.com/tips/change-address-checklist-who-to-notify-when-you-move) lists 19 companies you must inform, which includes the post office, tax agencies and banks. This process is tedious, and if you miss something vital, this could lead to missed bills or other serious consequences.

## What Zinc - ANS (Address Naming Service) does?

**Zinc - ANS (Address Naming Service)** is an application that makes streamlines this process for everyone! Individuals can change their address without having to do this tedious process of informing companies, and companies can easily access people's addresses through a simple API request, and be sure it's correct - as they get notified of any new address!

**Specifically**, through this service, home-owners are given a unique address user ID (AUID), serving as a unique identifier for the individual's address without disclosing his her’s name. Companies/Enterprises/Services, to whom a home-owner has shared his AUID with, may request to get access to the latest, up-to-date address. Why request? All companies must receive a one-time verification by the user to ensure trustworthiness.

## How we built it

Zinc - ANS (Server Side) was built with Django and Django REST Framework, alongside an Android Flutter Application integrated with Firebase Cloud Messaging. A Flask server was also used to mimic an enterprises's, who's servers will be actively listening for a webhook from ANS upon address change.

## Challenges we ran into

1. Firebase Cloud Messaging: Push-notification pop-ups not working, emulator not connecting to firebase, notifications coming after a unusual period of time 
2. Django REST Framework: Utilizing token authentication in a simple way to do user authentication (in this case the enterprise)
3. Android Studio Emulator: emulator was crashing, with the UI not loading in the right way and not establishing a connection to firebase

## What's next for Zinc - ANS (Address Naming Service)

Of course, there are many additions that could be made for Zinc - ANS. Address verification using an API like positionstack would be able to make sure their address actually exists, and the mobile application could be extended to have the same functionality as the website. Additionally, more information could be provided to both parties: Users could know when companies are checking their address, and Companies could better manage their Users through tables.

## Final Notes

This project was created for Hack the North 2022.
