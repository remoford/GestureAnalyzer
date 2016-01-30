// GestureAnalyzer.cpp : Defines the entry point for the application.
//

#include "stdafx.h"
#include "GestureAnalyzer.h"
#include <array>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>
#include <myo/myo.hpp>
#include <vector>
#include <stack>
#include "commctrl.h"
#include "windows.h"
#include "resource.h"
#include <fstream>
#include <cstdlib>
#pragma comment(lib, "comctl32.lib")



#define MAX_LOADSTRING 100
#define EMG_SAMPLE_BUF_SIZE 1000
#define GRAPH_START_X 300
#define GRAPH_START_Y 100
#define CHANNEL_VERTICAL_SPACING 70
#define GRAPH_QUANTIZATION 8

// Global Variables:
HINSTANCE hInst;								// current instance
TCHAR szTitle[MAX_LOADSTRING];					// The title bar text
TCHAR szWindowClass[MAX_LOADSTRING];			// the main window class name
HWND hEdit; // our text box for output
HWND hwndTrack; // our slider for adding marks
bool isInitialized = false;
int8_t emgSampleBuf[8][EMG_SAMPLE_BUF_SIZE];
int emgSampleBufIdx = 0;
myo::Hub * hubPtr;
myo::Myo * myMyo;
LARGE_INTEGER StartingTime, PreviousTime, EndingTime, ElapsedMicroseconds;
LARGE_INTEGER Frequency;
int sampleCount = 0;
LONGLONG emgAverage[8];
std::stack<int> marks;

// Forward declarations of functions included in this code module:
ATOM				MyRegisterClass(HINSTANCE hInstance);
BOOL				InitInstance(HINSTANCE, int);
LRESULT CALLBACK	WndProc(HWND, UINT, WPARAM, LPARAM);
INT_PTR CALLBACK	About(HWND, UINT, WPARAM, LPARAM);

