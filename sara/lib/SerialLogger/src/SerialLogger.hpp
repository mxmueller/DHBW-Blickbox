#ifndef SerialLogger_HPP
#define SerialLogger_HPP

#include <Arduino.h>
namespace serial_communication{

  /**
   * Adds structure for switching between commands and arguments 
   */

  enum RequestPattern{
    COMMAND,
    ARGUMENT
  };
  
  extern RequestPattern CurrentPattern;
  extern String command;


  extern String inputString;

  /**
   * @brief Speichert ob der String fertig verarbeitet wurde
   * 
   */
  extern bool stringComplete;  // whether the string is complete

  /**
   * Eventhandler für Daten die über die Serielle Schnittstelle empfangen wurden
  */
  void on_serial_message_recieved();


}

namespace Debugger{

  enum DebugLevels{
    NONE,
    ERROR,
    WARNING,
    INFO,
    DEBUG,
  };

  String state_to_string(DebugLevels state);

  void log(String message, DebugLevels level);
}

class SerialLogger {
public:
  SerialLogger(){};
  void set_debug_level(Debugger::DebugLevels level);
  Debugger::DebugLevels get_debug_level();
  void log(String message, Debugger::DebugLevels level);  
  void begin();
  static void serialHandler(int argCnt, char **args);
  static SerialLogger *p_serial_logger;
private:
    Debugger::DebugLevels debug_level = Debugger::NONE;
};

#endif  // SerialLogger_HPP

