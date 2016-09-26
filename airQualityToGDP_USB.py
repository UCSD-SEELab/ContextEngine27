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

if len(sys.argv) < 4:
    print 'Usage: python %s <serial_port> <log_name> <key_path>' % sys.argv[0]
    sys.exit(1)
else:
    serial_port = sys.argv[1]
    name_str = sys.argv[2]
    ketfile = sys.argv[3]

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
    i = i + 1
    line = ser.readline()
    if is_json(line):
        jsonLine = json.loads(line)
        if 'msg' in jsonLine:
            if jsonLine['msg'] == 'read':
                #print 'line: ', i, ', ', line
                datum = {'data': line}
                gcl_handle.append(datum)
