#include <iostream>
#include <ctime>
#include <cmath>

using namespace std;

float pi(int loops);


int main(){
	srand(time(NULL));
	cout << pi(10000000) << endl; // 10,000,000
}


float pi(int loops) {
	float circleNums = 0; // Number of points that are in the circle
	float total = 0;      // Total number of points
	float x;
	float y;
	float x_sqr;  // Square of X
	float y_sqr;  // Square of Y
	float sum;    // Sum of squared x and y


	for (int i = 0; i < loops; i++) {
		x = float((double)rand() / (double)(RAND_MAX / 1.0)); // 2 random floating point numbers between 0 and 1
		y = float((double)rand() / (double)(RAND_MAX / 1.0));

		x_sqr = pow(x, 2.0); // x^2
		y_sqr = pow(y, 2.0); // x^2

		sum = x_sqr + y_sqr;

		if (sum <= 1) {
			circleNums++;
		}
		total++;
	}

	total = 4 * circleNums / total;

	return total;
}
