# Recreate-Energy
Recreate Energy Main Github

- Arduino -> Arduino. Reads from sensors and writes out to serial.
- Pi -> Pi. Pi should have two scripts running. One for backups, which writes to the AWS TimestreamDB. And one for sending/reccieving lines over serial from Arduino, and savings those sensor readings to the local SQL database.
- API -> API in python
- Frontend -> UI using react


Remember that our AWS region is **Oregon**.
