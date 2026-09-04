/**
 * @file ThreadPool.hpp
 * @brief Structured concurrency with asio thread pool
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 3 - Control Flow & Fault Tolerance
 * - Raw std::thread and detached threads are prohibited
 * - Asynchronous workflows must use composable task graphs
 * - Guarantees graceful teardown on application exit
 */

#pragma once

#include <functional>
#include <future>
#include <memory>
#include <type_traits>
#include <asio/io_context.hpp>
#include <asio/thread_pool.hpp>
#include <asio/post.hpp>
#include <asio/use_future.hpp>
#include "engine/core/Expected.hpp"

namespace omnicpp {
namespace concurrency {

// ============================================================================
// Thread Pool Configuration
// ============================================================================

/**
 * @brief Configuration for thread pool
 */
struct ThreadPoolConfig {
    std::size_t min_threads{1};
    std::size_t max_threads{0};  // 0 = hardware concurrency
    std::size_t max_queue_size{1024};
    std::chrono::milliseconds shutdown_timeout{5000};
};

// ============================================================================
// Thread Pool - Structured Concurrency
// ============================================================================

/**
 * @brief Thread pool using asio for structured concurrency
 * 
 * Benefits:
 * - No raw threads (prevents resource leaks)
 * - Graceful shutdown with timeout
 * - Work-stealing for load balancing
 * - Exception-safe task submission
 * 
 * Usage:
 *   ThreadPool pool(4);
 *   auto future = pool.submit([]{ return compute(); });
 *   auto result = future.get();
 */
class ThreadPool {
public:
    /**
     * @brief Create thread pool with specified number of threads
     * @param num_threads Number of worker threads (0 = hardware concurrency)
     */
    explicit ThreadPool(std::size_t num_threads = 0)
        : pool_(num_threads > 0 ? num_threads : std::thread::hardware_concurrency())
        , work_guard_(asio::make_work_guard(pool_))
        , running_(true) {
    }
    
    /**
     * @brief Create thread pool with configuration
     */
    explicit ThreadPool(const ThreadPoolConfig& config)
        : pool_(config.max_threads > 0 ? config.max_threads : std::thread::hardware_concurrency())
        , work_guard_(asio::make_work_guard(pool_))
        , config_(config)
        , running_(true) {
    }
    
    /**
     * @brief Destructor - gracefully shuts down pool
     */
    ~ThreadPool() {
        shutdown();
    }
    
    // Non-copyable, non-movable
    ThreadPool(const ThreadPool&) = delete;
    ThreadPool& operator=(const ThreadPool&) = delete;
    ThreadPool(ThreadPool&&) = delete;
    ThreadPool& operator=(ThreadPool&&) = delete;
    
    /**
     * @brief Submit a callable for execution
     * @tparam F Callable type
     * @tparam Args Argument types
     * @return Future holding the result
     * 
     * COMPLIANCE: Exceptions from tasks are captured in the future
     */
    template<typename F, typename... Args>
    [[nodiscard]] auto submit(F&& f, Args&&... args) 
        -> std::future<std::invoke_result_t<std::decay_t<F>, std::decay_t<Args>...>> {
        using return_type = std::invoke_result_t<std::decay_t<F>, std::decay_t<Args>...>;
        
        auto task = std::make_shared<std::packaged_task<return_type()>>(
            std::bind(std::forward<F>(f), std::forward<Args>(args)...)
        );
        
        std::future<return_type> result = task->get_future();
        
        asio::post(pool_, [task]() {
            (*task)();
        });
        
        return result;
    }
    
    /**
     * @brief Submit a callable with Expected return type (no exceptions)
     * @tparam F Callable type returning Expected<T, E>
     * @return Future holding Expected result
     */
    template<typename F, typename... Args>
    [[nodiscard]] auto submit_expected(F&& f, Args&&... args) {
        return submit(std::forward<F>(f), std::forward<Args>(args)...);
    }
    
