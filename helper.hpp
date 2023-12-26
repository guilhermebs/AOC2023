#include <vector>
# include <string>

void tokenize(const std::string &str, const std::string &sep, std::vector<std::string> &results, size_t init_pos = 0)
{
    size_t pos = init_pos;
    size_t next_token = 0;
    do {
        next_token = str.find(sep, pos);
        results.push_back(str.substr(pos, next_token - pos));
        pos = next_token + sep.size();
    } while (next_token != std::string::npos);

};