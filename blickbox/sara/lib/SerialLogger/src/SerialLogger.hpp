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
  
  /**
   * @brief Hält das aktuelle Pattern während der Verarbeitung
   * 
   */
  extern RequestPattern CurrentPattern;

  /**
   * @brief Enthält das Kommando
   * 
   */
  extern String command;

  /**
   * @brief Hällt den empfangenen String
   * 
   */
  extern String inputString;

  /**
   * @brief Speichert ob der String fertig verarbeitet wurde
   * 
   */
  extern bool stringComplete;  // whether the string is complete

  /**
   * @brief Verwaltet eingehende Bytes der Seriellen Schnittstelle
   *  sollte im Hauptprogramm ausgeführt werden
   * 
   */
  void handle_serial_message_recieved();


}

namespace debugger{

    /**
     * @brief Definiert Debuglevel um ausgaben zu definieren
     * 
     */
    enum DebugLevels{
      NONE,
      ERROR,
      WARNING,
      INFO,
      DEBUG,
    };

    /**
     * @brief Wandelt ein Debuglevel in einen String um
     * 
     * @param state 
     * @return String 
     */
    String state_to_string(DebugLevels state);

}

namespace serial_logger{
    using namespace debugger;

    /**
     * @brief speichert das globale Loglevel
     * 
     */
    extern DebugLevels level;

    /**
     * @brief Setzt das globale debuglevel
     * 
     * @param level 
     */
    void set_debug_level(DebugLevels level);

    /**
     * @brief Gibt das globale debuglevel zurück
     * 
     * @return DebugLevels 
     */
    DebugLevels get_debug_level();

    /**
     * @brief log die definierte message auf der Seriellen Konsole
     * Mit dem Level definiert um welche Art von Nachricht es sich handelt.
     * 
     * @param message 
     * @param level 
     */
    void log(String message, DebugLevels level);  
}

#endif  // SerialLogger_HPP

