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
- [ ] In the card for “Financial Requirements”, on click of the button “Create new”, implement a modal for financial requirements with fields:
  - course_name
  - tuition_amount
  - home_office_amount
  - total_finance (derived from: tuition_amount + home_office_amount)
  - session_year
  - Requirement checkpoints:
    - Home office living expense check (yes/no)
    - Tuition check (yes/no)
    - Exchange rate risks (yes/no)
    - Basic balance check (yes/no)
    - Probability of payment default forecast (yes/no)
    - 
- [ ] Reuse existing functions from database.py design where possible and implement new database table for 'financial_requirements' with:
  - org_id (foreign key to user account)
  - unique_id for each requirement
  - All form fields
- [ ] Implement a callback to get form dataa insert data into table
 

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
----- (1a.) [ignore temporarily]Redirect to Mono to collect json data, store the data in database

----- (2.) Send the 'applicant_id' and 'required_amount' value (obtain from the 'total_finance' field from 'financial_requirements' table) to the api 'https://us-central1-com-726-project.cloudfunctions.net/run-ml-model' using the json format data = {
    'applicant_id': 912345678,
    'required_amount': 14000
}
----- (3.) Redirect to a completion page with Thank you message, 

- [ ] In the card for “Batch applicant check" in home.py, on click of the button "Batch check”, implement a modal with a form with fields for:
- start date
- end date
- upload button
- start button
The form should have instructions saying "Please upload the excel file with name, course, email, country, application_date, for applicants for whom you want to conduct checks. Once you click on “start check”, an email will be sent to the applicants with an ink to commence their checks." 

Note: Upload button should accept only .csv file with the following columns (name, course, email, country, application_date). On click of "start button" in the form, insert file content into a database table 'applicant_table' using existing or new functions in database.py. The table should have (applicant_id, name, course, email, country, application_date, start_date, end_date, check_status). The start_date and end_date should be obtained from These table fields should never be empty (applicant_id, name, course, email, country). applicant_id should be unique 9 digit starting with 'ap086xxxxx' where first entry should be given 'ap08600001' next 'ap08600002' etc

...note this should trigger an email to be sent (call an api from Biyi?)


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
- [ ] Create a new card in in profile.py like the card for “Account Settings” there, display a DashTable with the requirements table but retrieve only requirements from database table for only logged in user org_id 

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