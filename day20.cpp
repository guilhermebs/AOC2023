#include <chrono>
#include <iostream>
#include <vector>
#include <fstream>
#include <unordered_map>
#include <optional>
#include "helper.hpp"

enum Signal
{
    low,
    high,
};

class Module
{
public:
    std::string name;
    std::vector<std::string> destinations;
    virtual std::optional<Signal> handle_signal(Signal s, const std::string &source) = 0;
    virtual ~Module() {};
    void print()
    {
        std::string destinations_str;
        for (const auto &d : destinations) destinations_str += ", " + d;
        std::cout << name << " -> " << destinations_str.substr(2) << std::endl;
    }
};

class BroadcasterModule: public Module
{
public:
    BroadcasterModule (const std::string line)
    {
        name = line.substr(0, line.find(" -> "));
        tokenize(line, ", ", destinations, line.find(" -> ") + 4);
    };

    std::optional<Signal> handle_signal(Signal s, const std::string &source) override
    {

        return s;
    };

};

class FlipFlopModule: public Module
{
    bool m_on = false;
public:
    FlipFlopModule (const std::string line)
    {
        name = line.substr(1, line.find(" -> ") - 1);
        tokenize(line, ", ", destinations, line.find(" -> ") + 4);
    };

    std::optional<Signal> handle_signal(Signal s, const std::string &source) override
    {
        if (s == Signal::low)
        {
            m_on = !m_on;
            if (m_on) return Signal::high;
            else return Signal::low;
        }
        return {};
    };

};

class ConjunctionModule: public Module
{
    std::unordered_map<std::string, Signal> m_prev_signals;
public:
    ConjunctionModule (const std::string line)
    {
        name = line.substr(1, line.find(" -> ") - 1);
        tokenize(line, ", ", destinations, line.find(" -> ") + 4);
    };

    std::optional<Signal> handle_signal(Signal s, const std::string &source) override
    {
        m_prev_signals[source] = s;
        for (auto& [_, value]: m_prev_signals)
        {
            if (value != Signal::high) return Signal::high;
        }
        return Signal::low;
    };

    void register_incomming(const std::string &incoming)
    {
        m_prev_signals[incoming] = Signal::low;
    };

};


class ModuleConfig
{
private:
    std::unordered_map<std::string, std::unique_ptr<Module>> m_modules;
public:
    ModuleConfig(std::string fn)
    {
        std::ifstream file(fn);
        std::string line;
        while (std::getline(file, line))
        {
            std::string module_name = line.substr(1, line.find(" -> ") - 1);
            std::unique_ptr<Module> new_module;
            if (line[0] == 'b')
            {
                m_modules['b' + module_name] = std::make_unique<BroadcasterModule>(line);
            } else if (line[0] == '%')
            {
                m_modules[module_name] = std::make_unique<FlipFlopModule>(line);
            } else if (line[0] == '&')
            {
                m_modules[module_name] = std::make_unique<ConjunctionModule>(line);
            }
        }
        // Register all incomming connections to conjunction modeules
        for (auto &[_, m]: m_modules) {
            for (auto dest_name: m->destinations) {
                if (m_modules.contains(dest_name)) {
                    ConjunctionModule* cm = dynamic_cast<ConjunctionModule*>(m_modules[dest_name].get());
                    if (cm != nullptr) {
                        cm->register_incomming(m->name);
                    }
                }
            }
        }
    }

    std::pair<uint, uint> press_button()
    {
        std::deque<std::tuple<Signal, std::string, std::string>> to_process = {{Signal::low, "broadcaster", "button"}};
        uint count_low = 0;
        uint count_high = 0;
        while (to_process.size() > 0)
        {
            auto [signal, dest, source] = std::move(to_process.back());
            //std::cout << source << "-" << signal << ">" << dest << std::endl;
            to_process.pop_back();
            count_low += signal == Signal::low;
            count_high += signal == Signal::high;
            if (m_modules.contains(dest))
            {
                if (auto new_signal = m_modules[dest]->handle_signal(signal, source))
                {
                    for (auto new_dest: m_modules[dest]->destinations)
                        to_process.push_front(std::make_tuple(*new_signal, new_dest, dest));
                }
            }
        }
        return std::make_pair(count_low, count_high);
        
    }
};


int main()
{
    auto started = std::chrono::high_resolution_clock::now();
    auto module_config = ModuleConfig("input/day20");
    //auto module_config = ModuleConfig("input/day20_example1");
    uint count_low = 0;
    uint count_high = 0;
    for (size_t i = 0; i < 1000; i++)
    {
        auto [l, h] = module_config.press_button();
        count_low += l;
        count_high += h;
        //std::cout << l << ", " << h << std::endl;
    }
    auto done = std::chrono::high_resolution_clock::now();
    std::cout << "Part 1 solution: " << count_low * count_high << std::endl;
    std::cout << std::chrono::duration_cast<std::chrono::milliseconds>(done-started).count() << "ms\n";
} 