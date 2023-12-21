These are the initial requisites I extracted from the assignment.

**PRE-REQUISITES**
------------------

* ✅ Can we manually read/write data?
* ✅ Initial proof of concept with swagger/CURL

**ENDPOINTS**
------------------------
* ✅ Write data (mock) → final
* ✅ Read data (mock) → final
* ✅ Create user final
* ✅ Login final

**TESTS**
------------------------
Initially, mock the data. Once the DB models are in place, re-implement.

* ✅ Determine the necessary unit tests
  * ✅ Is data written correctly?
  * ✅ Is data read correctly?
  * ✅ Ensure a user can only read ECGs created by them.
* ✅ Extra edge cases.

**DATABASE**
------------------------

* ✅ Create the database with a Docker image (to reproduce)
* ✅ Create the data model reproducibly → alchemysql.
* ✅ Create a PostgreSQL database with the provided structure.
* ✅ Adapt the endpoints (unmock)
* ✅ Migration system

**USER SYSTEM**
-------------------------

* ✅ Add an API TOKEN system (oauth2)
* ✅ Create a user role that can use the API.
     At server startup (admin).
* ✅ Endpoint to create users (admin).
* ✅ Endpoint to login users.
* ✅ Create a user with admin role at startup.
* ✅ Create a normal user at startup.

**CONSIDERATIONS**
------------------

* ✅ Using TDD could be very desirable in this case.
* ✅ Ensure we are counting the electro points. → We leave te responsability to
     the frontend, as the field is optional.
