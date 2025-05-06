#include <iostraem>
#include <map>
#include <vector>

int main() {
    vector<int> a{1, 2, 3};
    vector<int> b{1, 2, 3};

    map<vector<int>, int> d{a : 1};

    return 0;
}
