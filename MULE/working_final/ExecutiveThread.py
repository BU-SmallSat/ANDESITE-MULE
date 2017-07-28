import logging
import Queue
import sys
import time
from threading import BoundedSemaphore
from DeploymentThread import DeploymentThread
from EPSThread import EPSThread
from ADCThread import ADCThread
from GlobalstarThread import GlobalstarThread
from RFM22BThread import RFM22BThread

'''*******************GLOBAL STATIC DEFINES************************'''
FIFTEEN_MINUTES = 60 #900
THIRTY_MINTUES = 120 #1800
TWO_ORBIT = 120 #10800
'''****************************************************************'''

'''*******************GLOBAL SYSTEM DEFINES************************'''
GPSenabled=0
GPSantennaEnabled = 0
EndOfLife = False
BDOTcheck = False
DeployerEnabled = False
GlobalstarEnabled = False
GroundContact = False
DeployerConnected = False
DeployerCheck = False
WSNcontact = False
'''****************************************************************'''


def FunctionalTest():
    #should we actually turn on the switches and test communication

    print("*** BEGINING ANDESITE FLIGHT COMPUTER FUNCTIONAL TEST ***")

    Power.inputQueue.put("PE:EPSswitchesStatus")
    response = waitForResp(.5)
    if response == "EP:SwitchStateSuccess":
        print("************ SUCCESSFUL EPS SWITCHERS STATUS EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS SWITCHERS STATUS EXECUTION ----------")
    '''
    Power.inputQueue.put("PE:switchOnAntenna")
    response = waitForResp(.5)
    if response == "EP:AntennaOn":
        print("************ SUCCESSFUL EPS ANTENNA SWITCHER ENABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS ANTENNA SWITCHER ENABLE EXECUTION ----------")

    Power.inputQueue.put("PE:switchOnGPS")
    response = waitForResp(.5)
    if response == "EP:GPSOn":
        print("************ SUCCESSFUL EPS GPS SWITCHER ENABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS GPS SWITCHER ENABLE EXECUTION ----------")

    Power.inputQueue.put("PE:switchOnDeployer")
    response = waitForResp(.5)
    if response == "EP:DeployerOn":
        print("************ SUCCESSFUL EPS DEPLOYER SWITCHER ENABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS DEPLOYER SWITCHER ENABLE EXECUTION ----------")

    Power.inputQueue.put("PE:EPSswitchesStatus")
    response = waitForResp(.5)
    if response == "EP:SwitchStateSuccess":
        print("************ SUCCESSFUL EPS SWITCHERS STATUS EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS SWITCHERS STATUS EXECUTION ----------")
    '''
    '''
    Comm.inputQueue.put("CE:enableGlobalstar")
    ##NEED ENABLES FOR THE EPS SWITCHES: gps, gps antenna, deployer board comm and vbatt, globalstar?
    Comm.inputQueue.put("CE:globalStarHealth")
    response = waitForResp()
    if response == "EC:ConnectionFail" or  "EC:ConnectionSucces:" in response :
        print("************ SUCCESSFUL GLOBALSTAR HEALTH TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH GLOBALSTAR HEALTH TEST EXECUTION ----------")
    '''
    '''
    Power.inputQueue.put("PE:EPSHealth")
    response = waitForResp(.5)
    if response == "EP:healthTestSuccess":
        print("************ SUCCESSFUL EPS HEALTH TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS HEALTH TEST EXECUTION ----------")
    '''
    ADC.inputQueue.put("AE:readMagData")
    response = waitForResp(.5)
    if response == "EA:magReadSuccess":
        print("************ SUCCESSFUL MAG SELF TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH MAG SELF TEST EXECUTION ----------")
    '''
    ADC.inputQueue.put("AE:iMTQSelfTest")
    response = waitForResp()
    if response == "EA:selfTestSuccess":
        print("************ SUCCESSFUL MAG SELF TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH MAG SELF TEST EXECUTION ----------")
    ADC.inputQueue.put("AE:Detumbling")
    response = waitForResp()
    if response == "EA:detumblingSuccess":
        print("************ SUCCESSFUL B-DOT TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH B-DOT TEST EXECUTION ----------")
    ADC.inputQueue.put("DE:SerialTest")
    response = waitForResp()
    if response == "EA:detumbleSuccess":
        print("************ SUCCESSFUL B-DOT TEST EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH B-DOT TEST EXECUTION ----------")
    '''

    '''
    Deployer.inputQueue.put("DE:CheckSerial")
    response = waitForResp()
    if response == "ED:SerialConnected":
        print("************ SUCCESSFUL DEPLOYER BOARD CONNECTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH DEPLOYER BOARD CONNECTION ----------")
    '''
    '''
    Power.inputQueue.put("PE:switchOffAntenna")
    response = waitForResp(.5)
    if response == "EP:AntennaOff":
        print("************ SUCCESSFUL EPS ANTENNA SWITCHER DISABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS ANTENNA SWITCHER DISABLE EXECUTION ----------")

    Power.inputQueue.put("PE:switchOffGPS")
    response = waitForResp(.5)
    if response == "EP:GPSOff":
        print("************ SUCCESSFUL EPS GPS SWITCHER DISABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS GPS SWITCHER DISABLE EXECUTION ----------")

    Power.inputQueue.put("PE:switchOffDeployer")
    response = waitForResp(.5)
    if response == "EP:DeployerOff":
        print("************ SUCCESSFUL EPS DEPLOYER SWITCHER DISABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS DEPLOYER SWITCHER DISABLE EXECUTION ----------")

    Power.inputQueue.put("PE:EPSswitchesStatus")
    response = waitForResp(.5)
    if response == "EP:SwitchStateSuccess":
        print("************ SUCCESSFUL EPS SWITCHERS STATUS EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH EPS SWITCHERS STATUS EXECUTION ----------")
    '''
    '''
    RFM22B.inputQueue.put(""RE:radioInit")
    response = waitForResp()
    if response == "ER:RadioInitSuccess":
        print("************ SUCCESSFUL RFM22B RADIO ENABLE EXECUTION ***************")
    elif response == "EP:lowPowerMode":
        lowPowerMode()
    else:
        print("------- PROBLEM OCCURED WITH RFM22B RADIO ENABLE EXECUTION ----------")
    '''


