[MAX]
# distance from the end of the "reference tool" (tool-length - 0) to the
# center of the head tilt axis
B_PIVOT_LENGTH = 0


[DISPLAY]
DISPLAY           = axis 
CYCLE_TIME        = 0.200
POSITION_OFFSET   = RELATIVE
POSITION_FEEDBACK = ACTUAL
MAX_FEED_OVERRIDE = 2.0
PROGRAM_PREFIX    = ../../nc_files/
INTRO_GRAPHIC     = linuxcnc.gif
INTRO_TIME        = 5
EDITOR            = gedit

[RS274NGC]
PARAMETER_FILE = max5triv.var

[EMCMOT]
EMCMOT       = motmod
COMM_TIMEOUT = 1.0
COMM_WAIT    = 0.010
SERVO_PERIOD = 1000000

[TASK]
TASK =                  milltask
CYCLE_TIME =            0.010

[TRAJ]
COORDINATES =           X Y Z B C
LINEAR_UNITS =          1.0
ANGULAR_UNITS =         1.0
CYCLE_TIME =            0.010
DEFAULT_VELOCITY =      200.0
MAX_VELOCITY =          346.0
MAX_ACCELERATION =      800.0
DEFAULT_ACCELERATION =  800.0
TLO_IS_ALONG_W =          0

[EMCIO]
EMCIO      = io
CYCLE_TIME = 0.100
TOOL_TABLE = max5.tbl

[AXIS_X]
MIN_LIMIT = -100
MAX_LIMIT = 100
MAX_VELOCITY = 20.0
MAX_ACCELERATION = 100.0

[JOINT_0]
# this is the table
TYPE =               LINEAR
HOME =               0.000
MAX_VELOCITY =       20.0
MAX_ACCELERATION =   100.0
BACKLASH =           0.000
#INPUT_SCALE =       1000  
#OUTPUT_SCALE =      1.000
MIN_LIMIT =          -100
MAX_LIMIT =          100
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        101.0
HOME_SEARCH_VEL =    20.0
HOME_LATCH_VEL =     5.0
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = YES
HOME_SEQUENCE =                 1

[AXIS_Y]
MIN_LIMIT =        -60
MAX_LIMIT =         60
MAX_VELOCITY =      20.0
MAX_ACCELERATION = 100.0

[JOINT_1]
# this is the saddle
TYPE =               LINEAR
HOME =               0.000
MAX_VELOCITY =       20.0
MAX_ACCELERATION =   100.0
BACKLASH =           0.000
#INPUT_SCALE =       4000 
#OUTPUT_SCALE =      1.000 
MIN_LIMIT =          -60
MAX_LIMIT =          60
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        -61
HOME_SEARCH_VEL =    -20
HOME_LATCH_VEL =     -3
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = YES
HOME_SEQUENCE =      1

[AXIS_Z]
MIN_LIMIT =       -149.0
MAX_LIMIT =          1.0
MAX_VELOCITY =      20.0
MAX_ACCELERATION = 100.0

[JOINT_2]
# this is the head moving up and down the column
TYPE =               LINEAR
HOME =               0.000
MAX_VELOCITY =       20.0
MAX_ACCELERATION =   100.0
BACKLASH =           0.000
#INPUT_SCALE =       4000
#OUTPUT_SCALE =      1.000
MIN_LIMIT =          -149.0
MAX_LIMIT =          1.0
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        2.0
HOME_SEARCH_VEL =    20.0
HOME_LATCH_VEL =     5.0
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = YES
HOME_SEQUENCE =      0

[AXIS_A]
MIN_LIMIT =        -10.0
MAX_LIMIT =         10.0
MAX_VELOCITY =      45.0
MAX_ACCELERATION = 100.0

[JOINT_3]
TYPE =               ANGULAR
HOME =               0.000
MAX_VELOCITY =       45.0
MAX_ACCELERATION =   100.0
BACKLASH =           0.000
#INPUT_SCALE =       4000
#OUTPUT_SCALE =      1.000
MIN_LIMIT =          -10.0
MAX_LIMIT =          10.0
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        0.0
HOME_SEARCH_VEL =    0.0
HOME_LATCH_VEL =     0.0
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = NO
HOME_SEQUENCE =      0

[AXIS_B]
MIN_LIMIT =        -90.0
MAX_LIMIT =         90.0
MAX_VELOCITY =      45.0
MAX_ACCELERATION = 225.0

[JOINT_4]
# this is the head tilting side to side
TYPE =               ANGULAR
HOME =               0.000
MAX_VELOCITY =       45.0
MAX_ACCELERATION =   225.0
BACKLASH =           0.000
#INPUT_SCALE =       4000
#OUTPUT_SCALE =      1.000
MIN_LIMIT =          -90.0
MAX_LIMIT =          90.0
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        91.0
HOME_SEARCH_VEL =    25.0
HOME_LATCH_VEL =     3.0
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = YES
HOME_SEQUENCE =      1

[AXIS_C]
MIN_LIMIT =      -3600.0
MAX_LIMIT =       3600.0
MAX_VELOCITY =      45.0
MAX_ACCELERATION = 225.0

[JOINT_5]
# this is a rotary table sitting on the main table
TYPE =               ANGULAR
HOME =               0.000
MAX_VELOCITY =       45.0
MAX_ACCELERATION =   225.0
BACKLASH =           0.000
#INPUT_SCALE =       4000
#OUTPUT_SCALE =      1.000
MIN_LIMIT =          -3600.0
MAX_LIMIT =          3600.0
FERROR =             2.000
MIN_FERROR =         0.200
HOME_OFFSET =        0.0
HOME_SEARCH_VEL =    20.0
HOME_LATCH_VEL =     3.0
HOME_USE_INDEX =     NO
HOME_IGNORE_LIMITS = NO
HOME_SEQUENCE =      1