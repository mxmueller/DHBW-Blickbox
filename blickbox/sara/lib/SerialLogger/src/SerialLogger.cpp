#include <SerialLogger.hpp>
namespace serial_logger{

    using namespace debugger;

    DebugLevels level = DebugLevels::DEBUG;

    void log(String message,DebugLevels level){
        if(level > NONE){
            switch (level)
            {
            case DEBUG:
                Serial.print(state_to_string(DEBUG));
                Serial.print(F(":"));
                Serial.println(message);
                break;
            case ERROR:
                Serial.print(state_to_string(ERROR));
                Serial.print(F(":"));
                Serial.println(message);
                break;
            case WARNING:
                Serial.print(state_to_string(WARNING));
                Serial.print(F(":"));
                Serial.println(message);
                break;
            case INFO:
                Serial.print(state_to_string(INFO));
                Serial.print(F(":"));
                Serial.println(message);
                break;
            
            default:
                break;
            }
        }
    }

    DebugLevels get_debug_level(){
        return level;
    }

    void set_debug_level(DebugLevels level){
        level = level;
    }

}



namespace debugger {
    String state_to_string(DebugLevels state){
        switch (state) {
        case NONE:
            return F("none");
            break;
        case ERROR:
            return F("error");
            break;
        case WARNING:
            return F("warning");
            break;
        case INFO:
            return F("info");
            break;
        case DEBUG:
            return F("debug");
            break;
        }
        return F("UNKNOWN");
    }

}

namespace serial_communication{
    RequestPattern CurrentPattern = COMMAND;
    String command = "";

    String inputString = "";      // a String to hold incoming data
    bool stringComplete = false;  // whether the string is complete

    void handle_serial_message_recieved(){
        if (Serial.available()) {
            char inChar = (char)Serial.read();
            
            if (inChar == '\n' || inChar == '\r') {
                
                stringComplete = true;
                CurrentPattern = COMMAND;
                return;
            }

            inputString += inChar;

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
