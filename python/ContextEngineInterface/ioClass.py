import gdp
import json
import bluetooth
# Input/output class. Identifies the gcl_name and parameter_name for each input or output.

def collectTrace(gclHandle, param, start, stop):
    # this is the actual subscribe call
    gclHandle.multiread(start, stop-start+1)

    # timeout
    t = {'tv_sec':0, 'tv_nsec':500*(10**6), 'tv_accuracy':0.0}
    data = []
    while True:
        # This could return a None, after the specified timeout
        event = gdp.GDP_GCL.get_next_event(t)
        if event is None or event["type"] == gdp.GDP_EVENT_EOS:
            break
        datum = event["datum"]
        handle = event["gcl_handle"]
        data.append(float(json.loads(datum['data'])[param]))
    return data

class ioClass(object):
    # TODO: Fix number of passed parameters
    def __init__(self, srcSink = "", nameStr = "", paramName = "", lagVal = 0, normMeth = 'none', 
                key = "", password = ""):
        if nameStr == "":
            raise ValueError ("Name must be provided.")
        if paramName == "":
            raise ValueError ("JSON parameter name must be provided.") 
        if srcSink == "":
            raise ValueError ("Source/Sink must be provided.")
        elif srcSink == "GDP_I":
            self.IO = 'in'
            self.IOtype = 'GDP'
            # Assume that GCL already exists and create the GCL handle
            # Log name in GDP
            self.gclName = gdp.GDP_NAME(nameStr)
            self.gclHandle = gdp.GDP_GCL(self.gclName, gdp.GDP_MODE_RO)
        elif srcSink == "BT_I":
            print "BT"
            self.IO = 'in'
            self.IOtype = 'BT'
            self.btAddr = nameStr
        elif srcSink == "GDP_O":
            print nameStr
            # Log name in GDP
            self.gclName = gdp.GDP_NAME(nameStr)
            self.gclHandle = gdp.GDP_GCL(self.gclName, gdp.GDP_MODE_RO)
            self.IO = 'out'
            self.IOtype = 'GDP'
            if key == "" or password == "":
                raise ValueError ("Key path and password must \
                            be provided.")
            else:
                skey = gdp.EP_CRYPTO_KEY(filename=key,
                                keyform=gdp.EP_CRYPTO_KEYFORM_PEM,
                                flags=gdp.EP_CRYPTO_F_SECRET)
                open_info = {'skey': skey}
                # TODO Bypass password prompt
                # Assume that GCL already exists and create the GCL handle
                self.gclHandle = gdp.GDP_GCL(self.gclName, gdp.GDP_MODE_RA, open_info)
        # JSON parameter name to be used in each log record
        self.param = paramName
        # Lag from the current record. Can be used to implement time series functions.
        self.lag = lagVal
        # Normalization method for data:
        # 'none': no normalization
        # 'lin': linear normalization: mean-zeroed and divided by std
        self.norm = normMeth
        # Normalization parameters (i.e., avg, std etc.)
        self.normParam = {}

    def printTester(self):
        print self.gcl, self.param, self.lag
    def readLog(self, start, stop): 
        param = self.param
        handle = self.gclHandle            
        lag = self.lag
        trace = collectTrace(handle, param, start - lag, stop - lag)
        return trace
    def subscribe(self):
        if self.IO == 'in':
            if self.IOtype == 'BT':
                self.btSock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
                self.btSock.connect((self.btAddr, 1)) # Fixed to port 1
            else:   # Assume GDP log
                self.gclHandle.subscribe(0, 0, None)
        else:
            raise ValueError ('Subscription is not defined for output ports')
    def getNextData(self):
        ## NOTE How to identify log?! next line. How to muliti-Log?!
        ## NOTE Maybe you subs to all and it returns event for each?!
            ## NOTE ^^ Yeah, exactly that.^^
        newRecord = gdp.GDP_GCL.get_next_event(None)
        newDataPoint = json.loads(newRecord['datum']['data'])['temperature_celcius']
#        print newDataPoint
        return newDataPoint
    def write(self, data):
        if self.IO == 'in':
            raise ValueError ('Cannot write to input port.')
        else:
            datDict = {"data": data}
            self.gclHandle.append(datDict)
