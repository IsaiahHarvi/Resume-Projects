#include <iostream>
#include <ctime>
#include <cmath>

using namespace std;

float pi(int loops);


int main(){
	srand(time(NULL));
	cout << pi(100000000) << endl;
}


float pi(int loops) {
	float circleNums = 0;
	float total = 0;

	for (int i = 0; i < loops; i++) {
		float num1 = float((double)rand() / (double)(RAND_MAX / 1.0)); // 2 random floating point numbers between 0 and 1
		float num2 = float((double)rand() / (double)(RAND_MAX / 1.0));

		float num1S = pow(x, 2.0); // squares each floating point num
		float num2S = pow(y, 2.0);

		float sum = num1S + num2S; 

		if (sum <= 1) {
			circleNums++;
		}
		total++;
	}

	float total = 4 * circleNums / total;

	return total;
}
