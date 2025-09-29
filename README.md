# Multi-threaded Python Chat Platform
## Overview

This project is a high-performance, multi-user chat application built on a Client-Server architecture using standard TCP/IP socket programming in Python.
The system supports real-time communication, private messaging, user-defined chat rooms, and a reliable peer-to-server file transfer utility with data integrity checks.
The core strength of the platform lies in its multi-threaded server design, enabling simultaneous, non-blocking communication for numerous concurrent users.

## 🚀 Key Features and Technical Highlights
### Server Architecture (server.py)

  Multi-threaded Concurrency: Implements a multi-threaded server architecture where each new client connection is delegated to its own independent thread (chat_session). This ensures high throughput and responsiveness by preventing any single client session from blocking others.
  
  Modular Protocol Design: The server handles a custom application-level protocol that parses incoming data for specific commands (e.g., -pr, -goto, -file).
  
  State Management: Manages and persists in-memory state for user sessions (CHAT_CLIENTS), current chat room membership (CHAT_ROOMS), and client-server communication.

  Chat Room Logic: Dynamically manages client presence across pre-defined chat channels, enabling focused communication and targeted message broadcasting.

  Reliable File Reception: Implements robust file transfer logic (get_file) that receives file size metadata first, ensuring data integrity during chunked transfer and reliable storage of files in a designated server directory.

### Client Implementation (client.py)

  Asynchronous Communication: Employs two separate threads for the client: one dedicated to receiving incoming messages/broadcasts (receive_broadcast) and one dedicated to handling user input (chat_input). This ensures the client can continuously receive messages while the user is typing or executing commands.

  Custom Command Handling: Supports a rich set of user commands for:

  Private messaging (-pr [username] [message])

  Joining specific chat rooms (-goto [room name])

  Initiating a file upload to the server (-file [path])

  Local Session Management: Features simple user login and registration by persisting usernames to a local users.txt file
  
## 📝 Usage Commands

Once connected, the client supports the following commands:


```[message]``` Broadcasts the message to all users in your current chat room.

```-pr [username] [message]```  Sends a private message to a specific user.
Example: ```-pr Bob Hey, check this out!```

```-goto [room]``` Switches your chat session to a different room (e.g., room1, room2, room3).
Example: ```-goto room2```

```-file [path]``` Initiates a file transfer of the file at [path] to the server.
Example: ```-file C:\docs\report.pdf```

```bye``` Closes the client connection gracefully.
