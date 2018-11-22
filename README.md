# Sensor data Forwarded
A small Python daemon to query and forward sensor data accross various platform, currently focused on reading from Telldus Tellstick Duo and forwarding to EmonCMS. More platforms will eventually come :)

# Prerequisites
- A [Tellstick duo](http://telldus.com/produkt/tellstick-duo/) or an equivalent product that works with TelldusCore
- The TelldusCore Python library : `pip install tellcore-py`
- Currently, only Python 2.7 is supported

# Running the thing
- Edit sensor_mapping.py to suit your sensor setup
- Edit telldus_forwarder.py to configure one of EmonCMS url and API key
- Run it: `python ./telldus_forwarder.py`  
