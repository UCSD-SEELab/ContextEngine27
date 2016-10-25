import serial
import json, sys
import gdp
# check for valid json string to filter out other communicated messges.
def is_json(mystr):
    try:
        json_object = json.loads(mystr)
    except ValueError, e:
        return False
    return True

def reformatKeys(jsonLine):
    outDict = {}
    outDict["CO2"] = jsonLine['co2']['CO2']
    outDict["bP"] = jsonLine['hu_pr']['bP'] # barometric pressure milibar(mBar)
    outDict["bT"] = jsonLine['hu_pr']['bT'] # Temp from pressure sensor (Celcius)
    outDict["hH"] = jsonLine['hu_pr']['hH'] # relative humidity %
    outDict["hT"] = jsonLine['hu_pr']['hT'] # temperature from humidity sensor (Celsius)
    # Calculated part per billion for gas pollutants
    outDict["AQI"] = jsonLine['ppb']['AQI'] # unitless
    outDict["CO_PPM"] = jsonLine['ppb']['CO']
    outDict["NO2_PPB"] = jsonLine['ppb']['NO2']
    outDict["OX_PPM"] = jsonLine['ppb']['OX']

    outDict["S1W"] = jsonLine['raw']['S1W']

    return outDict


#if len(sys.argv) < 4:
#    print 'Usage: python %s <serial_port> <log_name> <key_path>' % sys.argv[0]
#    sys.exit(1)
#else:
#    serial_port = sys.argv[1]
#    name_str = sys.argv[2]
#    keyfile = sys.argv[3]

serial_port = '/dev/ttyACM0'
#name_str = 'OQa5mdiJ2nK1qq4gfJh75FDsjLlCl_BRL8hkhMpVCGA' # gdp-02
name_str = 'DV9CXF9WwOzYE_0blrSGR0Iw4FWNtlWTBoA-3_oAUeM' # gdp-01
#keyfile = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.pem'
keyfile = 'visReady.pem'


# serial_port = 'dev/ttyACM0' # Tested on Raspberry Pi
ser = serial.Serial(serial_port, timeout = 2)
print 'Receving serial data from: ', ser.name
# Initiate sensor data stream.
ser.write('{"msg":"cmd","usb":1}')

# Output log information
# keyfile = 'DgAAAOjbtnYAAAAA-Nm2dkD2j36MofJ2AAAAAAAAAAA.pem'
# name_str = '58jK2obVbOma7OwQNkgA7kuYqrEVcy4Tw5hMlREn5jY'
skey = gdp.EP_CRYPTO_KEY(filename=keyfile,
                                keyform=gdp.EP_CRYPTO_KEYFORM_PEM,
                                flags=gdp.EP_CRYPTO_F_SECRET)
# Create a GDP_NAME object from a python string provided as argument
gcl_name = gdp.GDP_NAME(name_str)

# There's a GCL with the given name, so let's open it
gcl_handle = gdp.GDP_GCL(gcl_name, gdp.GDP_MODE_AO,
                                open_info={'skey':skey})


i = 0
while 1:
    line = ser.readline()
    if is_json(line):
        jsonLine = json.loads(line)
        if 'msg' in jsonLine:
            if jsonLine['msg'] == 'read':
                i = i + 1
                visReadyJSON = json.dumps(reformatKeys(jsonLine))
#                print visReadyJSON
                print 
                print 'Record: ', i, ', ', visReadyJSON
                datum = {'data': str(visReadyJSON)}
                gcl_handle.append(datum)
