/**
 * @file Telemetry.hpp
 * @brief OpenTelemetry integration for distributed tracing
 * @version 1.0.0
 * 
 * COMPLIANCE: Phase 4 - Observability & Telemetry
 * - Telemetry must not be siloed to stdout
 * - Distributed tracing (Spans, Trace IDs) must be exported
 * - Supports OTLP protocol for centralized collectors
 */

#pragma once

#include <chrono>
#include <memory>
#include <string>
#include <string_view>
#include <unordered_map>
#include <mutex>
#include <atomic>
#include <functional>
#include <optional>
#include <span>
#include <fmt/format.h>
#include "engine/logging/spdlog_shim.hpp"

namespace omnicpp {
namespace telemetry {

// ============================================================================
// Trace Context
// ============================================================================

/**
 * @brief Represents a 128-bit trace ID
 */
struct TraceId {
    std::array<uint8_t, 16> data{};
    
    [[nodiscard]] std::string to_hex() const;
    [[nodiscard]] bool is_valid() const noexcept;
    static TraceId generate();
    static TraceId invalid() { return {}; }
};

/**
 * @brief Represents a 64-bit span ID
 */
struct SpanId {
    std::array<uint8_t, 8> data{};
    
    [[nodiscard]] std::string to_hex() const;
    [[nodiscard]] bool is_valid() const noexcept;
    static SpanId generate();
    static SpanId invalid() { return {}; }
};

/**
 * @brief Span kind enumeration
 */
enum class SpanKind {
    Internal,       // Internal span within the service
    Server,         // Server-side span (receiving request)
    Client,         // Client-side span (making request)
    Producer,       // Producer of a message
    Consumer        // Consumer of a message
};

/**
 * @brief Span status codes
 */
enum class StatusCode {
    Unset,          // Default, not set
    Ok,             // Operation completed successfully
    Error           // Operation encountered an error
};

/**
 * @brief Attribute value type
 */
using AttributeValue = std::variant<
    std::string,
    int64_t,
    double,
    bool,
    std::span<const uint8_t>
>;

/**
 * @brief Span attributes (key-value pairs)
 */
using SpanAttributes = std::unordered_map<std::string, AttributeValue>;

// ============================================================================
// Span
// ============================================================================

/**
 * @brief Represents a unit of work in a trace
 */
class Span {
public:
    /**
     * @brief Create a new span
     * @param name Span name
     * @param kind Span kind
     * @param trace_id Parent trace ID
     * @param parent_span_id Parent span ID (optional)
     */
    Span(std::string name, SpanKind kind, 
         TraceId trace_id, 
         std::optional<SpanId> parent_span_id = std::nullopt);
    
    ~Span();
    
    // Non-copyable, movable
    Span(const Span&) = delete;
    Span& operator=(const Span&) = delete;
    Span(Span&&) noexcept;
    Span& operator=(Span&&) noexcept;
    
    /**
     * @brief Add an attribute to the span
     */
    template<typename T>
    void set_attribute(std::string_view key, T&& value) {
        std::lock_guard<std::mutex> lock(mutex_);
        attributes_[std::string(key)] = AttributeValue(std::forward<T>(value));
    }
    
    /**
     * @brief Add an event to the span
     */
    void add_event(std::string_view name, 
                   const SpanAttributes& attributes = {});
    
    /**
     * @brief Set span status
     */
    void set_status(StatusCode code, std::string_view description = "");
    
    /**
     * @brief Record an exception
     */
    void record_exception(std::string_view type, 
                          std::string_view message,
                          std::string_view stacktrace = "");
    
    /**
     * @brief End the span
     */
    void end();
    
    /**
     * @brief Check if span has ended
     */
    [[nodiscard]] bool has_ended() const noexcept { return ended_.load(); }
    
    /**
     * @brief Get span ID
     */
    [[nodiscard]] SpanId span_id() const noexcept { return span_id_; }
    
    /**
     * @brief Get trace ID
     */
    [[nodiscard]] TraceId trace_id() const noexcept { return trace_id_; }
    
    /**
     * @brief Get parent span ID
     */
    [[nodiscard]] std::optional<SpanId> parent_span_id() const noexcept { 
        return parent_span_id_; 
    }
    
    /**
     * @brief Get span name
     */
    [[nodiscard]] const std::string& name() const noexcept { return name_; }
    
