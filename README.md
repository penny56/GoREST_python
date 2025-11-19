GoREST is a free, publicly available REST API service designed for testing.

Use the 'Access Token' as the Authorization method.  

- Use Python for RESTful API testing (non-GUI)
  - include user, post, comment, todo test suites, each test suite has several test cases.
  - the test_parallel() test case in test_scenarios.py module use concurrent.futures module to verify the create_user operation runs in parrallel.
  - Use GitHub actions to run as the daily auto test inside the ci/cd process on GitHub-hosted runner.

-- use JMeter for 

Created an Amazon EC2 Instance as a self-hosted runner in repo settings.

And an action flow to run the JMeter test hourly to perform the loading test on the runner.
