from datetime import datetime
import urllib.request


# converts a list of timestamps into a dictionary with the hour as keys, and
# dictionaries as values where minutes are keys and values are another dict
# containing seconds as keys and number of instances of that second as values
def list_to_dict(timestamps: list) -> dict:
    timesdict = {}
    for time in timestamps:
        hrs = int(time[:2])
        mins = int(time[3:5])
        sec = int(time[6:])
        if hrs in timesdict:
            saved_mins = timesdict[hrs]
            if mins in saved_mins.keys():
                saved_secs = timesdict[hrs][mins]
                if sec in saved_secs:
                    timesdict[hrs][mins][sec] = timesdict[hrs][mins][sec] + 1  # increment # of instances
                else:
                    timesdict[hrs][mins][sec] = 1
            else:
                timesdict[hrs][mins] = {sec: 1}
        else:
            timesdict[hrs] = {mins: {sec: 1}}
    return timesdict


def callapi(times: dict) -> None:
    print('Call API script is now running. Progress will be recorded below as it occurs.')
    while True:
        # Get current date/time
        now = datetime.now()
        curr_time = str(now.strftime("%H:%M:%S"))
        curr_hour = int(curr_time[:2])
        curr_min = int(curr_time[3:5])
        curr_sec = int(curr_time[6:])

        # if it is midnight, the day is over, and we need a new input list of timestamps
        # In future real world application, this process should be automated with a new
        # input list for the new day automatically inputed, instead of terminating
        if curr_time == '00:00:00':
            print("End of Day reached, process terminating.")
            break
        # if the current hour is not in the times dictionary, sleep
        if curr_hour not in times:
            continue
        else:
            # the current hour is a key in the times dict, so we now will need to check
            # at what minute and second is stored in times dict (i.e. when to make the
            # api call within this hour)

            # if the current minute is not in the current hour's dict of minutes, sleep
            if curr_min not in times[curr_hour]:
                continue
            else:
                # the current minute is a key in the current hours' dict, so we now will
                # need to check at what second is stored (i.e. when to make the api call
                # within the minute)

                # if the current second is not in the current minute's list of seconds, sleep
                if curr_sec not in times[curr_hour][curr_min]:
                    continue
                else:
                    # Now we send the Get request per number of recorded instances of that second
                    for _ in range(times[curr_hour][curr_min][curr_sec]):

                        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'

                        url = "http://ifconfig.co"
                        headers = {'User-Agent': user_agent, }

                        request = urllib.request.Request(url, None, headers)  # The assembled request
                        response = urllib.request.urlopen(request)
                        #data = response.read()  # Not needed for this, but its here

                        curr_time_str = str(curr_hour) + ":" + str(curr_min) + ":" + str(curr_sec)
                        if response.status == 200:
                            print("API call sent at " + curr_time_str + " was successful.")
                        else:
                            print("API call failed at " + curr_time_str + " with status code " + str(response.status))
                    tmp = times[curr_hour][curr_min].pop(curr_sec)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # First we prompt the user to input today's list of timestamps.
    # In future real world application, this process should be automated, not user input
    # Example input: 09:15:25,11:58:23,13:45:09,13:45:09,13:45:09,17:22:00,17:22:00
    inputstr = input("Please enter the list of timestamps for the day separated by a comma: ")

    # We want to split the string input using the commas
    inputlist = inputstr.split(',')

    # Next, we will convert the inputlist into a dictionary for efficiency
    inputdict = list_to_dict(inputlist)

    now = datetime.now()
    year = now.strftime("%Y")
    year = int(year)
    month = now.strftime("%m")
    month = int(month)
    day = now.strftime("%d")
    day = int(day)
    callapi(inputdict)
