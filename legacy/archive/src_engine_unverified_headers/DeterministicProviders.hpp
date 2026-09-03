/**
 * @file DeterministicProviders.hpp
 * @brief Time and RNG abstraction interfaces for deterministic testing
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 4 - Observability & Telemetry
 * - Direct calls to std::chrono::system_clock::now() or rand() in business logic prohibited
 * - Timeouts and randomness must be injected via interfaces
 * - Allows deterministic time-traveling and reproducible tests
 */

#pragma once

#include <chrono>
#include <random>
#include <memory>
#include <functional>
#include <concepts>
#include <optional>
#include "engine/core/StrongTypes.hpp"

namespace omnicpp {
namespace core {

// ============================================================================
// Time Provider Interface
// ============================================================================

/**
 * @brief Concept for time provider types
 */
template<typename T>
concept TimeProvider = requires(T provider) {
    { provider.now() } -> std::same_as<std::chrono::steady_clock::time_point>;
    { provider.system_now() } -> std::same_as<std::chrono::system_clock::time_point>;
    { provider.elapsed() } -> std::same_as<std::chrono::nanoseconds>;
};

/**
 * @brief Interface for time abstraction
 * 
 * Allows deterministic testing by injecting mock time providers.
 * 
 * Usage:
 *   class MyService {
 *       ITimeProvider& time_;
 *   public:
 *       void doWork() {
 *           auto start = time_.now();
 *           // ... work ...
 *           auto elapsed = time_.now() - start;
 *       }
 *   };
 *   
 *   // Production:
 *   MyService service(SystemTimeProvider{});
 *   
 *   // Test:
 *   MockTimeProvider mock;
 *   mock.set_time(t1);
 *   MyService service(mock);
 */
class ITimeProvider {
public:
    virtual ~ITimeProvider() = default;
    
    /**
     * @brief Get current steady clock time (monotonic, for measurements)
     */
    [[nodiscard]] virtual std::chrono::steady_clock::time_point now() const = 0;
    
    /**
     * @brief Get current system clock time (wall clock, for timestamps)
     */
    [[nodiscard]] virtual std::chrono::system_clock::time_point system_now() const = 0;
    
    /**
     * @brief Get elapsed time since a reference point
     */
    [[nodiscard]] virtual std::chrono::nanoseconds elapsed() const = 0;
    
    /**
     * @brief Get Unix timestamp in milliseconds
     */
    [[nodiscard]] virtual int64_t unix_millis() const {
        return std::chrono::duration_cast<std::chrono::milliseconds>(
            system_now().time_since_epoch()
        ).count();
    }
    
    /**
     * @brief Get Unix timestamp in seconds
     */
    [[nodiscard]] virtual int64_t unix_seconds() const {
        return std::chrono::duration_cast<std::chrono::seconds>(
            system_now().time_since_epoch()
        ).count();
    }
};

/**
 * @brief Real system time provider (production use)
 */
class SystemTimeProvider : public ITimeProvider {
public:
    SystemTimeProvider() : start_(std::chrono::steady_clock::now()) {}
    
    [[nodiscard]] std::chrono::steady_clock::time_point now() const override {
        return std::chrono::steady_clock::now();
    }
    
    [[nodiscard]] std::chrono::system_clock::time_point system_now() const override {
        return std::chrono::system_clock::now();
    }
    
    [[nodiscard]] std::chrono::nanoseconds elapsed() const override {
        return std::chrono::steady_clock::now() - start_;
    }

private:
    std::chrono::steady_clock::time_point start_;
};

/**
 * @brief Mock time provider for deterministic testing
 * 
 * Usage:
 *   MockTimeProvider time;
 *   time.set_now(tp1);
 *   EXPECT_EQ(time.now(), tp1);
 *   time.advance(std::chrono::milliseconds(100));
 *   EXPECT_EQ(time.elapsed(), 100ms);
 */
class MockTimeProvider : public ITimeProvider {
public:
    MockTimeProvider() 
        : steady_now_(std::chrono::steady_clock::time_point{})
        , system_now_(std::chrono::system_clock::time_point{})
        , start_(steady_now_) {}
    
    explicit MockTimeProvider(
        std::chrono::steady_clock::time_point steady,
        std::chrono::system_clock::time_point system
    ) : steady_now_(steady), system_now_(system), start_(steady) {}
    
    [[nodiscard]] std::chrono::steady_clock::time_point now() const override {
        return steady_now_;
    }
    
    [[nodiscard]] std::chrono::system_clock::time_point system_now() const override {
        return system_now_;
    }
    
    [[nodiscard]] std::chrono::nanoseconds elapsed() const override {
        return steady_now_ - start_;
    }
    
    // Test manipulation methods
    
    /**
     * @brief Set the current steady time
     */
    void set_now(std::chrono::steady_clock::time_point tp) {
        steady_now_ = tp;
    }
    
    /**
     * @brief Set the current system time
     */
    void set_system_now(std::chrono::system_clock::time_point tp) {
        system_now_ = tp;
    }
    
