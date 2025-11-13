#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <fstream>
#include <vector>
#include <cstdint>
#include <string>

namespace py = pybind11;


std::string getFileName(uint8_t fileNum, const std::string& filePath)
{
    // Function which returns a file path based on a given file number
    uint8_t folderNum = fileNum/10;
    fileNum %= 10;

    if (folderNum == 0) 
        return filePath + "/../drug_data/otc_drugs/otc-"+std::to_string(fileNum)+".json";
    else if (folderNum == 1) 
        return filePath + "/../drug_data/prescription_drugs/prescription-"+std::to_string(fileNum)+".json";

    return "Folder Index Out Of Bounds\n";
}


std::string getDrugEntry(uint8_t fileNum, uint32_t bytePos, const std::string& appAbsPath)
{
    std::string fileName = getFileName(fileNum, appAbsPath);
    std::string jsonString;

    // Open the file in binary
    std::ifstream file(fileName, std::ios::binary);
    if (!file) return jsonString;
    file.seekg(bytePos);
    
    std::string line;
    while (std::getline(file, line) && line.size() >= 4) {
        
        if (line.back() == '\r') line.pop_back();
        if (line.size() > 3 && line[3] == ',') line.erase(3, 1);
        
        // For every line, append it to the jsonString
        jsonString.append(line);

        // A '}' char at line[2] indicates the end of the drug entry
        if (line[2] == '}') break;
    }

    return jsonString;
}


PYBIND11_MODULE(data_reader, m) {
    m.def("get_filename", &getFileName);
    m.def("get_drug_entry", &getDrugEntry);
}