# Web API
Tested with Python 3.9.12

Monitoring the broker:
https://us-west-2.console.aws.amazon.com/iot/home?region=us-west-2#/test


AWS IoT Core has Policies and Things. Policies are like "roles", that restrict access of certain Things. Things are devices and services that will connect to our IoT Core MQTT Broker.

And no, FWIU you really shouldn't store credential files on your git repo. 

The current endpoint is 
```a2kubfstl68fu2-ats.iot.us-west-2.amazonaws.com```

at somepoint we should change this to 
```api.recreateenergy.com```

Reference:
https://aws.amazon.com/premiumsupport/knowledge-center/iot-core-publish-mqtt-messages-python/
https://fastapi.tiangolo.com/


