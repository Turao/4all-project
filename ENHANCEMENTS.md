# Improvements

Here we log things that could be better.

I could do this by opening enhancement issues, but you probably would not look there...

- How complex are our queries/joins?
  - NOSQL could be sharded and distributed. 
  - And we would not have problems when modifying our data structures.
    - Easier integration with multiple APIs

- It seems to me that we still don't have a good support for async operations in Python
  - Other programming languages are much better suited to the task and could improve our productivity
  - i.e. Functional languanges, or others with better support to concurrency such as Go

- I've mentioned in the log book, but I'm consuming data from text files. I think it would be a great idea to implement ingestion based on input, so we can pipe data into the module. This way we could run it indefinitely... :)