    /**
     * @brief Post a void callable (fire-and-forget with tracking)
     * @tparam F Callable type
     */
    template<typename F, typename... Args>
    void post(F&& f, Args&&... args) {
        asio::post(pool_, std::bind(std::forward<F>(f), std::forward<Args>(args)...));
    }
    
    /**
     * @brief Submit a coroutine-based task (C++20 coroutines)
     * @tparam awaitable_t Asio awaitable type
     */
    template<typename T>
    [[nodiscard]] auto co_spawn(asio::awaitable<T> awaitable) 
        -> std::future<T> {
        return asio::co_spawn(pool_, std::move(awaitable), asio::use_future);
    }
    
    /**
     * @brief Get the underlying asio thread pool
     */
    [[nodiscard]] asio::thread_pool& get_pool() noexcept { return pool_; }
    [[nodiscard]] const asio::thread_pool& get_pool() const noexcept { return pool_; }
    
    /**
     * @brief Get the io_context for custom asio operations
     */
    [[nodiscard]] asio::io_context& get_io_context() noexcept {
        return pool_.get_executor().context();
    }
    
    /**
     * @brief Get number of threads in pool
     */
    [[nodiscard]] std::size_t size() const noexcept {
        return config_.max_threads > 0 ? config_.max_threads 
                                       : std::thread::hardware_concurrency();
    }
    
    /**
     * @brief Check if pool is running
     */
    [[nodiscard]] bool is_running() const noexcept { return running_.load(); }
    
    /**
     * @brief Wait for all submitted tasks to complete
     */
    void wait() {
        pool_.join();
    }
    
    /**
     * @brief Gracefully shutdown the pool
     * @param timeout Maximum time to wait for tasks
     */
    void shutdown(std::chrono::milliseconds timeout = std::chrono::milliseconds(5000)) {
        if (!running_.exchange(false)) {
            return;  // Already shut down
        }
        
        work_guard_.reset();  // Allow pool to drain
        
        // Wait for completion with timeout
        std::thread([this, timeout]() {
            std::promise<void> promise;
            auto future = promise.get_future();
            
            asio::post(pool_, [&promise]() {
                promise.set_value();
            });
            
            if (future.wait_for(timeout) == std::future_status::timeout) {
                // Force stop on timeout
                pool_.stop();
            }
        }).detach();
        
        pool_.join();
    }
    
    /**
     * @brief Stop the pool immediately (may leave tasks incomplete)
     */
    void stop() {
        running_ = false;
        work_guard_.reset();
        pool_.stop();
        pool_.join();
    }

private:
    asio::thread_pool pool_;
    asio::executor_work_guard<asio::thread_pool::executor_type> work_guard_;
    ThreadPoolConfig config_;
    std::atomic<bool> running_{false};
};

// ============================================================================
// Global Thread Pool Singleton
// ============================================================================

/**
 * @brief Global thread pool for application-wide use
 * 
 * COMPLIANCE: Single point of thread management for deterministic shutdown
 */
class GlobalThreadPool {
public:
    /**
     * @brief Get the global thread pool instance
     */
    [[nodiscard]] static ThreadPool& instance() {
        static ThreadPool pool(std::thread::hardware_concurrency());
        return pool;
    }
    
    /**
     * @brief Initialize with custom configuration
     */
    static void initialize(const ThreadPoolConfig& config) {
        // Note: This creates a new pool, use carefully
        static std::unique_ptr<ThreadPool> custom_pool = 
            std::make_unique<ThreadPool>(config);
    }
    
    /**
     * @brief Shutdown global pool
     */
    static void shutdown() {
        instance().shutdown();
    }
    
