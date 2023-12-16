#include<iostream>
#include<fstream>
#include<ostream>
#include<string>
#include<vector>
#include<unordered_set>

template <class T>
inline void hash_combine(std::size_t & s, const T & v)
{
  std::hash<T> h;
  s^= h(v) + 0x9e3779b9 + (s<< 6) + (s>> 2);
}

struct BeamFront {
    int i;
    int j;
    char dir;

    bool operator==(const BeamFront &other) const {
       return (
           i == other.i &&
           j == other.j &&
           dir == other.dir
       );
    };

    void print() {
        std::cout << "(" << i << "," << j << ") " << dir << "\n";
    };
};


template <>
struct std::hash<BeamFront> {
  std::size_t operator()(const BeamFront& k) const {
    size_t result = 0;
    hash_combine(result, k.j);
    hash_combine(result, k.j);
    hash_combine(result, k.dir);
    return result;
  }
};

std::vector<BeamFront> descendents(std::vector<std::string> *cave, BeamFront bf) {
    BeamFront right = BeamFront{bf.i + 1, bf.j, '>'};
    BeamFront left = BeamFront{bf.i - 1, bf.j, '<'};
    BeamFront up = BeamFront{bf.i, bf.j - 1, '^'};
    BeamFront down = BeamFront{bf.i, bf.j +1, 'v'};
    char cur_cel = (*cave)[bf.j][bf.i];

    if ((cur_cel == '.' || cur_cel == '-') && bf.dir == '>')
    {
        return std::vector<BeamFront>{right};
    }
    else if ((cur_cel == '.' || cur_cel == '-') && bf.dir == '<')
    {
        return std::vector<BeamFront>{left};
    }
    else if ((cur_cel == '.' || cur_cel == '|') && bf.dir == '^')
    {
        return std::vector<BeamFront>{up};
    }
    else if ((cur_cel == '.' || cur_cel == '|') && bf.dir == 'v')
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '/' && bf.dir == '>')
    {
        return std::vector<BeamFront>{up};
    }
    else if (cur_cel == '/' && bf.dir == '<')
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '/' && bf.dir == '^')
    {
        return std::vector<BeamFront>{right};
    }
    else if (cur_cel == '/' && bf.dir == 'v')
    {
        return std::vector<BeamFront>{left};
    }
    else if (cur_cel == '\\' && bf.dir == '>')
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '\\' && bf.dir == '<')
    {
        return std::vector<BeamFront>{up};
    }
    else if (cur_cel == '\\' && bf.dir == '^')
    {
        return std::vector<BeamFront>{left};
    }
    else if (cur_cel == '\\' && bf.dir == 'v')
    {
        return std::vector<BeamFront>{right};
    }
    else if (cur_cel == '|' && (bf.dir == '>' || bf.dir == '<') )
    {
        return std::vector<BeamFront>{down, up};
    }
    else if (cur_cel == '-' && (bf.dir == '^' || bf.dir == 'v') )
    {
        return std::vector<BeamFront>{left, right};
    }
    return std::vector<BeamFront>{};
}

size_t propagate_beam(std::vector<std::string> *cave, BeamFront start) {
    std::deque<BeamFront> beam_fronts{start};
    std::unordered_set<BeamFront> seen;
    auto const nrows{(*cave).size()};
    auto const ncols{(*cave).front().size()};
    std::vector<bool> unique_positions;
    unique_positions.resize(nrows*ncols, false);
    size_t t = 0;

    while (beam_fronts.size() > 0) { 
        t++;
        BeamFront bf = std::move(beam_fronts.back());
        beam_fronts.pop_back();
        seen.insert(bf);
        unique_positions[bf.i + bf.j * ncols] = true;
        for (auto d: descendents(cave, bf))
        {
            if (d.i >= 0 && d.i < ncols && d.j >= 0 && d.j < nrows && !seen.contains(d)) beam_fronts.push_back(d);
        }
    }
    
    return std::count(unique_positions.begin(), unique_positions.end(), true);
}

int main() {
    std::vector<std::string> cave;
    //std::ifstream file("input/day16_example");
    std::ifstream file("input/day16");
    std::string line;

    while (std::getline(file, line))
    {
        cave.push_back(line);
    }
    auto sol_part1 = propagate_beam(&cave, BeamFront{0, 0, '>'});
    std::cout << "Part 1 solution: " << sol_part1 << "\n";

    size_t sol_part2 = 0;
    for (int j = 0; j < cave.size(); j++)
    {
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{0, j, '>'}));
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{(int) cave[0].size() - 1, j, '<'}));
    };
    for (int i = 0; i < cave[0].size(); i++)
    {
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{i, 0, 'v'}));
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{i, (int) cave.size() - 1, '^'}));
    };

    std::cout << "Part 1 solution: " << sol_part2 << "\n";
    return 0; 
}

