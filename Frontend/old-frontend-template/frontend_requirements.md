React frontend must be able to be hosted from Pi or cloud, in tandem with the web api backend. From a technical standpoint the frontend must
- Make REST calls to API backend
    - GET previous data
    - POST commands 
    - GET auth validated
    - POST new auth
    - POST command to request Pi to emit live updates (5sec)
    - REST calls should be at a domain name (ex api.reacreate-energy.com/api/v1/...) if cloud is accessible or else (ex localhost/api/v1/...), such that the same frontend code can be used locally and in the cloud without any changes or re-config to the files
- Listen to mqtt broker over websocket for live updates (5 sec)

Technically speaking, React could probably do many of these things without a backend, but using a dedicated API is from what I gather considered best practice.  