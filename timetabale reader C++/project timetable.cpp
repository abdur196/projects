#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <regex>
#include <cctype> 

using namespace std;

class tt {
public:
    string start;
    string coursename;
    string section;
    tt* next;

    tt() : start(""), coursename(""), section(""), next(nullptr) {}
};

class room {
public:
    string name;
    tt* classes;

    room() : name(""), classes(nullptr) {}

    ~room() {
        tt* current = classes;
        while (current != nullptr) {
            tt* temp = current;
            current = current->next;
            delete temp;
        }
    }
};

class days {
public:
    string day;
    room* ROOM[50];

    days() {
        for (int i = 0; i < 50; i++) {
            ROOM[i] = new room();
        }
    }

    ~days() {
        for (int i = 0; i < 50; i++) {
            delete ROOM[i];
        }
    }
};

class timetable {
public:
    days* d[6];
    const string timeSlots[7] = {
        "8:30-9:50", "10:00-11:20", "11:30-12:50",
        "1:00-2:20", "2:30-3:50", "4:00-5:20", "5:30-6:50"
    };

    timetable() {
        const char* dayNames[] = { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" };
        for (int i = 0; i < 6; i++) {
            d[i] = new days();
            d[i]->day = dayNames[i];
        }
    }

    ~timetable() {
        for (int i = 0; i < 6; i++) {
            delete d[i];
        }
    }

    void load(const string& filename) {
        ifstream file(filename);
        if (!file) {
            cout << "Error opening file." << endl;
            return;
        }

        const int startLines[] = { 2, 54, 106, 158, 210, 263 }; // Rows where each day's rooms start
        string line;
        regex courseRegex("([^,]+)\\(([^)]+)\\)"); 

        for (int day = 0; day < 6; day++) {
            file.clear(); 
            file.seekg(0, ios::beg); 

            int currentLine = 0;
            while (currentLine < startLines[day] - 1 && getline(file, line)) {
                currentLine++;
            }

            int roomIndex = 0;
            while (getline(file, line) && roomIndex < 50) {
                stringstream ss(line);
                string roomName;
                getline(ss, roomName, ','); // Extract the room name from the first column
                d[day]->ROOM[roomIndex]->name = roomName;

                string courseSectionString;
                int slotIndex = 0;
                while (getline(ss, courseSectionString, ',')) {
                    smatch matches;
                    if (regex_search(courseSectionString, matches, courseRegex) && matches.size() == 3) {
                        tt* newCourse = new tt();
                        newCourse->coursename = matches[1].str();
                        newCourse->section = matches[2].str();
                        newCourse->start = timeSlots[slotIndex % 7]; 
                        newCourse->next = d[day]->ROOM[roomIndex]->classes;
                        d[day]->ROOM[roomIndex]->classes = newCourse;
                    }
                    slotIndex++;
                }
                roomIndex++;
            }
        }

        file.close();
    }

    void printDay(const string& dayName) {
        string input = dayName;
        for (auto& c : input) c = tolower(c);

        for (int i = 0; i < 6; i++) {
            string compDay = d[i]->day;
            for (auto& c : compDay) c = tolower(c);

            if (compDay == input) {
                cout << "Schedule for " << d[i]->day << ":" << endl;
                for (int room = 0; room < 50; room++) {
                    cout << d[i]->ROOM[room]->name << ":" << endl;
                    for (tt* course = d[i]->ROOM[room]->classes; course != nullptr; course = course->next) {
                        cout << "  " << course->coursename << " (" << course->section << ") " << course->start << endl;
                    }
                }
                return;
            }
        }
        cout << "Day not found. Please enter a valid day name." << endl;
    }
};

int main() {
    timetable myTimetable;
    return 0;
}
