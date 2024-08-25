#include <mock/SerialLoggerMock.hpp>
namespace serial_logger{

    using namespace debugger;

    DebugLevels level = DebugLevels::DEBUG;

    /**
     * @brief Logs a Message with a Debug level
     * 
     * @param message 
     * @param level 
     */
    void log(String message, DebugLevels level){
        if(level > NONE){
            switch (level)
            {
            case DEBUG:
                std::cout << state_to_string(DEBUG) << " : " << message << std::endl;
                break;
            case ERROR:
                std::cout << state_to_string(ERROR) << " : " << message << std::endl;
                break;
            case WARNING:
                std::cout << state_to_string(WARNING) << " : " << message << std::endl;
                break;
            case INFO:
                std::cout << state_to_string(INFO) << " : " << message << std::endl;
                break;
            
            default:
                break;
            }
        }
    }

    /**
     * @brief Logs a Message with prefix 
     * 
     * @param prefix 
     * @param message 
     */
    void log(String prefix, String message){
        std::cout << prefix << " " << message << std::endl;
    }

    /**
     * @brief Logs a Message
     * 
     * @param message 
     */
    void log(String message){
        std::cout << message << std::endl;
    }
    /**
     * @brief Logs a Message
     * 
     * @param message 
     */
    void log(uint16_t number){
        std::cout << number << std::endl;
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
            return "none";
            break;
        case ERROR:
            return "error";
            break;
        case WARNING:
            return "warning";
            break;
        case INFO:
            return "info";
            break;
        case DEBUG:
            return "debug";
            break;
        }
        return "UNKNOWN";
    }

}

namespace serial_communication{
    RequestPattern CurrentPattern = COMMAND;
    String command = "";

    String inputString = "";      // a String to hold incoming data
    bool stringComplete = false;  // whether the string is complete

    void handle_serial_message_recieved(){
        // if (Serial.available() > 0) {
        //     char inChar = (char)Serial.read();
            
        //     if (inChar == '\n' || inChar == '\r') {
                
        //         stringComplete = true;
        //         CurrentPattern = COMMAND;
        //         return;
        //     }

        //     inputString += inChar;

        //     switch (CurrentPattern)
        //     {
        //         case COMMAND:
        //         command += inChar;
        //         if(inChar == ' '){
        //         CurrentPattern = ARGUMENT;
        //         }
        //         break;
        //     }
        // }
    }   

}
