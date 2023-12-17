#include<iostream>
#include<fstream>
#include<string>
#include<vector>
#include<chrono>

template <class T>
inline void hash_combine(std::size_t & s, const T & v)
{
  std::hash<T> h;
  s^= h(v) + 0x9e3779b9 + (s<< 6) + (s>> 2);
}

enum Direction {
    up,
    down,
    left,
    right
};

struct BeamFront {
    int i;
    int j;
    Direction dir;

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
    BeamFront right = BeamFront{bf.i + 1, bf.j, Direction::right};
    BeamFront left = BeamFront{bf.i - 1, bf.j, Direction::left};
    BeamFront up = BeamFront{bf.i, bf.j - 1, Direction::up};
    BeamFront down = BeamFront{bf.i, bf.j +1, Direction::down};
    char cur_cel = (*cave)[bf.j][bf.i];

    if ((cur_cel == '.' || cur_cel == '-') && bf.dir == Direction::right)
    {
        return std::vector<BeamFront>{right};
    }
    else if ((cur_cel == '.' || cur_cel == '-') && bf.dir == Direction::left)
    {
        return std::vector<BeamFront>{left};
    }
    else if ((cur_cel == '.' || cur_cel == '|') && bf.dir == Direction::up)
    {
        return std::vector<BeamFront>{up};
    }
    else if ((cur_cel == '.' || cur_cel == '|') && bf.dir == Direction::down)
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '/' && bf.dir == Direction::right)
    {
        return std::vector<BeamFront>{up};
    }
    else if (cur_cel == '/' && bf.dir == Direction::left)
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '/' && bf.dir == Direction::up)
    {
        return std::vector<BeamFront>{right};
    }
    else if (cur_cel == '/' && bf.dir == Direction::down)
    {
        return std::vector<BeamFront>{left};
    }
    else if (cur_cel == '\\' && bf.dir == Direction::right)
    {
        return std::vector<BeamFront>{down};
    }
    else if (cur_cel == '\\' && bf.dir == Direction::left)
    {
        return std::vector<BeamFront>{up};
    }
    else if (cur_cel == '\\' && bf.dir == Direction::up)
    {
        return std::vector<BeamFront>{left};
    }
    else if (cur_cel == '\\' && bf.dir == Direction::down)
    {
        return std::vector<BeamFront>{right};
    }
    else if (cur_cel == '|' && (bf.dir == Direction::right || bf.dir == Direction::left) )
    {
        return std::vector<BeamFront>{down, up};
    }
    else if (cur_cel == '-' && (bf.dir == Direction::up || bf.dir == Direction::down) )
    {
        return std::vector<BeamFront>{left, right};
    }
    return std::vector<BeamFront>{};
}

size_t propagate_beam(std::vector<std::string> *cave, BeamFront start) {
    std::deque<BeamFront> beam_fronts{start};
    std::vector<std::bitset<4>> seen;
    auto const nrows{(*cave).size()};
    auto const ncols{(*cave).front().size()};
    seen.resize(nrows*ncols);
    for (auto s: seen) {s.reset();};

    while (beam_fronts.size() > 0) { 
        BeamFront bf = std::move(beam_fronts.back());
        beam_fronts.pop_back();
        seen[bf.i + bf.j * ncols].set((size_t) bf.dir);
        for (auto d: descendents(cave, bf))
        {
            if (d.i >= 0 && d.i < ncols && d.j >= 0 && d.j < nrows && 
                !seen[d.i+d.j*ncols][(size_t) d.dir]) beam_fronts.push_back(d);
        }
    }
    
    size_t t = 0;
    for (auto b: seen) {t += (size_t) b.any();};
    return t;
}

int main() {
    auto started = std::chrono::high_resolution_clock::now();
    std::vector<std::string> cave;
    //std::ifstream file("input/day16_example");
    std::ifstream file("input/day16");
    std::string line;

    while (std::getline(file, line))
    {
        cave.push_back(line);
    }
    auto sol_part1 = propagate_beam(&cave, BeamFront{0, 0, Direction::right});
    std::cout << "Part 1 solution: " << sol_part1 << "\n";

    size_t sol_part2 = 0;
    for (int j = 0; j < cave.size(); j++)
    {
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{0, j, Direction::right}));
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{(int) cave[0].size() - 1, j, Direction::left}));
    };
    for (int i = 0; i < cave[0].size(); i++)
    {
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{i, 0, Direction::down}));
        sol_part2 = std::max(sol_part2, propagate_beam(&cave, BeamFront{i, (int) cave.size() - 1, Direction::up}));
    };

    std::cout << "Part 2 solution: " << sol_part2 << "\n";
    auto done = std::chrono::high_resolution_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count() << "ms\n";

    return 0; 
}

