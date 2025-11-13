#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <string>


bool is_bullet(const char32_t& ch)
{
    // Switch statement ontains unicode characters written in hexidecimal
    // These unicode symbols may serve as a bullet point in the data set
    
    switch (ch) {
        case 0x2022: case 0x2023: case 0x25E6: case 0x2981: case 0x25CF: case 0x25AA: case 0x25AB: case 0x25FC:
        case 0x25A0: case 0x2713: case 0x2714: case 0x2794: case 0x279C: case 0x2792: case 0x279E: case 0x27A0:
        case 0x27A4: case 0x27A5: case 0x27A6: case 0x27A7: case 0x27A8: case 0x27A9: case 0x27AA: case 0x27AB:
        case 0x27AC: case 0x27AD: case 0x27AE: case 0x27AF: case 0x27B1: case 0x27B2: case 0x27B3: case 0x27B5:
        case 0x27B8: case 0x27BB: case 0x27BC: case 0x00B7: case 0x2027: case 0x30FB:
            return true;
        default:
            return false;
    }
}


bool is_numberBullet(const std::u32string& line, size_t i)
{
    // Method which returns true if the next sequence of characters matches a number bullet pattern
    // number bullet pattern example: " 1. " or " 10. "

    if (i == 0 || line[i-1] != U' ') return false;

    size_t j = i;
    if (line[j] < U'0' || line[j] > U'9') return false;

    while (j < line.size() && line[j] >= U'0' && line[j] <= U'9') ++j;
    
    if (j+2 < line.size() && line[j] == U'.' && line[j+1] == U' ') return true;
    else return false;
}


// This function inserts line breaks in a line when it encounters bullets
std::u32string insertLineBreaks(const std::u32string& line)
{
    std::u32string newLine;

    // Loop through all characters in the string
    for (size_t i = 0; i < line.size(); i++) {
        // If the character can be used as a bullet, place a \n character before it
        if (is_bullet(line[i]) || is_numberBullet(line, i))
            newLine.push_back(U'\n');

        newLine.push_back(line[i]);
    }

    return newLine;
}


PYBIND11_MODULE(line_breaker, m) {
    m.def("insert_linebreaks", &insertLineBreaks);
}