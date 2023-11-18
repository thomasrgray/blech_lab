from pyControl.utility import *
from devices import *
import hardware_definition as hw  # Assuming you have a hardware_definition module

nose = Nosepoke(board.port_1, nose_event="poke")
#-------------------------------------------------------------------------
# States and events.
#-------------------------------------------------------------------------

states = ['init_trial',
          'vacuum_on',
          'odor_on',
          'wait_for_water',
          'water_on',
          'inter_trial_interval']

events = ['center_poke',
          'vacuum_timer',
          'odor_timer',
          'water_timer',
          'session_timer']

initial_state = 'init_trial'


#-------------------------------------------------------------------------
# Variables.
#-------------------------------------------------------------------------

v.vacuum_duration = 2 * second
v.odor_duration = 2 * second
v.water_duration = 0.01 * second
v.ITI_duration = 90 * second
v.hold_threshold = 1.5 * second
#-------------------------------------------------------------------------        
# State machine code.
#-------------------------------------------------------------------------

def run_start():
    set_timer('session_timer', 45 * minute)  # Set an overall session timer.

def run_end():
    hw.off()  # Turn off all hardware outputs.

def init_trial(event):
    if event == 'entry':
        nose.LED.on()
        print(f"hold for {v.hold_threshold} seconds to go to state A")
    elif event == "poke_in":
        set_timer("hold_timer_done", v.hold_threshold * second, output_event=True)
        nose.LED.off()
    elif event == "poke_out":
        disarm_timer("hold_timer_done")
        nose.LED.on()
    elif event == "hold_timer_done":
        goto_state("vacuum_timer")
        set_timer("hold_timer_done", v.hold_threshold * second, output_event=True)
    
def vacuum_timer(event):
    if event == 'hold_timer_done'
        hw.solenoidC.SOL.on()
        set_timer('vacuum_timer', v.vacuum_duration)
        goto_state('vacuum_on')

def vacuum_on(event):
    if event == 'vacuum_timer':
        hw.solenoidC.SOL.off()
        set_timer('odor_timer', 0.2 * second)
        goto_state('odor_on')

def odor_on(event):
    if event == 'odor_timer':
        hw.solenoidA.SOL.on()
        hw.activate_intan_input(hw.PINS['odor_intan_pin'])  # Signal marking start of odor solenoid
        set_timer('odor_timer', v.odor_duration)
        goto_state('wait_for_water')

def wait_for_water(event):
    if event == 'odor_timer':
        hw.solenoidA.SOL.off()
        hw.deactivate_intan_input(hw.PINS['odor_intan_pin'])
        goto_state('inter_trial_interval')

def water_on(event):
    if event == 'water_timer':
        hw.solenoidB.SOL.on()  # Activate the water solenoid
        set_timer('water_off_timer', v.water_duration)  
        goto_state('wateroff_timer')

def water_off_timer(event):
    if event == 'water_off_timer':
        hw.solenoidB.SOL.off()  # Deactivate the water solenoid
        goto_state('inter_trial_interval')

def inter_trial_interval(event):
    if event == 'entry':
        set_timer('session_timer', v.ITI_duration)
    elif event == 'session_timer':
        goto_state('init_trial')

# State independent behavior.
def all_states(event):
    if event == 'session_timer':
        stop_framework()

# Define the hardware.
def hardware_definition():
    # You should define your hardware setup here.
    # This includes solenoids, LEDs, and any other peripherals used in the task.
    pass