    /**
     * @brief Get span duration
     */
    [[nodiscard]] std::chrono::nanoseconds duration() const noexcept;
    
    /**
     * @brief Create a child span
     */
    [[nodiscard]] Span create_child(std::string_view child_name, SpanKind kind = SpanKind::Internal);

private:
    std::string name_;
    SpanKind kind_;
    TraceId trace_id_;
    SpanId span_id_;
    std::optional<SpanId> parent_span_id_;
    
    std::chrono::steady_clock::time_point start_time_;
    std::chrono::steady_clock::time_point end_time_;
    
    SpanAttributes attributes_;
    std::vector<std::pair<std::string, SpanAttributes>> events_;
    
    StatusCode status_{StatusCode::Unset};
    std::string status_description_;
    
    std::atomic<bool> ended_{false};
    mutable std::mutex mutex_;
};

// ============================================================================
// Tracer
// ============================================================================

/**
 * @brief Tracer interface for creating spans
 */
class Tracer {
public:
    virtual ~Tracer() = default;
    
    /**
     * @brief Start a new span
     */
    [[nodiscard]] virtual Span start_span(
        std::string_view name,
        SpanKind kind = SpanKind::Internal,
        const Span* parent = nullptr) = 0;
    
    /**
     * @brief Start a new span with explicit trace context
     */
    [[nodiscard]] virtual Span start_span(
        std::string_view name,
        SpanKind kind,
        TraceId trace_id,
        std::optional<SpanId> parent_span_id) = 0;
    
    /**
     * @brief Get the current active span (if any)
     */
    [[nodiscard]] virtual Span* get_active_span() = 0;
    
    /**
     * @brief Get tracer name
     */
    [[nodiscard]] virtual std::string_view name() const = 0;
};

/**
 * @brief TracerProvider for managing tracers
 */
class TracerProvider {
public:
    virtual ~TracerProvider() = default;
    
    /**
     * @brief Get or create a tracer
     */
    [[nodiscard]] virtual std::shared_ptr<Tracer> get_tracer(
        std::string_view name,
        std::string_view version = "") = 0;
    
    /**
     * @brief Force flush of all pending spans
     */
    virtual void force_flush(std::chrono::milliseconds timeout = std::chrono::milliseconds(5000)) = 0;
    
    /**
     * @brief Shutdown the provider
     */
    virtual void shutdown() = 0;
};

// ============================================================================
// OTLP Exporter
// ============================================================================

/**
 * @brief Configuration for OTLP exporter
 */
struct OtlpExporterConfig {
    std::string endpoint{"localhost:4317"};
    std::chrono::milliseconds timeout{10000};
    bool use_ssl{false};
    std::string ssl_cert_path;
    std::unordered_map<std::string, std::string> headers;
};

/**
 * @brief Span data for export
 */
struct SpanData {
    std::string name;
    TraceId trace_id;
    SpanId span_id;
    std::optional<SpanId> parent_span_id;
    SpanKind kind;
    std::chrono::nanoseconds start_time;  // Unix nanoseconds
    std::chrono::nanoseconds duration;
    SpanAttributes attributes;
    StatusCode status;
    std::string status_description;
};

/**
 * @brief Exporter interface for span data
 */
class SpanExporter {
public:
    virtual ~SpanExporter() = default;
    
    /**
     * @brief Export spans to the backend
     * @return true if successful
     */
    virtual bool export_spans(std::span<const SpanData> spans) = 0;
    
    /**
     * @brief Force flush pending exports
     */
    virtual void force_flush() = 0;
    
    /**
     * @brief Shutdown the exporter
     */
    virtual void shutdown() = 0;
};

// ============================================================================
// OpenTelemetry Manager
// ============================================================================

/**
 * @brief Configuration for telemetry system
 */
struct TelemetryConfig {
    bool enabled{true};
    std::string service_name{"omnicpp-engine"};
    std::string service_version{"1.0.0"};
    std::string environment{"development"};
    
    // Sampling configuration
    double sampling_rate{1.0};  // 1.0 = 100%
    
    // OTLP configuration
    OtlpExporterConfig otlp_config;
    
    // Batch export configuration
    size_t batch_size{512};
    std::chrono::milliseconds batch_timeout{5000};
    size_t max_queue_size{2048};
};

/**
 * @brief Main telemetry manager
 */
class TelemetryManager {
public:
    TelemetryManager();
    ~TelemetryManager();
    
