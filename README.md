# ATD
Automated Testing with Docker (ATD).

ATD is a simple tool to run a test suite for a project in a Docker container. Using a config file, the user may specifiy several parameters and ATD will automatically generate a Dockerfile and begin running the provided test files after constructing the appropriate Docker containers.

The user may provide an email address that will be notified if any tests fail.

Currently, ATD supports Git repos and unit tests written with PyUnit. 
