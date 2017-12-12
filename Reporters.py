class Reporter(object):

    def __init__(self,only_mapped=False):
        self.__buffer = []
        self.__latest_commit_time = 0
        self.__latest_flush_time = 0
        self.__only_mapped = only_mapped
    
    def report_async(self,sensor_record):

        #Ignore unmapped sensors if selected
        if ((self.__only_mapped == True) & (sensor_record.mapped==False)):
            return
        
        #Will ignore sensor data older than the last flush (they are already reported or in the buffer)
        if sensor_record.get_timestamp()<self.__latest_flush_time:
            return
        
        self.__buffer.append(sensor_record)
    
    def report(self,sensor_record):
        self.report_async(sensor_record)
        self.flush_buffer()
        
    def flush_buffer(self):
        from math import floor 
        import time

        self.__latest_flush_time = int(floor(time.time()))
        
        #Remove duplicates
        self.__buffer = list(set(self.__buffer))
        
        while len(self.__buffer)>0:
            d = self.__buffer.pop()
            if (self.commit_one(d) != True):
                #If something went wrong, stop, rebuffer the element and wait till next flush attempt for retry
                self.__buffer.append(d)
                break
        self.__latest_commit_time = int(floor(time.time()))
        
        
class Console_Reporter(Reporter):

    def __init__(self,only_mapped=False):
        super(Console_Reporter,self).__init__(only_mapped)

    def commit_one(self,d):
        print d
        return True
    

class EmonCMS_Reporter(Reporter):

    def __init__(self, URL,apikey=None,node=None,only_mapped=True):
        #URL must include port and path up to the emoncms root
        #ex: http://foo.bar:8080/emoncms/
        
        import time
        from math import floor
        
        super(EmonCMS_Reporter,self).__init__(only_mapped)
        
        self.url = URL + ("/" if URL[-1]!="/" else "" )    
        self.apikey = apikey
        self.node = node
        
        #Check if everything works
        from Sensor_record import Dummy_record
        dummy = Dummy_record()
        
        t = self.commit_one(dummy)
        
        if (t !=True):
            print "Something is wrong - Cannot continue"
            print t
            raise 
        
    
    def commit_one(self,sensor):        
    
    	#Build a query URL for the EmonCMS Input API
        query = self.url+"input/post?"
        
        query+="time=" + str(sensor.get_timestamp()) + "&"
        
        if self.node is not None:
            query+="node="+self.node+"&"
            
        name=sensor.get_name()
        
        payload = sensor.get_data()
        
        json_str = str()
        for (suffix,data) in payload.iteritems():
            json_str+=name+"_"+suffix+":"+str(data)+","
        json_str = json_str[0:-1]

        query += "json={" + json_str + "}"
        
        if self.apikey is not None:
            query+="&apikey=" + self.apikey
            
        #Make a simple http query
        #(This part is very slow - to be improved later)
        import urllib2
        r=[]
        try: 
            r = urllib2.urlopen(query).read()
        except:
            return "Queried URL: "+ query
        
        if r=="ok":
            return True
        
        return "Queried URL: "+ query + "\nResponse from server: " + r
        


