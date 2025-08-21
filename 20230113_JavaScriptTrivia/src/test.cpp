#include <iostream>
#include <vector>

int main() {
    std::vector<int> Xs{1, 2, 3};
    while (Xs) {  // Error!!
        std::cout << Xs.back() << std::endl;
        Xs.pop_back();
    }
}

// Error: expression must have bool type (or be convertible to bool)
