# Tanu

*Connecting UMD Students with one fresh fade, perfect lash set, and flawless manicure at a time.*

---

## What is Tanu?

Tanu is an **in-progress, university-exclusive marketplace** that lets UMD students who run **cosmetic businesses** (hair stylists, barbers, makeup artists, nail techs, lash artists, etc.) showcase their work and manage appointments—all while helping fellow students quickly find the beauty services they need right on campus.

---

## Why we’re building it&nbsp;💡

- **Spotlight student entrepreneurs** – Give campus creatives a professional-looking storefront without the overhead of Instagram DMs or endless group-chat promos.  
- **Keep dollars on campus** – Make it dead-simple for Terps to support Terps instead of traveling off-campus or paying salon premiums.  
- **Streamline scheduling** – Replace scattered text threads with a clean booking flow and automatically track upcoming & past appointments for both clients and businesses.  

---

## Core features (roadmap)

| Status | Feature | Description |
|--------|---------|-------------|
| ✅ | **UMD-only sign-up** | Users authenticate with their `@terpmail.umd.edu` address via Google OAuth. |
| 🚧 | **Business profiles** | Upload service menu, pricing, and **photo galleries stored on AWS S3**. |
| 🚧 | **Appointment booking** | Students select a service, pick an available slot, and receive email confirmations. |
| 🔜 | **Appointment history** | See upcoming/past bookings from both the client and business dashboards. |
| 🔜 | **Ratings & reviews** | Optional feedback loop to highlight top campus talent. |

---

## Under the hood 🛠

| Layer | Tech |
|-------|------|
| **Backend API** | Python · Flask |
| **Frontend** | Vanilla JS (ES6), HTML5, CSS3 |
| **Database & Auth** | **Supabase** (Postgres + GoTrue) |
| **Image storage** | **AWS S3** buckets for service photos |
| **Containerisation** | Docker & Docker Compose |
| **Process** | Agile sprints |

---

## Project status

The repo currently hosts:


> **Next sprint goals**  
> 1. Finish business profile CRUD (image uploads → S3).  
> 2. Ship MVP appointment scheduler with calendar view.  
> 3. Polish UI for mobile first.  

---

## Creators

- **Tamunoopubo Taribi** — CS @ UMD
- **Joshua Berhanu** — CS @ UMD
