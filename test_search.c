#include <stdio.h>
#include <assert.h>
#include "search.h"

void test_search_value_exists() {
    int arr[] = {1, 2, 3, 4, 5};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 3;
    int expected_index = 2;
    assert(search(arr, N, x) == expected_index);
}

void test_search_value_not_exists() {
    int arr[] = {1, 2, 3, 4, 5};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 6;
    assert(search(arr, N, x) == -1);
}

void test_search_empty_array() {
    int arr[] = {};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 1;
    assert(search(arr, N, x) == -1);
}

void test_search_single_element() {
    int arr[] = {1};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 1;
    assert(search(arr, N, x) == 0);
}

void test_search_first_element() {
    int arr[] = {1, 2, 3, 4, 5};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 1;
    assert(search(arr, N, x) == 0);
}

void test_search_last_element() {
    int arr[] = {1, 2, 3, 4, 5};
    int N = sizeof(arr) / sizeof(arr[0]);
    int x = 5;
    assert(search(arr, N, x) == N - 1);
}

int main() {
    test_search_value_exists();
    test_search_value_not_exists();
    test_search_empty_array();
    test_search_single_element();
    test_search_first_element();
    test_search_last_element();
    printf("All tests passed successfully.\n");
    return 0;
}