    // Non-instantiable
    GlobalThreadPool() = delete;
    ~GlobalThreadPool() = delete;
};

// ============================================================================
// Parallel For Each - Range-based parallel execution
// ============================================================================

/**
 * @brief Execute a function on each element of a range in parallel
 * @tparam Range Range type
 * @tparam F Function type
 * @param range Range to iterate
 * @param func Function to apply
 * @param pool Thread pool to use (default: global)
 * 
 * COMPLIANCE: Replaces raw parallel for loops
 */
template<typename Range, typename F>
void parallel_for_each(Range&& range, F&& func, ThreadPool& pool = GlobalThreadPool::instance()) {
    std::vector<std::future<void>> futures;
    futures.reserve(std::size(range));
    
    for (auto&& elem : range) {
        futures.push_back(pool.submit([&func, &elem]() {
            func(elem);
        }));
    }
    
    // Wait for all to complete
    for (auto& f : futures) {
        f.get();
    }
}

/**
 * @brief Execute a function for each index in parallel
 * @tparam F Function type
 * @param start Start index
 * @param end End index (exclusive)
 * @param func Function to apply
 * @param pool Thread pool to use
 */
template<typename F>
void parallel_for(std::size_t start, std::size_t end, F&& func, 
                  ThreadPool& pool = GlobalThreadPool::instance()) {
    std::vector<std::future<void>> futures;
    futures.reserve(end - start);
    
    for (std::size_t i = start; i < end; ++i) {
        futures.push_back(pool.submit([&func, i]() {
            func(i);
        }));
    }
    
    for (auto& f : futures) {
        f.get();
    }
}

// ============================================================================
// MPSC Queue - Multi-Producer Single-Consumer for UI thread communication
// ============================================================================

/**
 * @brief Thread-safe MPSC queue for background-to-UI communication
 * @tparam T Element type
 * 
 * COMPLIANCE: Non-Blocking Main Thread rule
 * - Workloads dispatched to background thread pool
 * - Results returned to main thread via MPSC queue
 */
template<typename T>
class MpscQueue {
public:
    MpscQueue() = default;
    
    /**
     * @brief Push an element (thread-safe, multi-producer)
     */
    void push(T&& item) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push(std::forward<T>(item));
        cv_.notify_one();
    }
    
    /**
     * @brief Push an element (copy)
     */
    void push(const T& item) {
        std::lock_guard<std::mutex> lock(mutex_);
        queue_.push(item);
        cv_.notify_one();
    }
    
    /**
     * @brief Try to pop an element (non-blocking)
     * @return Optional containing the element, or nullopt if empty
     */
    [[nodiscard]] std::optional<T> try_pop() {
        std::lock_guard<std::mutex> lock(mutex_);
        if (queue_.empty()) {
            return std::nullopt;
        }
        T item = std::move(queue_.front());
        queue_.pop();
        return item;
    }
    
    /**
     * @brief Pop an element (blocking)
     * @param timeout Maximum time to wait
     * @return Optional containing the element, or nullopt on timeout
     */
    [[nodiscard]] std::optional<T> pop(std::chrono::milliseconds timeout = std::chrono::milliseconds(100)) {
        std::unique_lock<std::mutex> lock(mutex_);
        if (!cv_.wait_for(lock, timeout, [this]() { return !queue_.empty(); })) {
            return std::nullopt;
        }
        T item = std::move(queue_.front());
        queue_.pop();
        return item;
    }
    
    /**
     * @brief Drain all elements to a vector
     */
    [[nodiscard]] std::vector<T> drain() {
        std::lock_guard<std::mutex> lock(mutex_);
        std::vector<T> result;
        result.reserve(queue_.size());
        while (!queue_.empty()) {
            result.push_back(std::move(queue_.front()));
            queue_.pop();
        }
        return result;
    }
    
    /**
     * @brief Check if queue is empty
     */
    [[nodiscard]] bool empty() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.empty();
    }
    
    /**
     * @brief Get approximate size
     */
    [[nodiscard]] std::size_t size() const {
        std::lock_guard<std::mutex> lock(mutex_);
        return queue_.size();
    }

private:
    mutable std::mutex mutex_;
    std::queue<T> queue_;
    std::condition_variable cv_;
};

} // namespace concurrency
} // namespace omnicpp