def waitForResp(timeout):
    while True:
        try:
            threadResponse = inputQueue.get(False)
            print(threadResponse)
            # response = processMessage(threadResponse)
            return threadResponse
        except Queue.Empty:
            pass
        time.sleep(timeout)


def lowPowerMode():
    # disable all threads

    # tell EPS thread that we are ready for low power mode
    processMessage("PE:lowPowerReady")

    # wait for response from EPS thread saying that low power mode is over
    waitForResp(60)

    # turn back on all threads


def lowPowerMode_GroundCommand():
    # disable all threads

    # tell EPS thread that we are ready for low power mode
    processMessage("PE:lowPowerReady")

    # wait for message from GROUND to power up? or from EPS to return to normal operations
    waitForResp(60)
    # turn back on all threads


def healthPoll():
    # need to tell EPS to pass most recent EPS data
    processMessage("PE:HealthPoll")
    EPSSemaphore.release()
    # need to tell GPS to pass most recent data and need to collect 5 sec of IMU and accelerometer data
    processMessage("AE:HealthPoll")
    ADCSemaphore.release()
    # wait for threads to finish with their data aquiring
    EPSlock = False
    ADClock = False
    while EPSlock is False and ADClock is False:
        try:
            threadResponse = inputQueue.get(False)
            processMessage(threadResponse)
        except Queue.Empty:
            pass
        EPSlock = EPSSemaphore.acquire(blocking=False)
        ADClock = ADCSemaphore.acquire(blocking=False)
    processMessage("CE:HealthPoll")


def ADCInterpreter(string):
    global BDOTcheck
    if string == "EA:BDOTdisabled":
        BDOTcheck = True
    elif string == "EA:disableFailure":
        BDOTcheck = True


