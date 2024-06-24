#include <windows.h>
#include <stdio.h>

#define ID_TEXTBOX 1

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

void LoadTextFromFile(HWND hwndEdit, const char* filename) {
    FILE *file = fopen(filename, "r");
    if (file) {
        fseek(file, 0, SEEK_END);
        long fsize = ftell(file);
        fseek(file, 0, SEEK_SET);

        char *text = malloc(fsize + 1);
        fread(text, 1, fsize, file);
        text[fsize] = 0;

        SetWindowText(hwndEdit, text);

        free(text);
        fclose(file);
    }
}

void SaveTextToFile(HWND hwndEdit, const char* filename) {
    int length = GetWindowTextLength(hwndEdit);
    char *text = malloc(length + 1);
    GetWindowText(hwndEdit, text, length + 1);

    FILE *file = fopen(filename, "w");
    if (file) {
        fwrite(text, 1, length, file);
        fclose(file);
    }
    free(text);
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const char CLASS_NAME[] = "PostItClass";
    
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = CLASS_NAME;
    wc.hbrBackground = CreateSolidBrush(RGB(255, 255, 0)); // Amarelo

    RegisterClass(&wc);

    HWND hwnd = CreateWindowEx(
        0,
        CLASS_NAME,
        "Post-It",
        WS_OVERLAPPEDWINDOW,
        CW_USEDEFAULT, CW_USEDEFAULT, 500, 500,
        NULL,
        NULL,
        hInstance,
        NULL
    );

    if (hwnd == NULL) {
        return 0;
    }

    ShowWindow(hwnd, nCmdShow);

    MSG msg = { 0 };
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    static HWND hwndEdit;
    switch (uMsg) {
    case WM_CREATE:
       
        hwndEdit = CreateWindowEx(
            0, "EDIT", "",
            WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_LEFT | ES_MULTILINE | ES_AUTOVSCROLL,
            0, 0, 300, 500,
            hwnd, (HMENU)ID_TEXTBOX,
            (HINSTANCE)GetWindowLongPtr(hwnd, GWLP_HINSTANCE), NULL);
            
        LoadTextFromFile(hwndEdit, "postit.ini");
        break;

    case WM_SIZE: {
        RECT rcClient;
        //GetClientRect(hwnd, &rcClient);
       // SetWindowPos(hwndEdit, NULL, 0, 0, rcClient.right, rcClient.bottom, SWP_NOZORDER);
        break;
    }

    case WM_DESTROY:
        SaveTextToFile(hwndEdit, "postit.ini");
        PostQuitMessage(0);
        break;

    default:
        return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}
