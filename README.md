# Virtual Theater Chrome Extension

## Overview

Virtual Theater is a Chrome extension that transforms your online video watching experience by enabling real-time watch parties across popular streaming platforms like YouTube and Netflix. With Virtual Theater, you can join or host watch parties, allowing you and your friends to watch videos together, regardless of the physical distance between you. The project leverages Django for the backend, Channels for real-time communication, and a React-based frontend for a seamless user experience.

## Features

- **Create or Join Watch Parties**: Easily start a new watch party or join an existing one with a unique party ID.
- **Real-Time Chat**: Engage with your friends through a real-time chat feature, enhancing the group watching experience.
- **Seamless Integration**: Works directly within YouTube and Netflix web pages without the need for an external website or service.
- **User Management**: Handles user sessions and party memberships efficiently, ensuring a smooth and synchronized viewing experience.

## Technologies Used

- **Backend**: Django, Django Channels for WebSocket communication.
- **Frontend**: React.js for a dynamic and responsive UI.
- **Database**: Uses Django's default SQLite for development with easy scalability options.
