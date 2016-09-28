import gdp
import time

name_str = '58jK2obVbOma7OwQNkgA7kuYqrEVcy4Tw5hMlREn5jY'
#name_str = 'edu.berkeley.eecs.bwrc.device.c098e5300036'
shift = 10
start = 1 + shift
stop = 100001 + shift


gcl_name = gdp.GDP_NAME(name_str)

gcl_handle = gdp.GDP_GCL(gcl_name, gdp.GDP_MODE_RO)

begin = time.time()
gcl_handle.multiread(start, stop - start + 1)
time1 = time.time() - begin
t = {'tv_sec':0, 'tv_nsec':500*(10**6), 'tv_accuracy':0.0}
data_len = 0
while True:
    # This could return a None, after the specified timeout
    event = gdp.GDP_GCL.get_next_event(t)
    if event is None or event["type"] == gdp.GDP_EVENT_EOS:
        break
    datum = event["datum"]
    handle = event["gcl_handle"]
    data_len = data_len + len(datum)
    #print datum

time2 = time.time() - begin
print len(datum)
print time1, time2
print len(datum) * (stop - start) / (time2 - time1)
print data_len / (time2 - time1)
