#include <chrono>
#include <iostream>
#include <vector>
#include <fstream>
#include "Eigen/Dense"
#include "helper.hpp"




class Hailstone
{
    public:
        Eigen::Vector3d v;
        Eigen::Vector3d p;
        Hailstone (const std::string line) 
        {
            std::vector<std::string> v_split, p_split, p_v_split;
            tokenize(line, " @ ", p_v_split);
            tokenize(p_v_split[0], ", ", p_split);
            tokenize(p_v_split[1], ", ", v_split);
            for (int i=0; i<3; i++)
            {
                v(i) = stod(v_split[i]);
                p(i) = stod(p_split[i]);
            }
        };
        bool paths_cross(const Hailstone &other, const double area_min, const double area_max) const
        {
            // p_1 + v_1 * t_1 = p_2 + v_2 * t_2
            // v_1 t_1 - v_2 * t_2 = p_2 - t_1
            Eigen::Matrix2d A;
            A(Eigen::all, 0) = v({0, 1});
            A(Eigen::all, 1) = -other.v({0, 1});
            if (abs(A.determinant()) < 1e-5) return false;
            Eigen::Vector2d t = A.colPivHouseholderQr().solve(other.p({0, 1}) - p({0, 1}));
            if (t(0) < 0.0 or t(1) < 0.0) return false;
            Eigen::Vector2d intercept = p({0, 1}) + v({0, 1})*t(0);
            return (area_min <= intercept(0) && intercept(0) <= area_max &&\
                    area_min <= intercept(1) && intercept(1) <= area_max);
        }
};


int main()
{
    auto started = std::chrono::high_resolution_clock::now();
    //std::ifstream file("input/day24_example");
    std::ifstream file("input/day24");
    std::string line;
    std::vector<Hailstone> hailstones;
    while (std::getline(file, line)) {
        hailstones.push_back(
            Hailstone(line)
        );
    };

    const double area_min = 200000000000000;
    const double area_max = 400000000000000;
    uint count = 0;

    for (size_t i = 0; i < hailstones.size() - 1; i++)
    {
        for (size_t j = i + 1; j < hailstones.size(); j++)
        {
            if (hailstones[i].paths_cross(hailstones[j], area_min, area_max)) count++;
        };
    };
 
    std::cout << "Part 1 solution: " << count << "\n";


    // for part 2:
    // p_i + v_i * t = p_s + v_s * t
    // (vx_i - vx_s) * t = (x_s - x_i)
    // t = (x_s - x_i) / (vx_i - vx_s) = (y_s - y_i) / (vy_i - vy_s)
    // (x_s - x_i) * (vy_i - vy_s) = (y_s - y_i) * (vx_i - vx_s)
    // x_s*vy_i - x_s*vy_s - x_i*vy_i + x_i*vy_s = y_s*vx_i - y_s*vx_s - y_i*vx_i + y_i*vx_s
    // x_s*vy_i - x_i*vy_i + x_i*vy_s -y_s*vx_i + y_i*vx_i - y_i*vx_s = -y_s*vx_s + x_s*vy_s
    // x_s*vy_j - x_j*vy_j + x_j*vy_s -y_s*vx_j + y_j*vx_j - y_j*vx_s = -y_s*vx_s + x_s*vy_s
    // x_s(vy_i - vy_j) + vy_s(x_i - x_j) - y_s(vx_i - vx_j) - vx_s(y_i - y_j) = x_i*vy_i - x_j*vy_j - y_i*vx_i + y_j*vx_j 
    // x_s(vz_i - vz_j) + vz_s(x_i - x_j) - z_s(vx_i - vx_j) - vx_s(z_i - z_j) = x_i*vz_i - x_j*vz_j - z_i*vx_i + z_j*vx_j 
    // y_s(vz_i - vz_j) + vz_s(y_i - y_j) - z_s(vy_i - vy_j) - vy_s(z_i - z_j) = y_i*vz_i - y_j*vz_j - z_i*vy_i + z_j*vy_j 
    /// | (vy_i - vy_j) -(vx_i - vx_j)       0        -(y_i - y_j)  (x_i - x_j)       0        |  
    /// | (vz_i - vz_j)      0         -(vx_i - vx_j) -(z_i - z_j)       0         (x_i - x_j) |  
    /// |       0        (vz_i - vz_j) -(vy_i - vy_j)       0      -(z_i - z_j)    (y_i - y_j) |      
    // 
    Eigen::Matrix<double, 6, 6> A;
    Eigen::Vector<double, 6> b;
    Eigen::Vector3d pj = hailstones[0].p;
    Eigen::Vector3d vj = hailstones[0].v;
    for (size_t i = 1; i < 3; i++)
    {
        Eigen::Vector3d pi = hailstones[i].p;
        Eigen::Vector3d vi = hailstones[i].v;
        Eigen::Vector3d dp = pi - pj;
        Eigen::Vector3d dv = vi - vj;
        A(3 * (i-1), 0) =  dv(1);
        A(3 * (i-1), 1) = -dv(0);
        A(3 * (i-1), 2) =    0.0;
        A(3 * (i-1), 3) = -dp(1);
        A(3 * (i-1), 4) =  dp(0);
        A(3 * (i-1), 5) =    0.0;
        b(3 * (i-1)) = pi(0) * vi(1) - pj(0) * vj(1) - pi(1) * vi(0) + pj(1) * vj(0);

        A(3 * (i-1) + 1, 0) =  dv(2);
        A(3 * (i-1) + 1, 1) =    0.0;
        A(3 * (i-1) + 1, 2) = -dv(0);
        A(3 * (i-1) + 1, 3) = -dp(2);
        A(3 * (i-1) + 1, 4) =    0.0;
        A(3 * (i-1) + 1, 5) =  dp(0);
        b(3 * (i-1) + 1) = pi(0) * vi(2) - pj(0) * vj(2) - pi(2) * vi(0) + pj(2) * vj(0);

        A(3 * (i-1) + 2, 0) =    0.0;
        A(3 * (i-1) + 2, 1) =  dv(2);
        A(3 * (i-1) + 2, 2) = -dv(1);
        A(3 * (i-1) + 2, 3) =    0.0;
        A(3 * (i-1) + 2, 4) = -dp(2);
        A(3 * (i-1) + 2, 5) =  dp(1);
        b(3 * (i-1) + 2) = pi(1) * vi(2) - pj(1) * vj(2) - pi(2) * vi(1) + pj(2) * vj(1);
    }
    Eigen::Vector<double, 6> x = A.colPivHouseholderQr().solve(b);
    
    std::cout << "Part 2 solution: " << static_cast<long long>(round(x({0, 1, 2}).sum())) << "\n";
    auto done = std::chrono::high_resolution_clock::now();
    std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count() << "ms\n";
} 