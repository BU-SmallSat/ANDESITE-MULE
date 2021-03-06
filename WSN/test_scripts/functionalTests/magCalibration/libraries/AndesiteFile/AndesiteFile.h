// -*-c++-*-
// **********************************************************************************
// 
// Name:    AndesiteFile.h
// Class:   <AndesiteFile>
// Author:  Gabriel Gonzalez
// 
// Description: The skeleton for writing and storing data on the ANDESITE Satellite.
//              
// Notes: None.
// 
// **********************************************************************************


// ============
// Header guard
// ============

#ifndef ANDESITEFILE_H
#define ANDESITEFILE_H

// Includes
#include "Arduino.h"
#include <RF22Mesh.h>
#include <SdFat.h>

// =======
// Classes
// =======

class AndesiteFile {
public:
    AndesiteFile();
    
    // Initialize the orbit file, start the data file on the correct orbit
    boolean       init();
    
    // Send the data file to the Mule
    boolean       send();
    
    // Send a done message to the Mule, inicating done sending file
    void          done();
    
    // Append the specified data to the string that will eventually be written to the file
    void          store(String str);
    
    // Write user defined string to the data file
    void          write(bool done);
    
    // Write the stored data string to the file
    void          write();
    
    // Check size of stored data string and see if it has reached its max length
    boolean       status();
    
    // Set the file name from the current orbit
    void          set();
    
    // Return name of file
    String        name() { return _file; }
    
    // Return the size of the data file
    unsigned long size();
    
    // Return the orbit as an actual value (not a string) (I think I can do this with just
    //   _file.toInt() but I'm not sure
    unsigned int  orbit();

    
    unsigned int        _ready_write_bool;
	File                _handle;
	String              _file;
private:
    
    // Converts an orbit number to a file name
    String strOrbitFile(unsigned int orb);
    
    // Search throught the SD card root directory and count the number of files 
    //   (where files equates to orbits)
    unsigned int getNumberOfFiles();
    
    // NOT FINISHED IMPLEMENTING! DOES NOT WORK AS EXECPTED
    // Find the last files that did not finish sending their data to the Mule
    void setUnfinishedFiles();
    
    // Variables
    
    char                _transmit_message[RF22_MESH_MAX_MESSAGE_LEN];
    ifstream::pos_type  _file_position;
    String              _collected_data;
    String              _writing_data;
    String              _str_parity;
    unsigned int        _int_parity;
    unsigned int        _file_open_bool;
    unsigned int        _message_size;
    unsigned int        _num_files;
    unsigned int        _num_unfinished_files;
    unsigned int        _last_orbit;
    unsigned int        _start_orbit;
    unsigned int        _failure;
    unsigned int        _data_limit;
    unsigned int        _header_size;
    unsigned int        _unfinished_files_size;
    unsigned int        _unfinished_files_arr[5];
};



// =======
// Globals
// =======

extern AndesiteFile _File;

#endif
