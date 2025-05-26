# CWB Tuition Check - Development Tasks

## Authentication & User Management
### Sign Up Implementation
- [ ] Create sign up modal triggered by "signup" link in login.py in components folder
- [ ] Reuse existing functions from database.py design and implement new database table using database credittials in cwb-db.env for university sign ups with fields below in a new table 'enterprise_clients':
  - org_id (unique identifier)
  - enterprise_name
  - first_name
  - lastname_name
  - group_email
  - person_email
  - phone
  - password
   - address_line1
  - address_line2
  - address_line3
  - city
  - postcode
  - country

- [ ] Modify login system to authenticate against new sign up table database
- [ ] The address fields in 'enterprise_clients' will be updated from a form in profile.py as part of verification/ completion after initial signup:



## Home Page (home.py)
### Financial Requirements Management
- [ ] In the card for “Financial Requirements”, on click of the button “Create new”, implement modal for financial requirements with fields:
  - course_name
  - tuition_amount
  - home_office_amount
  - total_finance (derived from: tuition_amount + home_office_amount)
  - session_year
  - Requirement checkpoints:
    - Home office living expense check
    - Tuition check (yes/no)
    - Exchange rate risks (yes/no)
    - Basic balance check (yes/no)
    - Probability of payment default forecast (yes/no)
    - 
- [ ] Reuse existing functions from database.py design and implement new database table for 'financial_requirements' with:
  - org_id (foreign key to user account)
  - unique_id for each requirement
  - All form fields
- [ ] Create a new card in in profile.py like the card for “Account Settings” there, display a DashTable with the requirements table but retrieve only requirements from database table for only logged in user org_id  

### Single Applicant Check
- [ ] - In the card for “Single applicant check”, on click of "Perform check" launch page to collect form for  single applicant with:
  - first_name
  - last_name
  - email
  - Course dropdown (filtered by university account)
  - Country field
  - Generate unique 'applicant_id'
  - Submit button
  The course drop down should be the list of courses from the 'course_name' column in 'financial_requirements' table
  for the logged-in 'org_id'.  
- [ ] On click of submit, do three things 
----- (1.) enter into a database table 'applicant_table' with credentials in cwb-db.env for the following fields					
    - org_id	
    - applicant_id	
    - first_name	
    - last_name	
    - email	
    - country	
    - course
----- (1a.) Redirect to Mono to collect json data, store the data in database

----- (2.) Send the 'applicant_id' and 'required_amount' value (obtain from the 'total_finance' field from 'financial_requirements' table) to the api 'https://us-central1-com-726-project.cloudfunctions.net/run-ml-model' using the json format data = {
    'applicant_id': 912345678,
    'required_amount': 14000
}
----- (3.) Redirect to a completion page with Thank you message, 


Integrate with backend verification system
- [ ] Implement email link generation and sending
- [ ] Set up Mono flow integration
- [ ] On click of submit 
  - Status update notification
- [ ] Implement database storage for Mono JSON data
- [ ] Set up API integration for affordability checks
- [ ] Create new table entry system for applicant results
- [ ] Implement view functionality linking to finhealth.py

## Financial Health Page (finhealth.py)
- [ ] Update data fetching logic to filter by applicant_id
- [ ] Implement dynamic data loading based on selected applicant

## Profile Page (profile.py)
- [ ] Implement basic profile management
- [ ] Add verification status display
- [ ] Create requirements table view
- [ ] Add functionality to complete address fields post-signup

## Support Page (support.py)
- [ ] Update FAQ content (Collaboration: Dami x Abel)

## Database Schema Updates
- [ ] Design and implement sign up table
- [ ] Design and implement requirements table
- [ ] Design and implement applicant results table

## Integration Points
- [ ] Connect signup flow with authentication system
- [ ] Link requirements creation with database
- [ ] Integrate Mono flow with applicant processing
- [ ] Connect Google Cloud Function for affordability checks
- [ ] Set up email notification system

## Testing
- [ ] Test signup flow
- [ ] Test requirements creation and retrieval
- [ ] Test applicant processing pipeline
- [ ] Test financial health data display
- [ ] Test profile management 