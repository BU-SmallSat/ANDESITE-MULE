// **********************************************************************************
// 
// Name:    AndesiteOrbit.cpp
// Class:   <AndesiteOrbit>
// Author:  Gabriel Gonzalez
// 
// Description: Controls information regarding the satellite orbit.
//              
// Notes: None.
// 
// **********************************************************************************


// ========
// Includes
// ========

// Includes
#include "AndesiteOrbit.h"
#include "AndesiteData.h"
#include "AndesiteRadio.h"
#include "libandesite.h"



// ////////////////////////////////
// ///// ANDESITE ORBIT CLASS /////
// ////////////////////////////////

// Initialize Andesite Orbit class
AndesiteOrbit::AndesiteOrbit() {
    _latitude        = 0;
    _lat_mode_switch = 65;
    
    _dl            = 0;          // [deg] (dv*dt/radius * 180/pi)
    _dt            = 0;          // [ms]
    _dv            = 7.5/1000.0; // [km/s]
    _radius        = 6371+525;   // [km]
    
    _orbit         = 1;
    _position      = 0;
    _status        = 0;
    
    _timeout       = 1000;
    _update_fail   = 0;
}



// //////////////////////////
// ///// ORBIT LATITUDE /////
// //////////////////////////

// Determine and set the orbit latitude
boolean AndesiteOrbit::setLatitude() {
    unsigned long timer_start = millis();
	
	// Read in data from the serial port
	while (1) {
        
		while ( Serial1.available() > 0 ) {
			char c = Serial1.read();
            
            // Determine latitude and latitude increment
			if ( c > -1 ) {
				if ( GPS.encode(c) ) {
					_latitude = GPS.location.lat();
                    _dt       = millis() - _dt;
                    _dl       = (_dv * _dt) / _radius * 180.0 / (double)3.1415926589;
                    return true;
				}
			}
			
			if ( (millis() - timer_start) >= _timeout ) { break; }
        }
        
		if ( (millis() - timer_start) >= _timeout ) { break; }
    }
    
    // Determine latitude increment
    _dt = millis() - _dt;
    // Change this for testing, make it so that it's dependent on orbit time
    _dl = (_dv * _dt) / _radius * 180.0 / (double)3.1415926589; 
    _latitude += _dl;
    
	return false;
}



// //////////////////////////////////////////
// ///// READ/WRITE TO DATA FILE HEADER /////
// //////////////////////////////////////////

// Return specified field in orbit information file
unsigned long AndesiteOrbit::readHeader(String file, int field) {
    File handle = SD.open(file.c_str(), O_READ);
    size_t loc  = 0;
    char sep    = ',';
    char end    = '|';
    char letter = '\0';
    String str  = "";
    
    // Check that the file opened
    if ( !handle ) {
        Serial.println("Orbit READ was unsuccesful!");
        handle.close();
        return -1;
    }
    
    // Get the specified field from the file
    while ( (handle.available() > 0) && (loc <= field) ) {
        letter = handle.read();
        
        if ( (letter == end) || (str.length() >= 7) )
            break;
        
        if ( letter == sep ) {
            ++loc;
            continue;
        }
        
        if ( (letter <= 0) || (letter == '\r') || (letter == '\n') )
          continue;
        
        if ( (field == loc) )
            str += letter;
    }
    
    // Close file
    handle.close();
    
    return (long)str.toInt();
}



// Set the header of the orbit data file
boolean AndesiteOrbit::writeHeader(File handle) {
    Serial.print("Orbit Info: ");
	Serial.print(_orbit);
    Serial.print(",");
    Serial.print(_position);
    Serial.print(",");
    Serial.println(_status);
    
	if ( !handle ) {
        Serial.println("Orbit WRITE was unsuccesful!");
        return false;
    }
    
    // Write the header of the orbit file
    String buf = zeroPadFields();
    Serial.print("Writing to orbit file, info: ");
    Serial.println(buf);
    
    handle.seek(0);
    handle.print(buf);
    
    return true;
}



// Update orbit file containing value of current orbit
boolean AndesiteOrbit::update(String file) {
    
    // PUT FUNCTION TO OPEN AND CHECK FAILURE IN ANDESITE_FILE
    // Open up orbit info file (check for file open fails globally)
    // File handle;
    // if ( _update_fail > 5 ) 
    //     handle = SD.open(file.c_str(), O_CREAT | O_TRUNC | O_WRITE);
    // else
    //     handle = SD.open(file.c_str(), O_CREAT | O_WRITE); // This should be read?
    
    // // Check status of opened file
	// if ( !handle ) {
    //     Serial.println(":: Unable to update file.");
        
    //     // Stop trying this orbit and go to next orbit
    //     if ( _update_fail > 10 )
    //         ++_orbit;
        
    //     // Opening file has failed, keep track of this        
    //     ++_update_fail;
    //     handle.close();
        
    //     return 0;
    // } else {
        
    //     // Opening file has failed many times, write fresh data to file and be done with it
    //     if ( _update_fail ) {
    //         if ( _update_fail > 5 )
    //             writeHeader(handle);
    //         _update_fail = 0;
    //         header.close();
    //         return 2;
    //     }
    //     header.close();
    // } 
    
    // Check file size, compare with pos and header (header size = (5+7+1)+(2+1) = 16)
    File handle = SD.open(file.c_str(), O_READ);
    if ( !handle ) 
        Serial.println("File not able to be opened (Orbit.update).");
    else {
        Serial.print("Info SIZE = ");
        Serial.println(handle.size());
    }
    
    handle.close();
    
    // Get data file header information
	unsigned int orb  = readHeader(file, 0);
    unsigned long pos = readHeader(file, 1);
    unsigned int stat = readHeader(file, 2);
    
    Serial.print("Info Orb = ");
    Serial.println(orb);
    Serial.print("Info Pos = ");
    Serial.println(pos);
    Serial.print("Info Stat = ");
    Serial.println(stat);
    Serial.println("Done.");
    
	// Setup header variables for next orbit
    if ( stat ) {
        ++_orbit;
        _position = 0;
        _status = 0;
        return true;
    } 
    
    return false;
}



