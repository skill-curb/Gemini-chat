#include <stdio.h> 
#include "search.h"
  
// Utility function to swap two elements
void swap(int *xp, int *yp) {
    int temp = *xp;
    *xp = *yp;
    *yp = temp;
}


  
// Driver code 
int main(void) 
{ 
    int arr[] = { 2, 3, 4, 10, 40 }; 
    int x = 10; 
    int N = sizeof(arr) / sizeof(arr[0]); 
  
    // Sort the array before searching
    for (int i = 0; i < N-1; i++)       
        for (int j = 0; j < N-i-1; j++) 
            if (arr[j] > arr[j+1]) 
                swap(&arr[j], &arr[j+1]);

    // Function call 
    int result = search(arr, N, x); 
    (result == -1) 
        ? printf("Element is not present in array") 
        : printf("Element is present at index %d", result); 
    return 0; 
}
