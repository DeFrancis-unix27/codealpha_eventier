
# Eventier - Event Management API

Eventier is an event registration and management platform built with **Django REST Framework**. It enables event organizers to create, publish, and manage events while allowing attendees to register with or without an account using customizable registration forms.

---

## 🚀 Features

### 👤 For Organizers

- Create and manage events
- Upload custom event banners
- Manage event lifecycle:
  - Draft
  - Published
  - Completed
  - Cancelled
  - Postponed
- Create custom registration forms for every event
- View organizer dashboard with:
  - Total events
  - Published events
  - Draft events
  - Total attendees
  - Upcoming event
  - Recent events
  - Recent attendees

---

### 🎟️ For Attendees

- Register for events with an account
- Register as a guest (no account required)
- Submit answers to organizer-defined custom questions
- Logged-in users have registrations linked to their account

---

### 🌍 Public Features

- Browse published events
- Search available events
- View event details
- Register directly from public listings

---

## ✨ Key Features

- Event lifecycle management
- Custom registration forms per event
- Guest attendee support
- Registered attendee support
- JWT Authentication
- Refresh Token Authentication
- Public event search
- Organizer dashboard
- Event banner uploads
- RESTful API architecture

---

## 🛠️ Tech Stack

- Python
- Django
- Django REST Framework
- Simple JWT
- SQLite (Development)
- Pillow (Image Uploads)

---

## 🔐 Authentication

Authentication is powered by **JWT (JSON Web Tokens)**.

Users can:

- Register
- Login
- Refresh tokens
- Access protected endpoints securely

---

## 📂 Core Modules

- Authentication
- Events
- Attendees
- Custom Questions
- Custom Answers
- Organizer Dashboard
- Public Dashboard

---

## 📈 Event Workflow

```text
Create Event
      │
      ▼
Draft
      │
Publish
      │
      ▼
Public Registration
      │
      ▼
Attendees Register
      │
      ▼
Organizer Views Dashboard
      │
      ▼
Complete / Cancel / Postpone
```

---

## 📡 API Highlights

- Authentication APIs
- Event CRUD APIs
- Attendee Registration APIs
- Custom Question APIs
- Custom Answer APIs
- Public Event APIs
- Organizer Dashboard APIs

---

## 🎯 Project Goal

Eventier was designed as an API-first event management system that can power:

- Web Applications
- Mobile Applications
- React Frontends
- Flutter Applications
- Third-party integrations

---

## 🔮 Future Improvements

- Email notifications
- QR code tickets
- Payment integration
- Event analytics
- Favorites
- Reviews and ratings
- Calendar integration

---

## 👨‍💻 Author

**DeFrancis Unix**

GitHub: https://github.com/DeFrancis-unix27

---

## 📄 License

This project is open-source and available under the MIT License.