def CommInterpreter(string):
    global BDOTcheck
    global DeployerEnabled
    global GlobalstarEnabled
    global GroundContact
    if string == "EC:lowPowerMode":
        lowPowerMode_GroundCommand()
    elif string == "EC:EnableDeployer":
        # wait for EPS thread to respond saying that threads are working
        DeployerCheck = False
        while DeployerCheck is False:
            try:
                threadResponse = inputQueue.get(False)
                print(threadResponse)
                processMessage(threadResponse)
            except Queue.Empty:
                pass
        if DeployerEnabled is True:
            processMessage("DE:CheckSerial")
            while DeployerConnected is False:
                try:
                    threadResponse = inputQueue.get(False)
                    processMessage(threadResponse)
                except Queue.Empty:
                    pass
        else:
            #downlink response saying Deployer is Disabled
            processMessage("CE:DeployerDisabled")
    elif "EC:deployPair" in string:
        if DeployerEnabled is True:
            # check that bdot is not enabled
            processMessage("AE:DisableBDOT")
            # wait for response from ADC thread
            BDOTcheck = False
            while BDOTcheck is False:
                try:
                    threadResponse = inputQueue.get(False)
                    processMessage(threadResponse)
                except Queue.Empty:
                    pass
            # tell deployer thread to deploy pair of nodes
            reply = "DE:Deploy" + string[-1:]
            print(reply)
            processMessage(reply)
        else:
            #downlink response saying Deployer is Disabled
            processMessage("CE:DeployerDisabled")
    elif string == "EC:GlobalstarEnabled":
        GlobalstarEnabled = True
    elif string == "EC:GlobalstarDisabled":
        GlobalstarEnabled = False
    elif string == "EC:HelloAndesite":
        print("CONTACT WITH GROUND STATION!")
        GroundContact = True
    elif string == "EC:HealthPoll":
        healthPoll()


def DeployerInterpreter(string):
    global DeployerConnected
    global DeployerEnabled
    if string == "ED:SerialConnected":
        DeployerConnected = True
    elif string == "ED:SerialDisconnected":
        DeployerConnected = False
        DeployerEnabled = False
        #should we command the switch to be turned off
        processMessage("PE:switchOffDeployer")


def GPSInterpreter(string):
    pass


def PowerInterpreter(string):
    global DeployerEnabled
    global DeployerConnected
    global GPSantennaEnabled
    global GPSenabled
    global DeployerCheck
    if string == "EP:DeployerOn":
        DeployerEnabled = True
        DeployerCheck = True
    elif string == "EP:DeployerOff":
        DeployerEnabled = False
        DeployerConnected = False
        DeployerCheck = True
    elif string == "EP:GPSOn":
        GPSenabled = True
    elif string == "EP:GPSOff":
        GPSenabled = False
    elif string == "EP:AntennaOn":
        GPSantennaEnabled = True
    elif string == "EP:AntennaOff":
        GPSantennaEnabled = False


def RFM22BInterpreter(string):
    if "ER:Done:" in string:
        processMessage("CE" + string[2:])



def processMessage(string):
    thread_char = string[0]
    subsystem_char = string[1]
    if thread_char == 'E':
        # include error handling for if subsystem char is not one of the items in the dictionary
        interpretMessage[subsystem_char](string)
        # how/where to update deploy state?
    else:
        # include error handling for if the thread char is not one of the items in the dictionary
        print("sending to thread: " + string)

        routeMessage[thread_char].put(string)



start_time = time.time()

EPSSemaphore = BoundedSemaphore(1)
ADCSemaphore = BoundedSemaphore(1)
ListSemaphore = BoundedSemaphore(1)
DownlinkSemaphore = BoundedSemaphore(1)

EPSSemaphore.acquire(blocking=False)
ADCSemaphore.acquire(blocking=False)

# setup threads and thread communication
inputQueue = Queue.Queue()  # E
Deployer = DeploymentThread(inputQueue)  # D
Power = EPSThread(inputQueue, EPSSemaphore)  # P
Comm = GlobalstarThread(inputQueue, ListSemaphore, DownlinkSemaphore)  # C
RFM22B = RFM22BThread(inputQueue, ListSemaphore, DownlinkSemaphore)  # R
ADC = ADCThread(inputQueue, ADCSemaphore)  # A

