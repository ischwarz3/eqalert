"""
eqalert key processor
"""

import curses
import time

import eqa_settings
import eqa_struct

def process(display_q, sound_q, keyboard_q, heal_q, damage_q, message_q, exit_flag, heal_parse, spell_parse, raid):
  """Process Key press events"""

  key = ''
  page = 'events'

  while key != ord('q') and key != 27 and not exit_flag.is_set():

    try:
      # Get key
      time.sleep(0.001)
      if not keyboard_q.empty():
        key = keyboard_q.get()
        keyboard_q.task_done()

        # Handle resize event
        if key == curses.KEY_RESIZE:
          display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'redraw', 'null'))

        # Handle tab keys
        if key == curses.KEY_F1:
          display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'events', 'null'))
          page = 'events'
        if key == curses.KEY_F2:
          display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'state', 'null'))
          page = 'state'
        if key == curses.KEY_F3:
          display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'settings', 'null'))
          page = 'settings'
        if key == curses.KEY_F4:
          display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'help', 'null'))
          page = 'help'

        # Events keys
        if page == 'events':
          if key == ord('c'):
            display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'event', 'clear', 'null'))
          if key == ord('r'):
            if not raid.is_set():
              raid.set()
              display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'event', 'events', 'Raid mode enabled'))
              sound_q.put(eqa_struct.sound('espeak', 'Raid mode enabled'))
            elif raid.is_set():
              raid.clear()
              display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'event', 'events', 'Raid mode disabled'))
              sound_q.put(eqa_struct.sound('espeak', 'Raid mode disabled'))
            display_q.put(eqa_struct.display(eqa_settings.eqa_time(), 'draw', 'events', 'null'))

        # State keys
        elif page == 'state':
          pass

        # Settings keys
        elif page == 'settings':
          pass

        # Help keys
        elif page == 'help':
          pass

    except Exception as e:
      eqa_settings.log('process keys: ' + str(e))
      exit_flag.set()
      pass

  exit_flag.set()


def read(exit_flag, keyboard_q, screen_obj):
  """Check dem keys"""
  key = ''
  while key != ord('q') and key != 27:
    key = screen_obj.getch()
    keyboard_q.put(key)
  exit_flag.set()