    /**
     * @brief Advance time by a duration
     */
    template<typename Rep, typename Period>
    void advance(std::chrono::duration<Rep, Period> duration) {
        steady_now_ += std::chrono::duration_cast<std::chrono::steady_clock::duration>(duration);
        system_now_ += std::chrono::duration_cast<std::chrono::system_clock::duration>(duration);
    }
    
    /**
     * @brief Set time from Unix milliseconds
     */
    void set_unix_millis(int64_t millis) {
        system_now_ = std::chrono::system_clock::time_point{
            std::chrono::duration_cast<std::chrono::system_clock::duration>(
                std::chrono::milliseconds(millis)
            )
        };
    }
    
    /**
     * @brief Reset to initial state
     */
    void reset() {
        steady_now_ = std::chrono::steady_clock::time_point{};
        system_now_ = std::chrono::system_clock::time_point{};
        start_ = steady_now_;
    }

private:
    std::chrono::steady_clock::time_point steady_now_;
    std::chrono::system_clock::time_point system_now_;
    std::chrono::steady_clock::time_point start_;
};

// ============================================================================
// Random Provider Interface
// ============================================================================

/**
 * @brief Concept for random provider types
 */
template<typename T>
concept RandomProvider = requires(T provider) {
    { provider.next_uint32() } -> std::same_as<uint32_t>;
    { provider.next_uint64() } -> std::same_as<uint64_t>;
    { provider.next_double() } -> std::same_as<double>;
    { provider.next_int(0, 10) } -> std::same_as<int>;
};

/**
 * @brief Interface for random number abstraction
 * 
 * Allows deterministic testing by injecting seeded/fixed RNGs.
 * 
 * Usage:
 *   class GameLogic {
 *       IRandomProvider& rng_;
 *   public:
 *       bool criticalHit() {
 *           return rng_.next_double() < 0.1;
 *       }
 *   };
 *   
 *   // Production:
 *   GameLogic game(SystemRandomProvider{});
 *   
 *   // Test (deterministic):
 *   MockRandomProvider mock;
 *   mock.set_next_double(0.05);  // Force critical hit
 *   GameLogic game(mock);
 *   EXPECT_TRUE(game.criticalHit());
 */
class IRandomProvider {
public:
    virtual ~IRandomProvider() = default;
    
    /**
     * @brief Get random uint32_t
     */
    [[nodiscard]] virtual uint32_t next_uint32() = 0;
    
    /**
     * @brief Get random uint64_t
     */
    [[nodiscard]] virtual uint64_t next_uint64() = 0;
    
    /**
     * @brief Get random double in [0, 1)
     */
    [[nodiscard]] virtual double next_double() = 0;
    
    /**
     * @brief Get random float in [0, 1)
     */
    [[nodiscard]] virtual float next_float() = 0;
    
    /**
     * @brief Get random int in [min, max]
     */
    [[nodiscard]] virtual int next_int(int min, int max) = 0;
    
    /**
     * @brief Get random size_t in [min, max]
     */
    [[nodiscard]] virtual std::size_t next_size(std::size_t min, std::size_t max) = 0;
    
    /**
     * @brief Get random bool with given probability of true
     */
    [[nodiscard]] virtual bool next_bool(double probability = 0.5) = 0;
    
    /**
     * @brief Shuffle a container
     */
    template<typename RandomIt>
    void shuffle(RandomIt first, RandomIt last) {
        for (auto it = first + 1; it != last; ++it) {
            auto j = first + next_size(0, static_cast<std::size_t>(it - first));
            std::iter_swap(it, j);
        }
    }
};

/**
 * @brief Real random provider using std::random_device (production use)
 */
class SystemRandomProvider : public IRandomProvider {
public:
    SystemRandomProvider() : gen_(rd_()) {}
    
    explicit SystemRandomProvider(uint64_t seed) : gen_(seed) {}
    
    [[nodiscard]] uint32_t next_uint32() override {
        return uint_dist_(gen_);
    }
    
    [[nodiscard]] uint64_t next_uint64() override {
        return uint64_dist_(gen_);
    }
    
    [[nodiscard]] double next_double() override {
        return double_dist_(gen_);
    }
    
    [[nodiscard]] float next_float() override {
        return float_dist_(gen_);
    }
    
    [[nodiscard]] int next_int(int min, int max) override {
        std::uniform_int_distribution<int> dist(min, max);
        return dist(gen_);
    }
    
    [[nodiscard]] std::size_t next_size(std::size_t min, std::size_t max) override {
        std::uniform_int_distribution<std::size_t> dist(min, max);
        return dist(gen_);
    }
    
    [[nodiscard]] bool next_bool(double probability) override {
        std::bernoulli_distribution dist(probability);
        return dist(gen_);
    }
    
    /**
     * @brief Re-seed the generator
     */
    void seed(uint64_t seed) {
        gen_.seed(seed);
    }

private:
    std::random_device rd_;
    std::mt19937_64 gen_;
    std::uniform_int_distribution<uint32_t> uint_dist_{0, UINT32_MAX};
    std::uniform_int_distribution<uint64_t> uint64_dist_{0, UINT64_MAX};
    std::uniform_real_distribution<double> double_dist_{0.0, 1.0};
    std::uniform_real_distribution<float> float_dist_{0.0f, 1.0f};
};

/**
 * @brief Mock random provider for deterministic testing
 */
class MockRandomProvider : public IRandomProvider {
public:
    MockRandomProvider() = default;
    