int APIENTRY _tWinMain(_In_ HINSTANCE hInstance,
                     _In_opt_ HINSTANCE hPrevInstance,
                     _In_ LPTSTR    lpCmdLine,
                     _In_ int       nCmdShow)
{
	UNREFERENCED_PARAMETER(hPrevInstance);
	UNREFERENCED_PARAMETER(lpCmdLine);

 	// TODO: Place code here.
	MSG msg;
	HACCEL hAccelTable;

	// Initialize global strings
	LoadString(hInstance, IDS_APP_TITLE, szTitle, MAX_LOADSTRING);
	LoadString(hInstance, IDC_GestureAnalyzer, szWindowClass, MAX_LOADSTRING);
	MyRegisterClass(hInstance);

	// Perform application initialization:
	if (!InitInstance (hInstance, nCmdShow))
	{
		return FALSE;
	}

	hAccelTable = LoadAccelerators(hInstance, MAKEINTRESOURCE(IDC_GestureAnalyzer));

	// Main message loop:
	while (GetMessage(&msg, NULL, 0, 0))
	{
		if (!TranslateAccelerator(msg.hwnd, hAccelTable, &msg))
		{
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}

	return (int) msg.wParam;
}

VOID PrintMsg(LPARAM myMsg)
{
	int ndx = GetWindowTextLength(hEdit);
	SendMessage(hEdit, EM_SETSEL, (WPARAM)ndx, (LPARAM)ndx);
	SendMessage(hEdit,
		EM_REPLACESEL,
		NULL,
		(LPARAM)myMsg);
}

struct emgSample{
	uint64_t timestamp;
	std::array<int8_t, 8> value;
};

class RawEmgData {
public:
	void AddSample(uint64_t timestamp, const int8_t* emg){
		if (noSamples){
			startingTime = timestamp;
			noSamples = false;
		}
		emgSample sample;
		sample.timestamp = timestamp;
		for (int i = 0; i < 8; i++) {
			sample.value[i] = emg[i];
		}
		samples.push_back(sample);
	}
	void Finalize(){
		if (samples.size() == 0){
			startingTime = 0;
			endingTime = 0;
		}
		else{
			endingTime = samples.back().timestamp;
		}
	}

	void save() {
		std::fstream fs;


		//if (const char* env_p = std::getenv("APPDATA"))



		fs.open("C:\\rawsamples.txt", std::fstream::in | std::fstream::out | std::fstream::app);

		fs << "Starting time:" << startingTime << std::endl;
		fs << "Ending time:" << endingTime << std::endl;

		for (auto iter = samples.begin(); iter != samples.end(); ++iter) {
			fs << iter->timestamp << ","
				<< static_cast<int>(iter->value[0]) << ","
				<< static_cast<int>(iter->value[1]) << ","
				<< static_cast<int>(iter->value[2]) << ","
				<< static_cast<int>(iter->value[3]) << ","
				<< static_cast<int>(iter->value[4]) << ","
				<< static_cast<int>(iter->value[5]) << ","
				<< static_cast<int>(iter->value[6]) << ","
				<< static_cast<int>(iter->value[7]) << std::endl;
		}


		fs.close();

	}




	uint64_t startingTime;
	uint64_t endingTime;
	std::vector<emgSample> samples;
private:
	uint64_t previousTime;
	BOOL noSamples = true;
};
RawEmgData * myRawEmgDataPtr = NULL;

class NormalizedEmgData {
public:
	NormalizedEmgData(){
		for (int i = 0; i < 1000; i++) {
			emgSample sample;
			for (int j = 0; j < 8; j++) {
				sample.value[j] = 0;
			}
			samples.push_back(sample);
		}
	}

	void save() {
		std::fstream fs;
		fs.open("C:\\samples.txt", std::fstream::in | std::fstream::out | std::fstream::app);

		fs << "Starting time:" << startingTime << std::endl;
		fs << "Ending time:" << endingTime << std::endl;
		fs << "Sample count:" << sampleCount << std::endl;

		for (auto iter = samples.begin(); iter != samples.end(); ++iter) {
			fs << iter->timestamp << ","
				<< static_cast<int>(iter->value[0]) << ","
				<< static_cast<int>(iter->value[1]) << ","
				<< static_cast<int>(iter->value[2]) << ","
				<< static_cast<int>(iter->value[3]) << ","
				<< static_cast<int>(iter->value[4]) << ","
				<< static_cast<int>(iter->value[5]) << ","
				<< static_cast<int>(iter->value[6]) << ","
				<< static_cast<int>(iter->value[7]) << std::endl;
		}


		fs.close();

	}

	std::vector<emgSample> samples;
	uint64_t startingTime;
	uint64_t endingTime;
	int sampleCount = 0;
	//std::array<ULONGLONG, 8> average;
	std::array<double, 8> average;
};
NormalizedEmgData * myNormalizedEmgDataPtr = NULL;

VOID NormalizeEmgData(NormalizedEmgData * myNormalizedEmgData){
	for (int emgChannel = 0; emgChannel < 8; emgChannel++) {
		myNormalizedEmgData->average[emgChannel] = 0;
	}


	if (myRawEmgDataPtr->samples.size() <= 0){
		PrintMsg((LPARAM)L"Zero Samples Collected! ");
	}


	INT rollForward = (myRawEmgDataPtr->samples.size() - 1) - 1000;
	if (rollForward < 0) {
		rollForward = 0;
	}
	myNormalizedEmgData->startingTime = myRawEmgDataPtr->samples[rollForward].timestamp;
	

	// Loop through the raw emg samples
	for (UINT emgSampleIdx = rollForward; emgSampleIdx < myRawEmgDataPtr->samples.size()-1; emgSampleIdx++) {
		// Calculate the time difference between the start of the data and the current sample timestamp
		//uint64_t localElapsedMicroseconds = myRawEmgDataPtr->samples[emgSampleIdx].timestamp - myRawEmgDataPtr->startingTime;
		uint64_t localElapsedMicroseconds = myRawEmgDataPtr->samples[emgSampleIdx].timestamp - myRawEmgDataPtr->samples[rollForward].timestamp;
		int elapsedMilliseconds = (int)(localElapsedMicroseconds / 1000);
		int normalizedEmgSampleIdx = (int)(localElapsedMicroseconds / 5000);
		if (normalizedEmgSampleIdx >= 1000){
			break;
		}
		myNormalizedEmgData->endingTime = myRawEmgDataPtr->samples[emgSampleIdx].timestamp;
		myNormalizedEmgData->sampleCount++;
		// Loop through the eight channels
		for (int emgChannel = 0; emgChannel < 8; emgChannel++) {
			myNormalizedEmgData->samples[normalizedEmgSampleIdx].value[emgChannel] = myRawEmgDataPtr->samples[emgSampleIdx].value[emgChannel];
			myNormalizedEmgData->average[emgChannel] += abs(myRawEmgDataPtr->samples[emgSampleIdx].value[emgChannel]);
		}
	}
	for (int emgChannel = 0; emgChannel < 8; emgChannel++) {
		myNormalizedEmgData->average[emgChannel] = myNormalizedEmgData->average[emgChannel] / EMG_SAMPLE_BUF_SIZE;
	}
	//myNormalizedEmgData->startingTime = myRawEmgDataPtr->startingTime;
}

VOID GetData(){
	if (isInitialized){
		PrintMsg((LPARAM)L"Collecting EMG data...\r\n");
		myRawEmgDataPtr = new RawEmgData;
		for (int i = 0; i < 1; i++){
			hubPtr->run(5000);
		}
		myRawEmgDataPtr->Finalize();

		myRawEmgDataPtr->save();


		if (myNormalizedEmgDataPtr != NULL){
			delete myNormalizedEmgDataPtr;
		}
		myNormalizedEmgDataPtr = new NormalizedEmgData;
		NormalizeEmgData(myNormalizedEmgDataPtr);

		myNormalizedEmgDataPtr->save();

		wchar_t buf[10];
		PrintMsg((LPARAM)L"Starting Time: ");
		swprintf(buf, 10, L"%d", myNormalizedEmgDataPtr->startingTime);
		PrintMsg((LPARAM)buf);
		PrintMsg((LPARAM)L"\r\n");

		PrintMsg((LPARAM)L"Ending Time: ");
		swprintf(buf, 10, L"%d", myNormalizedEmgDataPtr->endingTime);
		PrintMsg((LPARAM)buf);
		PrintMsg((LPARAM)L"\r\n");

		PrintMsg((LPARAM)L"Elapsed Milliseconds: ");
		swprintf(buf, 10, L"%d", (myNormalizedEmgDataPtr->endingTime - myNormalizedEmgDataPtr->startingTime) / 1000);
		PrintMsg((LPARAM)buf);
		PrintMsg((LPARAM)L"\r\n");

		PrintMsg((LPARAM)L"Raw Sample Count: ");
		swprintf(buf, 10, L"%d", myRawEmgDataPtr->samples.size());
		PrintMsg((LPARAM)buf);
		PrintMsg((LPARAM)L"\r\n");

		PrintMsg((LPARAM)L"Normalized Sample Count: ");
		swprintf(buf, 10, L"%d", myNormalizedEmgDataPtr->sampleCount);
		PrintMsg((LPARAM)buf);
		PrintMsg((LPARAM)L"\r\n");

		delete myRawEmgDataPtr;
		PrintMsg((LPARAM)L"Done.\r\n");
	}
	else{
		PrintMsg((LPARAM)L"Can not get data, myo is not initialized.\r\n");
	}

}

class DataCollector : public myo::DeviceListener {
public:
	DataCollector()
		: emgSamples()
	{
	}
	void onUnpair(myo::Myo* myo, uint64_t timestamp)
	{
		emgSamples.fill(0);
	}
	// onEmgData() is called whenever a paired Myo has provided new EMG data, and EMG streaming is enabled.
	void onEmgData(myo::Myo* myo, uint64_t timestamp, const int8_t* emg)
	{
		QueryPerformanceCounter(&EndingTime);
		sampleCount++;
		LONGLONG localElapsedMicroseconds = EndingTime.QuadPart - StartingTime.QuadPart;
		int ElapsedMilliseconds = (int) (localElapsedMicroseconds / 1000);
		emgSampleBufIdx = ElapsedMilliseconds % EMG_SAMPLE_BUF_SIZE;
		for (int i = 0; i < 8; i++) {
			emgSampleBuf[i][emgSampleBufIdx] = abs(emg[i]);
			emgSamples[i] = emg[i];
		}
		if (myRawEmgDataPtr != NULL){
			myRawEmgDataPtr->AddSample(timestamp, emg);
		}
		PreviousTime = EndingTime;
	}
	void print()
	{
		// Print out the EMG data.
		PrintMsg((LPARAM)L"Sample: ");
		for (size_t i = 0; i < emgSamples.size(); i++) {
			wchar_t buf[10];
			swprintf(buf, 10, L"%d", emgSamples[i]);
			PrintMsg((LPARAM)buf);
			PrintMsg((LPARAM)L" ");	
		}
		PrintMsg((LPARAM)L"\r\n");

	}
	// The values of this array is set by onEmgData() above.
	std::array<int8_t, 8> emgSamples;
};
DataCollector * dataCollectorPtr = NULL;

ATOM MyRegisterClass(HINSTANCE hInstance)
{
	WNDCLASSEX wcex;
	wcex.cbSize = sizeof(WNDCLASSEX);
	wcex.style			= CS_HREDRAW | CS_VREDRAW;
	wcex.lpfnWndProc	= WndProc;
	wcex.cbClsExtra		= 0;
	wcex.cbWndExtra		= 0;
	wcex.hInstance		= hInstance;
	wcex.hIcon			= LoadIcon(hInstance, MAKEINTRESOURCE(IDI_GestureAnalyzer));
	wcex.hCursor		= LoadCursor(NULL, IDC_ARROW);
	wcex.hbrBackground	= (HBRUSH)(COLOR_WINDOW+1);
	wcex.lpszMenuName	= MAKEINTRESOURCE(IDC_GestureAnalyzer);
	wcex.lpszClassName	= szWindowClass;
	wcex.hIconSm		= LoadIcon(wcex.hInstance, MAKEINTRESOURCE(IDI_SMALL));
	return RegisterClassEx(&wcex);
}

BOOL InitInstance(HINSTANCE hInstance, int nCmdShow)
{
   HWND hWnd;
   hInst = hInstance; // Store instance handle in our global variable
   hWnd = CreateWindow(szWindowClass, szTitle, WS_OVERLAPPEDWINDOW,
      CW_USEDEFAULT, 0, CW_USEDEFAULT, 0, NULL, NULL, hInstance, NULL);
   if (!hWnd)
   {
      return FALSE;
   }
   ShowWindow(hWnd, nCmdShow);
   UpdateWindow(hWnd);
   return TRUE;
}

BOOL InitMyo()
{
	try {
		hubPtr = new myo::Hub("com.remo.myoemgtestapp");
		PrintMsg((LPARAM)L"Attempting to find a Myo...\r\n");
		myMyo = hubPtr->waitForMyo(10000);
		// If waitForMyo() returned a null pointer, we failed to find a Myo, so exit with an error message.
		if (!myMyo) {
			PrintMsg((LPARAM)L"Unable to find a Myo!\r\n");
			return 1;
		}
		PrintMsg((LPARAM)L"Connected to a Myo armband!\r\n");
		myMyo->notifyUserAction();
		myMyo->setStreamEmg(myo::Myo::streamEmgEnabled);
		dataCollectorPtr = new DataCollector;
		hubPtr->addListener(dataCollectorPtr);
		PrintMsg((LPARAM)L"Myo Initialized.\r\n");

	}
	catch (const std::exception& e) {
		PrintMsg((LPARAM)L"Error!\r\n");
		wchar_t errorStrW[sizeof(wchar_t)*1000];
		size_t numConverted;
		mbstowcs_s(&numConverted, errorStrW, (size_t)1000, e.what(), (size_t)1000);
		PrintMsg((LPARAM)errorStrW );
		return 1;
	}
	isInitialized = true;
	return 0;
}

VOID PaintGraph(HDC hdc){
	// TODO: Add any drawing code here...

	LPPOINT currentPosition = 0;

	COLORREF penColor[8];
	penColor[0] = RGB(0, 255, 0);
	penColor[1] = RGB(255, 0, 0);
	penColor[2] = RGB(0, 0, 0);
	penColor[3] = RGB(0, 0, 255);
	penColor[4] = RGB(255, 255, 0);
	penColor[5] = RGB(0, 255, 255);
	penColor[6] = RGB(255, 0, 255);
	penColor[7] = RGB(128, 128, 128);

	// Set starting position
	MoveToEx(hdc, GRAPH_START_X, GRAPH_START_Y, currentPosition);
	SelectObject(hdc, GetStockObject(DC_PEN));

	if (myNormalizedEmgDataPtr != NULL){

		for (size_t emgChannel = 0; emgChannel < 8; emgChannel++) {
			MoveToEx(hdc, GRAPH_START_X, GRAPH_START_Y + emgChannel * CHANNEL_VERTICAL_SPACING, currentPosition);
			// Loop through our data
			SetDCPenColor(hdc, penColor[emgChannel]);
			for (size_t i = 0; i < myNormalizedEmgDataPtr->samples.size() / 1; i++) {
				int newX = GRAPH_START_X + (i * 1);
				int newY = 0;
				for (int j = 0; j < 1; j++){
					newY += myNormalizedEmgDataPtr->samples[(i * 1) + j].value[emgChannel];
				}
				newY = GRAPH_START_Y + emgChannel*CHANNEL_VERTICAL_SPACING - (newY / 1);
				LineTo(hdc, newX, newY);
			}
			wchar_t buf[10];
			swprintf(buf, 10, L"%5f", myNormalizedEmgDataPtr->average[emgChannel]);
			TextOut(hdc, 1300, GRAPH_START_Y + emgChannel*CHANNEL_VERTICAL_SPACING, buf, 2);
		}

		
		for (size_t emgChannel = 0; emgChannel < 8; emgChannel++) {
			std::stack<int> thresholdCrossings;
			MoveToEx(hdc, GRAPH_START_X, GRAPH_START_Y + emgChannel * CHANNEL_VERTICAL_SPACING, currentPosition);
			// Loop through our data
			SetDCPenColor(hdc, penColor[emgChannel]);
			for (size_t i = 0; i < myNormalizedEmgDataPtr->samples.size() / GRAPH_QUANTIZATION; i++) {
				int newX = GRAPH_START_X + (i * GRAPH_QUANTIZATION);
				int newY = 0;
				for (int j = 0; j < GRAPH_QUANTIZATION; j++){
					newY += abs(myNormalizedEmgDataPtr->samples[(i * GRAPH_QUANTIZATION) + j].value[emgChannel]);
				}
				if (newY > 32) {
					thresholdCrossings.push(newX);
				}
				newY = GRAPH_START_Y + emgChannel*CHANNEL_VERTICAL_SPACING - (newY / GRAPH_QUANTIZATION);
				LineTo(hdc, newX, newY);
			}
			wchar_t buf[10];
			swprintf(buf, 10, L"%5f", myNormalizedEmgDataPtr->average[emgChannel]);
			TextOut(hdc, 1300, GRAPH_START_Y + emgChannel*CHANNEL_VERTICAL_SPACING, buf, 2);
			int thresholdCrossing = 0;
			while (thresholdCrossings.size() > 0)
			{
				thresholdCrossing = thresholdCrossings.top() + emgChannel;
				thresholdCrossings.pop();
				MoveToEx(hdc, thresholdCrossing, 0, currentPosition);
				LineTo(hdc, thresholdCrossing, 50);
			}

		}

		SetDCPenColor(hdc, RGB(0, 0, 0));
		int mark = 0;
		while (marks.size() > 0)
		{
			mark = marks.top();
			marks.pop();
			MoveToEx(hdc, mark + GRAPH_START_X, GRAPH_START_Y, currentPosition);
			LineTo(hdc, mark + GRAPH_START_X, 800);
		}


	}
}

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam)
{
	int wmId, wmEvent;
	PAINTSTRUCT ps;
	HDC hdc;
	DWORD dwPos;
	

	switch (message)
	{
	case WM_CREATE:
		{
		HWND hWndButton = CreateWindowEx(NULL,
			L"BUTTON",
			L"Initialize",
			WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
			25,
			25,
			200,
			24,
			hWnd,
			(HMENU)IDC_REMO_BUTTON,
			GetModuleHandle(NULL),
			NULL);
		HWND getDataButton = CreateWindowEx(NULL,
			L"BUTTON",
			L"Get Data",
			WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
			25,
			50,
			200,
			24,
			hWnd,
			(HMENU)IDC_GETDATA_BUTTON,
			GetModuleHandle(NULL),
			NULL);
		HWND addMarkButton = CreateWindowEx(NULL,
			L"BUTTON",
			L"Add Mark",
			WS_TABSTOP | WS_VISIBLE | WS_CHILD | BS_DEFPUSHBUTTON,
			25,
			75,
			200,
			24,
			hWnd,
			(HMENU)IDC_ADDMARK_BUTTON,
			GetModuleHandle(NULL),
			NULL);
		hEdit = CreateWindowEx(WS_EX_CLIENTEDGE,
			L"EDIT",
			L"",
			WS_CHILD | WS_VISIBLE | ES_MULTILINE | ES_AUTOVSCROLL,
			25,
			125,
			200,
			500,
			hWnd,
			(HMENU)IDC_REMO_EDIT,
			GetModuleHandle(NULL),
			NULL);


		InitCommonControls();

		hwndTrack = CreateWindowEx(NULL,
			TRACKBAR_CLASS,
			L"Trackbar",
			WS_CHILD |
			WS_VISIBLE |
			TBS_AUTOTICKS |
			TBS_ENABLESELRANGE,
			GRAPH_START_X,
			650,
			1000,
			50,
			hWnd,
			(HMENU)IDC_MARK_TRACKBAR,
			GetModuleHandle(NULL),
			NULL);
		
		SendMessage(hwndTrack, TBM_SETRANGE,
			(WPARAM)TRUE,                   // redraw flag 
			(LPARAM)MAKELONG(0, 1000));  // min. & max. positions

		SendMessage(hwndTrack, TBM_SETPAGESIZE,
			0, (LPARAM)4);                  // new page size 


		SendMessage(hwndTrack, TBM_SETPOS,
			(WPARAM)TRUE,                   // redraw flag 
			(LPARAM)500);

		SetFocus(hwndTrack);

		

		HGDIOBJ hfDefault = GetStockObject(DEFAULT_GUI_FONT);
		SendMessage(hEdit,
			WM_SETFONT,
			(WPARAM)hfDefault,
			MAKELPARAM(FALSE, 0));
		SendMessage(hEdit,
			WM_SETTEXT,
			NULL,
			(LPARAM)L"Howdy pilgrim!\r\n");
		}
		break;
	case WM_COMMAND:
		wmId    = LOWORD(wParam);
		wmEvent = HIWORD(wParam);
		// Parse the menu selections:
		switch (wmId)
		{
		case IDM_ABOUT:
			DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;
		case IDM_EXIT:
			DestroyWindow(hWnd);
			break;
		case ID_REMO_DOSOMETHING:
			DialogBox(hInst, MAKEINTRESOURCE(IDD_ABOUTBOX), hWnd, About);
			break;
		case IDC_REMO_BUTTON:
			{
				InitMyo();
			}
			break;
		case IDC_GETDATA_BUTTON:
		{
			GetData();
			InvalidateRect(hWnd, NULL, TRUE);
		}
			break;

		case IDC_ADDMARK_BUTTON:
			wchar_t buf[10];
			dwPos = SendMessage(hwndTrack, TBM_GETPOS, 0, 0);
			PrintMsg((LPARAM)L"Mark Position: ");
			swprintf(buf, 10, L"%d", dwPos);
			PrintMsg((LPARAM)buf);
			PrintMsg((LPARAM)L"\r\n");
			marks.push((int)dwPos);
			InvalidateRect(hWnd, NULL, TRUE);
			break;


		default:
			return DefWindowProc(hWnd, message, wParam, lParam);
		}
		break;
	case WM_PAINT:
		hdc = BeginPaint(hWnd, &ps);
		PaintGraph(hdc);
		EndPaint(hWnd, &ps);
		break;
	case WM_DESTROY:
		PostQuitMessage(0);
		break;
	default:
		return DefWindowProc(hWnd, message, wParam, lParam);
	}
	return 0;
}

// Message handler for about box.
INT_PTR CALLBACK About(HWND hDlg, UINT message, WPARAM wParam, LPARAM lParam)
{
	UNREFERENCED_PARAMETER(lParam);
	switch (message)
	{
	case WM_INITDIALOG:
		return (INT_PTR)TRUE;

	case WM_COMMAND:
		if (LOWORD(wParam) == IDOK || LOWORD(wParam) == IDCANCEL)
		{
			EndDialog(hDlg, LOWORD(wParam));
			return (INT_PTR)TRUE;
		}
		break;
	}
	return (INT_PTR)FALSE;
}




