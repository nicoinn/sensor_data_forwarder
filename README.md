# Tellduscore Forwarded
A Python daemon to query sensor data from the Telldus Tellstick Duo and forward to EmonCMS and more


# Prerequisites
- A [Tellstick duo](http://telldus.com/produkt/tellstick-duo/) or an equivalent product that works with TelldusCore
- The TelldusCore Python library : `pip install tellcore-py`
- Currently, only Python 2.7 

# Running the thing
- Edit sensor_mapping.py to suit your sensor setup
- Edit telldus_forwarder.py to configure one of EmonCMS url and API key
- Run it: `python ./telldus_forwarder.py`  
