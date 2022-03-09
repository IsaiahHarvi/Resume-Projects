#include <iostream>
#include <string>

using namespace std;

// Function Decl
int DrawBoard(char arr[][7]);
bool Move(int location);
bool Win();

// Global Variables
int moves = 0;
char peice = 'O';
char board[6][7];


int main()
{
    int move = NULL;
    for (int i = 0; i < 6; i++) // Construct board
    {
        for (int j = 0; j < 7; j++)
        {
            board[i][j] = 0;
        }
    }

    while (1) {
        DrawBoard(board); // Display

        std::cout << "Enter Column Number: ";
        cin >> move;

        if (move < 8 && move >= 1){
            Move(move-1); // Move peice in next column
            move = NULL;
        }
    }
   
    return 1;

}


int DrawBoard(char arr[][7])
{
    system("cls");

    cout << "\n\t   " << peice << "'s Turn!" << endl;

    cout << endl << "  1   2   3   4   5   6   7  " << endl;
    for (int i = 0; i < 6; i++)
    {
        cout << "|   |   |   |   |   |   |   |" << endl;
        cout << "| ";
        for (int j = 0; j < 7; j++)
        {
            if (arr[i][j] != 'X' && arr[i][j] != 'O') {
                cout << " " << " | ";
            } else { cout << arr[i][j] << " | "; }
        }
        cout << endl;
    }
    cout << "*******************************" << endl;
    return 1;
}


bool Move(int location)
{
    moves++;
    if (moves % 2 == 0) {
        peice = 'X';
    } else { peice = 'O'; }

    for (int i = 5; i > -1; i-=1) {
        if (board[i][location] != 'X' && board[i][location] != 'O')
        {
            board[i][location] = peice;
            break;
        }
    }
    return true;
}


bool Win(char arr[][7]) // unfinished
{
    return true;
}