#include <stdio.h> 
  
int search(int arr[], int N, int x) 
{ 
    int left = 0;
    int right = N - 1;
    while (left <= right) {
        int mid = left + (right - left) / 2;
        if (arr[mid] == x)
            return mid;
        if (arr[mid] < x)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1; 
} 
  
// Driver code 
int main(void) 
{ 
    int arr[] = { 2, 3, 4, 10, 40 }; 
    int x = 10; 
    int N = sizeof(arr) / sizeof(arr[0]); 
  
    // Function call 
    int result = search(arr, N, x); 
    (result == -1) 
        ? printf("Element is not present in array") 
        : printf("Element is present at index %d", result); 
    return 0; 
}