    [[nodiscard]] uint32_t next_uint32() override {
        return pop_or_default(uint32_values_, default_uint32_);
    }
    
    [[nodiscard]] uint64_t next_uint64() override {
        return pop_or_default(uint64_values_, default_uint64_);
    }
    
    [[nodiscard]] double next_double() override {
        return pop_or_default(double_values_, default_double_);
    }
    
    [[nodiscard]] float next_float() override {
        return pop_or_default(float_values_, default_float_);
    }
    
    [[nodiscard]] int next_int(int min, int max) override {
        auto val = pop_or_default(int_values_, default_int_);
        return min + (val % (max - min + 1));
    }
    
    [[nodiscard]] std::size_t next_size(std::size_t min, std::size_t max) override {
        auto val = pop_or_default(size_values_, default_size_);
        return min + (val % (max - min + 1));
    }
    
    [[nodiscard]] bool next_bool(double /* probability */) override {
        return pop_or_default(bool_values_, default_bool_);
    }
    
    // Test manipulation methods
    
    void set_next_uint32(uint32_t val) { uint32_values_.push(val); }
    void set_next_uint64(uint64_t val) { uint64_values_.push(val); }
    void set_next_double(double val) { double_values_.push(val); }
    void set_next_float(float val) { float_values_.push(val); }
    void set_next_int(int val) { int_values_.push(val); }
    void set_next_size(std::size_t val) { size_values_.push(val); }
    void set_next_bool(bool val) { bool_values_.push(val); }
    
    void set_default_uint32(uint32_t val) { default_uint32_ = val; }
    void set_default_double(double val) { default_double_ = val; }
    void set_default_bool(bool val) { default_bool_ = val; }
    
    void reset() {
        uint32_values_ = {};
        uint64_values_ = {};
        double_values_ = {};
        float_values_ = {};
        int_values_ = {};
        size_values_ = {};
        bool_values_ = {};
        default_uint32_ = 0;
        default_uint64_ = 0;
        default_double_ = 0.0;
        default_float_ = 0.0f;
        default_int_ = 0;
        default_size_ = 0;
        default_bool_ = false;
    }

private:
    template<typename T>
    T pop_or_default(std::queue<T>& queue, T default_val) {
        if (queue.empty()) {
            return default_val;
        }
        T val = queue.front();
        queue.pop();
        return val;
    }
    
    std::queue<uint32_t> uint32_values_;
    std::queue<uint64_t> uint64_values_;
    std::queue<double> double_values_;
    std::queue<float> float_values_;
    std::queue<int> int_values_;
    std::queue<std::size_t> size_values_;
    std::queue<bool> bool_values_;
    
    uint32_t default_uint32_{0};
    uint64_t default_uint64_{0};
    double default_double_{0.0};
    float default_float_{0.0f};
    int default_int_{0};
    std::size_t default_size_{0};
    bool default_bool_{false};
};

// ============================================================================
// Seeded Random Provider (for reproducible runs)
// ============================================================================

/**
 * @brief Seeded random provider for reproducible production runs
 * 
 * Use when you need deterministic behavior in production (e.g., game replays)
 */
class SeededRandomProvider : public IRandomProvider {
public:
    explicit SeededRandomProvider(uint64_t seed) : gen_(seed), seed_(seed) {}
    
    [[nodiscard]] uint64_t seed() const noexcept { return seed_; }
    
    [[nodiscard]] uint32_t next_uint32() override {
        return uint_dist_(gen_);
    }
    
    [[nodiscard]] uint64_t next_uint64() override {
        return uint64_dist_(gen_);
    }
    
    [[nodiscard]] double next_double() override {
        return double_dist_(gen_);
    }
    
    [[nodiscard]] float next_float() override {
        return float_dist_(gen_);
    }
    
    [[nodiscard]] int next_int(int min, int max) override {
        std::uniform_int_distribution<int> dist(min, max);
        return dist(gen_);
    }
    
    [[nodiscard]] std::size_t next_size(std::size_t min, std::size_t max) override {
        std::uniform_int_distribution<std::size_t> dist(min, max);
        return dist(gen_);
    }
    
    [[nodiscard]] bool next_bool(double probability) override {
        std::bernoulli_distribution dist(probability);
        return dist(gen_);
    }
    
    void reseed(uint64_t seed) {
        seed_ = seed;
        gen_.seed(seed);
    }

private:
    std::mt19937_64 gen_;
    uint64_t seed_;
    std::uniform_int_distribution<uint32_t> uint_dist_{0, UINT32_MAX};
    std::uniform_int_distribution<uint64_t> uint64_dist_{0, UINT64_MAX};
    std::uniform_real_distribution<double> double_dist_{0.0, 1.0};
    std::uniform_real_distribution<float> float_dist_{0.0f, 1.0f};
};

} // namespace core
} // namespace omnicpp
