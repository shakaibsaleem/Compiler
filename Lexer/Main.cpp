#pragma once
#include <stdio.h>
#include <conio.h>


int main()
{
	int b = 2;
	int a = +b;
	printf("%d\n", a); // print a
	printf("enter a num\n"); //display msg
	scanf_s("%d", &a); // a = input()
	printf("num is %d", a); // print num is a
	//scanf_s("%d", &a); // extra input to prevent program closing
	_getch(); // to prevent program closing
	return 0;
}

