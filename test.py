t1 = '07:00 PM'
t2 = '05:00 PM'
t3 = '11:00 AM'

currentTime = t1
returnedValue = t2

if currentTime[6:8] == 'AM' and returnedValue[6:8] == 'PM':
    t = 'current time is before '

   '''
    if given_time[5:7] == 'AM' and current_time == 'PM':
        print(True)
    elif given_time[5:7] == 'PM' and current_time == 'AM':
        print(False)
    else: # same part of day
        if int(given_time[0:2]) < int(current_time[0:2]): # compare Hour
            print(True)
        elif int(given_time[0:2]) > int(current_time[0:2]):
            print(False)
        else:
            if int(given_time[3:5]) < int(current_time[3:5]): # compare Minute
                print(True)
            elif int(given_time[3:5]) > int(current_time[3:5]):
                print(False)
            else:
                print("Times are the same")
    '''

