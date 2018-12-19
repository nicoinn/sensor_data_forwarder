import json


class Sensor_record(object):

    def __init__(selfself,sensor):
        return

    def get_timestamp(self):
        return None

    def get_name(self):
        return ""

    def get_data(self):
        return {}

    def __repr__(self):
        return "Sensor object template"


class Telldus_Sensor_record(Sensor_record):
        
    def __init__(self, sensor):
        import tellcore.constants as td_cst
        
        def get_custom_name(sensor):
            try :
                from sensor_mapping import sensor_mapping
                name = sensor_mapping[(sensor.protocol,sensor.model,int(sensor.id))]
                self.mapped = True
                return name
            
            except:
                self.mapped = False
                return None
            
        self.sensor_id = {"protocol" : sensor.protocol,"model" : sensor.model, "id" : sensor.id, "custom_name" : get_custom_name(sensor)}
        
        if sensor.has_value(td_cst.TELLSTICK_TEMPERATURE):
            value = sensor.value(td_cst.TELLSTICK_TEMPERATURE)
            self.temperature = value.value
            self.timestamp = value.timestamp
        else:
            self.temperature = None
            self.timestamp = None
            
        if sensor.has_value(td_cst.TELLSTICK_HUMIDITY):
            value = sensor.value(td_cst.TELLSTICK_HUMIDITY)
            self.humidity = value.value
            if self.timestamp is None:
                self.timestamp = value.timestamp
        else:
            self.humidity = None
            
    def get_timestamp(self):
        return self.timestamp
    
    def get_name(self):
        if self.mapped==True:
            return self.sensor_id["custom_name"]
        return self.sensor_id["protocol"] + "_" + self.sensor_id["model"] + "_" + str(self.sensor_id["id"])
    
    def get_data(self):
        d = dict()
        if self.temperature is not None:
            d["temperature"] = self.temperature
        if self.humidity is not None:
            d["humidity"] = self.humidity
        return d        
        
    
    def __repr__(self):
        import time 
        
        if self.mapped==False:
            outstr = self.sensor_id["protocol"] + "/" + self.sensor_id["model"] + " sensor ID " + str(self.sensor_id["id"]) + ": "
        else:
            outstr = self.sensor_id["custom_name"]+": "
        
        if self.temperature is not None:
            outstr+= str(self.temperature) + "C "
            if self.humidity is not None:
                outstr+= " - "
        if self.humidity is not None:
                outstr+= str(self.humidity) + "% "
        
        if self.timestamp is not None:
                outstr+= "(last seen " + str(int(time.time())-self.timestamp) + "s ago)"
        return outstr 
    
    
class Dummy_record(Telldus_Sensor_record):
        def __init__(self,name="EmonCMS_Reporter_Dummy",Temperature=42,Humidity=42,mapped=True):
            import time
            self.timestamp = int(time.time())
            self.sensor_id = {"protocol" : "dummy","model" : "sample", "id" : 0, "custom_name" : name}
            self.mapped = mapped
            self.temperature = Temperature
            self.humidity = Humidity


class Sparsnas_Sensor_record(Sensor_record):

    def __init__(self, sensor):
        self.record = json.loads(sensor)
        self.mapped = True

    def get_timestamp(self):
        return self.record["time"]

    def get_name(self):
        return "Sparnas_ID_{0}".format(self.record["sensorID"])

    def get_data(self):
        return {x: self.record[x] for x in self.record if x not in ["time","sensorID"]}

    def __repr__(self):
        return str(self.record)






