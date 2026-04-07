# Applied-Job-tracker
A lightweight Python project that uses the Gmail API to track job applications and rejections, built to turn rejection into a measurable and actionable tracker.

## Learning Goals 
This project focuses on: 
* API integration  
* state management without overengineering
* Incremental system design and building projects iteratively

## Motivation
The overall goal here is to reframe rejections as a progress towards actionable goals. 

For example, each rejection milestone triggers a specific action: 
* 5 rejections → Additional Applications.  
* 10 rejections → Network and reach out further  
* 15+ → Additional tasks  
* 20 rejections → A new challenging project

## Features
* 📧 Gmail API integration using custom labels
* 📊 Sprint-based tracking (time-windowed email counts)
* 🎯 Milestone system with real-world actions
* 🔁 Cycle-based progress with overflow handling
* 🧩 JSON-based state (simple, transparent, no database)

## Design Decisions and Discissions 

#### Emails are grouped into time-based windows (sprints):

To avoid Duplicates and complex state managements such as timestamping and ids. Additionally, personally it also made sense as I prefer working in a 2-week sprint-based windows. Hence it became convenient to track progress over this period. 

#### There is also separation of Lifetime vs Current Progress:

This is done so to distinguish between historical data and current progress towards milestones. This is accounted for future features that I may decide to add to track historical data. Overall, this also prevented recalculating old milestones and duplicate triggers. And enabling overflow emails to be carried over across different cycles of milestones. 

#### Minimal State design:

At this current stage this project intentionally avoids databases and storing email metadata (IDs, timestamps). Instead, it uses a simple JSON file for persistence and recomputation + incremental updates.

## Usage
call: <code>python applied_tracker.py</code>

Example output: 

>Current Total Rejections: 18
>
>New Milestone achieved! 20
>
>Cycle Completed! Carrying over: 2 rejections

## Future Improvements 

* Simple frontend dashboard (cards + progress bar)  

* Visualisation of sprint trends  

* Improved date handling for sprint boundaries 

* AI Agents

## Tech Stack 

* Python  
* Gmail API  
* JSON (state management) 
