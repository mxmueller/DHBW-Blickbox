#include <SerialLogger.hpp>

SerialLogger *SerialLogger::p_serial_logger = nullptr;


void SerialLogger::serialHandler(int argCnt, char **args){
  if(p_serial_logger != nullptr){
    if(strcmp(args[1], "g") == 0){
        Serial.print(Debugger::state_to_string(p_serial_logger->get_debug_level()));
    }else if (strcmp(args[1], "d") == 0){
        p_serial_logger->set_debug_level(Debugger::DEBUG);
        Serial.println(F("Debug"));
    }else if (strcmp(args[1], "n") == 0){
        p_serial_logger->set_debug_level(Debugger::NONE);
        Serial.println(F("None"));
    }else if (strcmp(args[1], "e") == 0){
        p_serial_logger->set_debug_level(Debugger::ERROR);
        Serial.println(F("Error"));
    }else if (strcmp(args[1], "w") == 0){
        p_serial_logger->set_debug_level(Debugger::WARNING);
        Serial.println(F("Warning"));
    }else if (strcmp(args[1], "i") == 0){
        p_serial_logger->set_debug_level(Debugger::INFO);
        Serial.println(F("Info"));
    }
  }else{
    Serial.println(F("SerialLogger not initialized"));
  }
}

void SerialLogger::begin(){
    p_serial_logger = this;
}

void SerialLogger::log(String message, Debugger::DebugLevels level){
    if(debug_level > Debugger::NONE){
        switch (level)
        {
        case Debugger::DEBUG:
            Serial.print(F("[DEBUG] "));
            Serial.println(message);
            break;
        case Debugger::ERROR:
            Serial.print(F("[Error] "));
            Serial.println(message);
            break;
        case Debugger::WARNING:
            Serial.print(F("[Warning] "));
            Serial.println(message);
            break;
        case Debugger::INFO:
            Serial.print(F("[INFO] "));
            Serial.println(message);
            break;
        
        default:
            break;
        }
    }
}

Debugger::DebugLevels SerialLogger::get_debug_level(){
    return debug_level;
}

void SerialLogger::set_debug_level(Debugger::DebugLevels level){
    debug_level = level;
}

namespace Debugger {
    String state_to_string(DebugLevels state){
        switch (state) {
        case NONE:
            return F("NONE");
            break;
        case ERROR:
            return F("ERROR");
            break;
        case WARNING:
            return F("WARNING");
            break;
        case INFO:
            return F("INFO");
            break;
        case DEBUG:
            return F("DEBUG");
            break;
        }
        return F("UNKNOWN");
    }

    void log(String message, DebugLevels level){
        if(SerialLogger::p_serial_logger != nullptr){
            SerialLogger::p_serial_logger->log(message, level);
        }
    }
}

namespace SerialCommunication{
    RequestPattern CurrentPattern = COMMAND;
    String command = "";

    String inputString = "";      // a String to hold incoming data
    bool stringComplete = false;  // whether the string is complete

    void Handle_Serial_Request(){
        while (Serial.available()) {
            // get the new byte:
            char inChar = (char)Serial.read();
            
            if (inChar == '\n' || inChar == '\r') {
                
                stringComplete = true;
                CurrentPattern = COMMAND;
                return;
            }

            // add it to the inputString:
            inputString += inChar;

            // if the incoming character is a newline, set a flag so the main loop can
            // do something about it:
            switch (CurrentPattern)
            {
                case COMMAND:
                command += inChar;
                if(inChar == ' '){
                CurrentPattern = ARGUMENT;
                }
                break;
            }

            
        }
    }
}
