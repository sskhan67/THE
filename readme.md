

Use Postman to call the api: NO UI available  
1. Create Admin 
localhost:5000/create-admin
 By default admin is test (created already). Please use the following parameters to 
 set Postman headers: 
            email: test@test.com
            password: password 
            content-type: application/json 
    Body: 
   {
    "email" : "test_admin@test.com",
    "name" : "test_admin",
    "password" : "password"
  }
   it will create user test_admin and set role to admin using step 3 


2. To add user 
POST: localhost:5000/signup
{
    "email" : "test_2@test.com",
    "name" : "test_2",
    "password" : "password"
}

3. To add role admin/user 
4. 
POST: localhost:5000/create-role
{
    "email" : "test@test.com",
    "role" : "admin"
}

5. To delete role 
localhost:5000/delete-role
{
    "email" : "test@test2.com",
    "role" : "admin"
}

6. Create company permission

localhost:5000/create-permissions
{
    "email" : "test@test2.com",
    "permission" : "company_list"
}

8. Delete Permission

localhost:5000/delete-permissions
{
    "email" : "test@test2.com",
    "permission" : "admin"
}

9. To get  control panel
HTTP method : GET 
localhost:5000/control_panel
{
    "email" : "test@test.com",
    "password" : "password"
}

10. Create Company 
HTTP method : POST 
localhost:5000/create-company
{
    "name" : "company 3"
}

11. Add company user 
HTTP method : POST 
localhost:5000/add-company-user
{
    "company_name" : "company 2",
    "email" : "test@test.com"
}

12. Get user company 
HTTP method : GET 

localhost:5000/get-user-company
{
    "email" : "test@test.com"
}

13. Get company 
HTTP method : GET
localhost:5000/get-company-users
{
    "name" : "company 1"
}