// ///////////////////////
// ///// GPS TESTING /////
// ///////////////////////

// Wait for orbit to finish
boolean AndesiteOrbit::waitOrbitFinish() {
    Serial.println(":: Waiting for orbit to finish...");
    acdh_led_set(1);
    unsigned long timer_start = millis();
    
    // Wait for orbit to finish
	while ( _latitude < _lat_mode_switch ) {
        timer_start = latIntervalPrint(timer_start, 1000);
        
        if ( !setLatitude() ) { Serial.println("GPS Fail."); }
	}
	
	Serial.println("Done.");
	
	// Orbit number peaked and is too big, do nothing
    Serial.print("Max int: ");
    unsigned int maxi = (1 << (8*sizeof(int)-1) );
    Serial.println(maxi);
    
    if ( _orbit >= maxi ) {
        Serial.print("Orbit number is at its max value: ");
        Serial.println(_orbit);
        while ( _orbit >= maxi ) {}
    }
    
    return true;
}



// Wait for Science mode to finish
boolean AndesiteOrbit::waitScienceFinish() {
    Serial.println(":: Waiting for Science Mode to finish...");
    acdh_led_set(1);
    unsigned long timer_start = millis();
    
    // Wait for Science mode to finish
	while ( _latitude >= _lat_mode_switch ) {
        timer_start = latIntervalPrint(timer_start, 1000);
        
		if ( !setLatitude() ) { Serial.println("GPS Fail."); }
	}
	
	Serial.println("Done.");
	
	// Orbit number peaked and is too big, do nothing
    if ( _orbit >= 999 ) {
        Serial.print("Orbit number is at its max value: ");
        Serial.println(_orbit);
        while ( _orbit >= 999 ) {}
    }
    
    return true;
}


// Wait for Transfer mode start signal from Mule
boolean AndesiteOrbit::waitTransferStartCmd() {
    Serial.println(":: Waiting for message from Mule...");
    acdh_led_set(1);
	unsigned long timer_start  = millis();
    unsigned long poll_timer   = millis();
    unsigned long poll_refresh = 1000;
    boolean message_sent       = false;
    
    // Establish communication with Mule to start sending data
    while ( _latitude < _lat_mode_switch ) { 
        
        // Send message to Mule saying done with Science mode
        if ( !message_sent ) {
            if ( !_Radio.send(&_Radio._cmd_start, sizeof(uint8_t), ACDH_MULE_ADDR) ) 
                Serial.println("Send Fail.");
            else
                message_sent = true;
        }
        
        // Wait for command from Mule to start sending data to it
        if ( message_sent ) {
            if ( _Radio.listen() == ACDH_MULE_ADDR ) {
                Serial.println("Done.");
                return true;
            }
        }
        
		timer_start = latIntervalPrint(timer_start, 1000); // Maybe sec should not be same
        
		// GPS string poll (maybe add a timer here if necessary)
        if ( (millis() - poll_timer) >= poll_refresh ) {
            if ( !setLatitude() ) { Serial.println("GPS Fail."); }
            poll_timer = millis();
        }
    }
	
    Serial.println("Going back to Science mode.");
    
    return false;
}




// ///////////////////
// ///// UTILITY /////
// ///////////////////

// Zero pad the data file header fields
String AndesiteOrbit::zeroPadFields() {
    String part1      = String(_orbit);
    String part2      = String(_position);
    String part3      = String(_status);
    unsigned int  orb = _orbit;
    unsigned long pos = _position;
    
    // Set initial values (on first run)
    if ( orb == 0 ) { orb = 1; }
    if ( pos == 0 ) { pos = 1; }
    
    // Zero pad the fields
    while ( (orb=orb*10) < 1e3 ) { part1 = "0" + part1; }
    while ( (pos=pos*10) < 1e7 ) { part2 = "0" + part2; }
    
    return (part1 + "," + part2 + "," + part3 + "|");
}



// Print the latitude at the given time interval
unsigned long AndesiteOrbit::latIntervalPrint(unsigned long now, int interval) {
    if ( (millis() - now) >= interval ) {
        Serial.print("Latitude = ");
        Serial.println(_latitude);
        now = millis();
    }
    
    return now;
}