# logging setup
logging.basicConfig(stream=sys.stdout, level=logging.INFO, format="%(asctime)s.%(msecs)03d:%(name)s:%(message)s",
                    datefmt='%Y-%m-%d,%H:%M:%S')
logger = logging.getLogger("main")

routeMessage = {'A': ADC.inputQueue, 'C': Comm.inputQueue, 'D': Deployer.inputQueue,
                'P': Power.inputQueue, 'R': RFM22B.inputQueue}
interpretMessage = {'A': ADCInterpreter, 'C': CommInterpreter, 'D': DeployerInterpreter,
                    'P': PowerInterpreter, 'R': RFM22BInterpreter}
ADC.resume()
Comm.resume()
Deployer.resume()
Power.resume()
RFM22B.resume()

#enable everything before functional test
FunctionalTest()
#disable everything after functional test?

# wd = open("/dev/watchdog", "w+")

WaitFifteen = True
WaitThirty = True
queueEmpty = False
while WaitThirty is True:
    elapsed_time = int(time.time() - start_time)
    print("Time since initialization of Flight Computer: " + str(elapsed_time))
    while queueEmpty is False:
        try:
            threadResponse = inputQueue.get(False)
            processMessage(threadResponse)
        except Queue.Empty:
            queueEmpty = True
    if(elapsed_time >= FIFTEEN_MINUTES):
        if(WaitFifteen == True):
            #START BDOT FOR TWO ORBITS
            processMessage("AE:TwoOrbitBDOT")
            WaitFifteen = False
            #start_time = time.time()
        if(elapsed_time >= THIRTY_MINTUES):
            WaitThirty=False
            break
    time.sleep(60)

BDOTstart_time = time.time()-15
processMessage("PE:switchOnGPS")
processMessage("PE:switchOnAntenna")
GPStimeout = 10
GPSstart_time = time.time()
GPSnow = time.time() - GPSstart_time
while GPSenabled is False and GPSantennaEnabled is False and GPSnow < GPStimeout:
    try:
        threadResponse = inputQueue.get(False)
        processMessage(threadResponse)
    except Queue.Empty:
        pass
    GPSnow = time.time() - GPSstart_time
processMessage("CE:EnableGlobalstar")
while GlobalstarEnabled is False:
    try:
        threadResponse = inputQueue.get(False)
        processMessage(threadResponse)
    except Queue.Empty:
        pass
processMessage("CE:HelloBU") #add health info to this first downlink message?
healthPoll()

GlobalstarStart_Time = time.time()
BDOTelapsed_time = time.time() - BDOTstart_time
GlobalstarElapsed_time = int(time.time() - GlobalstarStart_Time)
while GroundContact is False:
    BDOTelapsed_time = int(time.time() - BDOTstart_time)
    GlobalstarElapsed_time = int(time.time() - GlobalstarStart_Time)
    print("Time since BDOT enabled: " + str(BDOTelapsed_time))
    print("Time since message downlinked to ground: " + str(GlobalstarElapsed_time))
    queueEmpty = False
    while queueEmpty is False:
        try:
            threadResponse = inputQueue.get(False)
            processMessage(threadResponse)
        except Queue.Empty:
            queueEmpty = True
    if(BDOTelapsed_time >= TWO_ORBIT):
        #START BDOT FOR TWO ORBITS
        processMessage("AE:TwoOrbitBDOT")
        BDOTstart_time = time.time()
    time.sleep(60)

while EndOfLife is False:
    GlobalstarElapsed_time = int(time.time() - GlobalstarStart_Time)
    print("Time since message downlinked to ground: " + str(GlobalstarElapsed_time))
    queueEmpty = False
    while queueEmpty is False:
        try:
            threadResponse = inputQueue.get(False)
            processMessage(threadResponse)
        except Queue.Empty:
            queueEmpty = True

logger.info("After calling terminate on threads")
sys.exit(0)
