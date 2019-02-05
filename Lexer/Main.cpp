#pragma once
#include <stdio.h>
#include <conio.h>
#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
	//fstream myFile;
	string line;
	ifstream myFile;
	myFile.open("snippet.huc");
	if (myFile.is_open())
	{
		printf("File Opened\n");
		//myFile << "hello";
		//printf("File written\n");
		
		while (getline(myFile, line))
		{
			cout << line << '\n';
		}

		myFile.close();
		printf("File Closed\n");
	}
	else printf("Cant open\n");
	_getch(); // to prevent program closing
	return 0;
}

void test()
{
	int b = 2;
	int a = +b;
	printf("%d\n", a); // print a
	printf("enter a num\n"); //display msg
	scanf_s("%d", &a); // a = input()
	printf("num is %d", a); // print num is a, %d gets replaced by value of a
	//scanf_s("%d", &a); // extra input to prevent program closing
	//StreamReader r = new StreamReader("C:\\Users\\Public\\ServerInfo.ini");
	//string s = r.ReadLine();
	return;
}

