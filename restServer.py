import csv 
from datetime import datetime

#!/usr/bin/python

def rest_server(dummy, state,timeState):
    from bottle import route, run, get, post, request, static_file, abort
    from subprocess import call
    from datetime import datetime
    import config as conf
    import os

    # '/root/silvia-pi'#os.path.dirname(__file__)
    basedir = os.path.dirname(os.path.abspath(__file__))
    wwwdir = basedir+'/www/'

    @route('/')
    def docroot():
        return static_file('index.html', wwwdir)

    @route('/<filepath:path>')
    def servfile(filepath):
        return static_file(filepath, wwwdir)

    @route('/curtemp')
    def curtemp():
        return str(state['avgtemp'])

    @get('/settemp')
    def settemp():
        return str(state['settemp'])

    @post('/settemp')
    def post_settemp():
        try:
            settemp = float(request.forms.get('settemp'))
            if settemp >= conf.low_temp_b and settemp <= conf.high_temp_b:
                state['settemp'] = settemp
                return str(settemp)
            else:
                print("wrong temp 186")
                # abort(400,'Set temp out of range 200-260.')
        except:
            print("line189 wrong number set temp")
            # abort(400,'Invalid number for set temp.')

    @post('/setsteamtemp')
    def post_setsteamtemp():
        try:
            steamtemp = float(request.forms.get('steamtemp'))
            if steamtemp >= conf.low_temp_s and steamtemp <= conf.high_temp_s:
                state['steamtemp'] = steamtemp
                return str(steamtemp)
            else:
                print("wrong temp 53")
                # abort(400,'Set temp out of range 200-260.')
        except:
            print("line56 wrong number set temp")
            # abort(400,'Invalid number for set temp.')


    @get('/snooze')
    def get_snooze():
        return str(state['snooze'])

    @post('/snooze')
    def post_snooze():
        snooze = request.forms.get('snooze')
        try:
            datetime.strptime(snooze, '%H:%M')
        except:
            print("line202,wrong time format")
            # abort(400,'Invalid time format.')
        state['snoozeon'] = True
        state['snooze'] = snooze
        return str(snooze)

    @post('/resetsnooze')
    def reset_snooze():
        state['snoozeon'] = False
        return True

    @get('/allstats')
    def allstats():
        
        # with open("tempcsv.csv","a+") as tempFile:
        #     fieldNames = ["time","avgtemp","settemp","steamtemp"]
        #     writer = csv.DictWriter(tempFile,fieldnames=fieldNames)
        #     writer.writerow({"time": datetime.now(), "avgtemp":state["avgtemp"],"settemp":state["settemp"],"steamtemp":state["steamtemp"]})
        return dict(state)

    @get('/alltime')
    def alltime():
        return dict(timeState)

    @route('/restart')
    def restart():
        call(["reboot"])
        return ''

    @route('/shutdown')
    def shutdown():
        call(["shutdown", "-h", "now"])
        return ''

    @get('/healthcheck')
    def healthcheck():
        return 'OK'

    @post('/TimerOnMo')
    def post_TimerOnMo():
        TimerOnMo = request.forms.get('TimerOnMo')
        try:
            datetime.strptime(TimerOnMo,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnMo'] = TimerOnMo
        return str(TimerOnMo)

    @post('/TimerOnTu')
    def post_TimerOnTu():
        TimerOnTu = request.forms.get('TimerOnTu')
        try:
            datetime.strptime(TimerOnTu,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnTu'] = TimerOnTu
        return str(TimerOnTu)

    @post('/TimerOnWe')
    def post_TimerOnWe():
        TimerOnWe = request.forms.get('TimerOnWe')
        try:
            datetime.strptime(TimerOnWe,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnWe'] = TimerOnWe
        return str(TimerOnWe)

    @post('/TimerOnTh')
    def post_TimerOnTh():
        TimerOnTh = request.forms.get('TimerOnTh')
        try:
            datetime.strptime(TimerOnTh,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnTh'] = TimerOnTh
        return str(TimerOnTh)

    @post('/TimerOnFr')
    def post_TimerOnFr():
        TimerOnFr = request.forms.get('TimerOnFr')
        try:
            datetime.strptime(TimerOnFr,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnFr'] = TimerOnFr
        return str(TimerOnFr)

    @post('/TimerOnSa')
    def post_TimerOnSa():
        TimerOnSa = request.forms.get('TimerOnSa')
        try:
            datetime.strptime(TimerOnSa,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnSa'] = TimerOnSa
        return str(TimerOnSa)

    @post('/TimerOnSu')
    def post_TimerOnSu():
        TimerOnSu = request.forms.get('TimerOnSu')
        try:
            datetime.strptime(TimerOnSu,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOnSu'] = TimerOnSu
        return str(TimerOnSu)

    @post('/TimerOffMo')
    def post_TimerOffMo():
        TimerOffMo = request.forms.get('TimerOffMo')
        try:
            datetime.strptime(TimerOffMo,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffMo'] = TimerOffMo
        return str(TimerOffMo)

    @post('/TimerOffTu')
    def post_TimerOffTu():
        TimerOffTu = request.forms.get('TimerOffTu')
        try:
            datetime.strptime(TimerOffTu,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffTu'] = TimerOffTu
        return str(TimerOffTu)

    @post('/TimerOffWe')
    def post_TimerOffWe():
        TimerOffWe = request.forms.get('TimerOffWe')
        try:
            datetime.strptime(TimerOffWe,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffWe'] = TimerOffWe
        return str(TimerOffWe)

    @post('/TimerOffTh')
    def post_TimerOffTh():
        TimerOffTh = request.forms.get('TimerOffTh')
        try:
            datetime.strptime(TimerOffTh,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffTh'] = TimerOffTh
        return str(TimerOffTh)

    @post('/TimerOffFr')
    def post_TimerOffFr():
        TimerOffFr = request.forms.get('TimerOffFr')
        try:
            datetime.strptime(TimerOffFr,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffFr'] = TimerOffFr
        return str(TimerOffFr)

    @post('/TimerOffSa')
    def post_TimerOffSa():
        TimerOffSa = request.forms.get('TimerOffSa')
        try:
            datetime.strptime(TimerOffSa,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffSa'] = TimerOffSa
        return str(TimerOffSa)

    @post('/TimerOffSu')
    def post_TimerOffSu():
        TimerOffSu = request.forms.get('TimerOffSu')
        try:
            datetime.strptime(TimerOffSu,'%H:%M')
        except:
            abort(400,'Invalid time format.')
        timeState['TimerOffSu'] = TimerOffSu
        return str(TimerOffSu)


    run(host='0.0.0.0', port=conf.port, server='auto')