    // Non-copyable, non-movable
    TelemetryManager(const TelemetryManager&) = delete;
    TelemetryManager& operator=(const TelemetryManager&) = delete;
    TelemetryManager(TelemetryManager&&) = delete;
    TelemetryManager& operator=(TelemetryManager&&) = delete;
    
    /**
     * @brief Initialize the telemetry system
     */
    bool initialize(const TelemetryConfig& config);
    
    /**
     * @brief Shutdown the telemetry system
     */
    void shutdown();
    
    /**
     * @brief Get a tracer by name
     */
    [[nodiscard]] std::shared_ptr<Tracer> get_tracer(
        std::string_view name,
        std::string_view version = "");
    
    /**
     * @brief Start a root span
     */
    [[nodiscard]] Span start_span(std::string_view name, SpanKind kind = SpanKind::Internal);
    
    /**
     * @brief Start a child span
     */
    [[nodiscard]] Span start_span(std::string_view name, const Span& parent);
    
    /**
     * @brief Get current trace context (for propagation)
     */
    [[nodiscard]] std::pair<TraceId, std::optional<SpanId>> get_current_context() const;
    
    /**
     * @brief Set trace context from external source (e.g., incoming request)
     */
    void set_context(TraceId trace_id, SpanId parent_span_id);
    
    /**
     * @brief Force flush all pending spans
     */
    void force_flush();
    
    /**
     * @brief Check if telemetry is enabled
     */
    [[nodiscard]] bool is_enabled() const noexcept { return enabled_.load(); }
    
    /**
     * @brief Get service name
     */
    [[nodiscard]] const std::string& service_name() const noexcept { return config_.service_name; }
    
    /**
     * @brief Add a global attribute to all spans
     */
    void add_global_attribute(std::string_view key, const AttributeValue& value);

private:
    struct Impl;
    std::unique_ptr<Impl> impl_;
    
    TelemetryConfig config_;
    std::atomic<bool> enabled_{false};
    std::atomic<bool> initialized_{false};
};

// ============================================================================
// Scoped Span Helper
// ============================================================================

/**
 * * @brief RAII wrapper for spans
 * 
 * Usage:
 *   {
 *       ScopedSpan span(tracer, "process_frame");
 *       span.set_attribute("frame_number", 42);
 *       // ... do work ...
 *   }  // Span automatically ends
 */
class ScopedSpan {
public:
    explicit ScopedSpan(Span span) : span_(std::move(span)) {}
    ~ScopedSpan() { if (!span_.has_ended()) span_.end(); }
    
    ScopedSpan(const ScopedSpan&) = delete;
    ScopedSpan& operator=(const ScopedSpan&) = delete;
    ScopedSpan(ScopedSpan&&) = default;
    ScopedSpan& operator=(ScopedSpan&&) = default;
    
    Span* operator->() { return &span_; }
    const Span* operator->() const { return &span_; }
    
    Span& get() { return span_; }
    const Span& get() const { return span_; }

private:
    Span span_;
};

// ============================================================================
// Convenience Macros
// ============================================================================

/**
 * @brief Create a scoped span with automatic naming
 */
#define OMNICPP_SPAN(name) \
    omnicpp::telemetry::ScopedSpan _scoped_span_##__LINE__( \
        omnicpp::telemetry::TelemetryManager::instance().start_span(name))

/**
 * @brief Create a scoped span with attributes
 */
#define OMNICPP_SPAN_WITH_ATTRS(name, ...) \
    auto _span_##__LINE__ = omnicpp::telemetry::TelemetryManager::instance().start_span(name); \
    _span_##__LINE__.set_attributes(__VA_ARGS__); \
    omnicpp::telemetry::ScopedSpan _scoped_span_##__LINE__(std::move(_span_##__LINE__))

/**
 * @brief Add event to current span
 */
#define OMNICPP_ADD_EVENT(name, ...) \
    do { \
        auto* span = omnicpp::telemetry::TelemetryManager::instance().get_active_span(); \
        if (span) { span->add_event(name, __VA_ARGS__); } \
    } while(0)

/**
 * @brief Set attribute on current span
 */
#define OMNICPP_SET_ATTR(key, value) \
    do { \
        auto* span = omnicpp::telemetry::TelemetryManager::instance().get_active_span(); \
        if (span) { span->set_attribute(key, value); } \
    } while(0)

} // namespace telemetry
} // namespace omnicpp
