# Gyanova
This project focuses on application of python flask for creation of the website

## Outcome of the project
  - a user can sign-up as a student or a teacher
  - the teacher can upload notes in form of pdf/docs
  - the teacher can also upload youtube links for reference
  - the student can view and download notes and can filter by subject, chapter, teacher or school

## Tools Used
  - Python Flask
  - Flask sql_alchemy
  - Jinga (templating Language, which allow us to write some python logic inside of html)
  - Front_end Language (HTML, CSS styles, JS bootstraps)

## Structure of the project
```bash
  .
  |- website/
  |  |-resumes
  |  ⨽templates/
  |    |-base.html
  |    ⨽home.html
  |    ⨽login.html
  |    ⨽preview.html
  |    ⨽sign_up.html
  |    ⨽student_dashboard.html
  |    ⨽teacher_dashboard.html
  |    ⨽upload.html
  |  |-__init__.py
  |  ⨽auth.py
  |  ⨽models.py
  |  ⨽views.py
  |-main.py

```
## Running the app
```bash
  python main.py
```
## Note
  - Please create an empty folder name 'uploads' inside website folder, which would store all notes

## Expected Outcome in the Future
* The teacher will be able to upload notes based oon different class
* The teacher will also have a option to share notes privately to individual students

## Find a bug?
If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above.
If you found an issue or would like to submit an improvement to this project, please submit an issue using the issues tab above.

