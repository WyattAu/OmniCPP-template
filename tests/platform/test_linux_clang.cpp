// Linux Clang Platform Test
// Tests basic C++ compilation on Linux with Clang
// Reference: ADR-028-linux-platform-support.md, REQ-009-cleanup.md

#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<int> v = {1, 2, 3};
    std::string s = "Hello, World!";
    std::cout << s << std::endl;
    return 0;
}
