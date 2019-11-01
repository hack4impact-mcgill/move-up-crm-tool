# Move Up - CRM Tool

This project will help [Move Up](http://www.moveuptoday.org/) manage their clients more easily, and allow them to keep client information in one central location. The CRM tool will allow Move Up mentors to create a profile, keep track of their client notes, and send emails to clients.  

## Development Team

**Project Manager:** Idil Ates

**Developers:** Aidan Sullivan, Alex Asfar, Antonia Nistor, Celine Huang, Curtis Lin, Gwynette Labitoria, Hope Kelly, Michael Buchar, Michel Majdalani, Ted Spare

## Setup and Installation

To get the backend set up, follow the instructions in the `README` in the `backend` folder.

Running the backend requires having some environment variables defined. To do this, create a file called `.env` at the root of the `backend` folder, and define variables in the following format:

```
EXAMPLE_VAR=example_value
SECRET_VAR=supersecretpassword
```

You will need to define values for `FLASK_CONFIG` (can be either `development`, `testing` or `production`), `API_KEY` (API key for Airtable base) and `AIRTABLE_ID` (ID for Airtable base). Once this file is created with proper values, the app will automatically load them into the environment when run. 
