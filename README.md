# Diskussed-backend

This repo has 2 components:

## API endpoint to process request from https://github.com/mrahul17/diskussed

It simply accepts the hashed url from the client and matches it against a prepopulated database.
It currently runs as a Supabase edge function.


## Cron to fetch latest discussions and store it

This is inspired from https://github.com/ashish01/hn-data-dumps . Currently it is running on a schedule as a Github action that fetches from HN's api and stores it in a Postgres db. This implementation is likely to change depending on how reliable Github action proves to be.
This badge should show if the cron is working fine:

![Fetch New Discussions workflow](https://github.com/mrahul17/Diskussed-backend/actions/workflows/fetch_new_discussions.yml/badge.svg?query=branch%3Amaster)

Contributions and feedback are welcome and will help to improve experience of the Diskussed extension.


Diskussed-backend is licensed under **MIT License**
