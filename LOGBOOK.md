# Log Book

In order to help you better understand the project, I've decided to log my project decisions here.

I'll take the liberty to write things without worrying too much about formatting. :)

- Using Python 3.7: I was using 3.6, but updated to test how things would work async with a TaskPool to reduce memory usage
  - might discuss this in the future, but I think I won't need it
- Using Flake8 linter: This should make things consistent between files, improving readability.
- Using radon (code complexity analizer): Running from time to time... It signals me when I might be doing something too complex.
- Using Peewee ORM: Not sure about the DDL thing. Since I don't want to bang my head against the wall writing SQL queries, ORM it is.
  - As a dependency of Peewee, I had to install psycopg2 (a lower level lib to handle postgresql stuff)
- About the GPS APIs:
  - Tried to use Google Maps API: but is a pay-per-request service (with very low cap when using it for free)
  - Tried to use Nominatim API (uses OpenStreetMap data). Successful, but had a VERY low RPS (requests per second) cap of 1 (yes, 1 RPS).
    - It would take me ~100 sec to do 100 queries. Nope.
  - Using OpenCage API: pay-per-request, as the Google Maps API, but with a limit of 2.5k requests per day.
    - Requests per second (synchronous): around 2.5 rps.
  - Using aiohttp and asyncio to run asynchronouse queries:
    - Requests per second (asynchronous): around 500 rps (tested only once, due to the 2.5k req limit)
    - Clearly, had to raise the limit of open descriptors: `ulimit -n [limit here, using 8192]`
    - Tried to use pypeln, to make things cleaner/faster by using pipelines
      - Bad documentation, does not worth the stress.
- Using connection pooling to improve database performance
- Batching insertion of Location rows in PostgreSQL to improve performance
- Had a lot of trouble debugging why the descriptor limits were not being properly set
  - After fixing, I could test the application with 10k requests
  - 10k requests in 13.3 seconds (about 750 RPS)
- Implemented a modular Parser module (inpired by the Interpreter pattern)
- The whole process of setting everything up was too tiresome. Decided to use Docker Compose to automate things for me.
- Since I had a compose file done and working, decided to integrate CircleCI. This way you can see the tests passing (or not) without having to run them. :)
  - But there's a downside: Since we use docker-compose, we need a VM executor (multiple containers). Because of that, we cannot test locally with the CircleCI-CLI (we have to do it manually, as described in the README file)
- Refactored Hermes to be a Producer/Consumer module:
  - Much better performance
  - Reduces memory usage
    - no need to create all tasks before scheduling them
    - no need to read everything before processing, nor batch data
   - Working on files. Planning on receiving data from user input, so we can pipe data in the future. 
