#include <iostream>
#include <fstream>

using namespace std;

void possibileStrConfigs(string str, int startIndex, int endIndex);
void swap(char *item1, char *item2);
ofstream file;


int main()
{
    string str;
    file.open("string_configs.txt", std::ios_base::app);

    // Get Input
    cout << "STRING: ";
    cin >> str;

    // Call function
    possibileStrConfigs(str, 0, str.length() - 1);
}


void swap(char *item1, char *item2)
{
    char *tempIem1 = item1;
    item1 = item2;
    item2 = tempIem1;
}


void possibileStrConfigs(string str, int startIndex, int endIndex) 
{
    if (startIndex == endIndex) // break out of recursion (base case)
    {
        //cout << str << endl;
        file << str << "\n";
    }

    for (int i = startIndex; i <= endIndex; i++) 
    {
        swap(str[startIndex], str[i]); // swaps the (originally first) index of the string with the indexed letter (i)

        possibileStrConfigs(str, startIndex + 1, endIndex); // calls the function again but for the following letter

        swap(str[startIndex], str[i]);  // backtracking solves all sub-problems one by one
    }
}
