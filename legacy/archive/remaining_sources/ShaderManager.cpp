#include "Vulkan/ShaderManager.hpp"
#include <QLoggingCategory>
#include <fstream>
#include <stdexcept>

Q_LOGGING_CATEGORY(logShaderManager, "omnicpp.shadermanager")

namespace OmniCpp {

ShaderManager::ShaderManager()
    : m_device(VK_NULL_HANDLE)
{
}

ShaderManager::~ShaderManager()
{
    shutdown();
}

bool ShaderManager::initialize(VkDevice device)
{
    qCDebug(logShaderManager) << "Initializing shader manager...";

    m_device = device;

    qCDebug(logShaderManager) << "Shader manager initialized successfully";
    return true;
}

void ShaderManager::shutdown()
{
    qCDebug(logShaderManager) << "Shutting down shader manager...";

    m_device = VK_NULL_HANDLE;

    qCDebug(logShaderManager) << "Shader manager shut down";
}

VkShaderModule ShaderManager::loadShader(const std::string& filename)
{
    qCDebug(logShaderManager) << "Loading shader:" << QString::fromStdString(filename);

    // Read shader file
    std::vector<char> code = readFile(filename);

    // Create shader module
    VkShaderModuleCreateInfo createInfo{};
    createInfo.sType = VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO;
    createInfo.codeSize = code.size();
    createInfo.pCode = reinterpret_cast<const uint32_t*>(code.data());

    VkShaderModule shaderModule;
    if (vkCreateShaderModule(m_device, &createInfo, nullptr, &shaderModule) != VK_SUCCESS) {
        qCCritical(logShaderManager) << "Failed to create shader module for:" << QString::fromStdString(filename);
        return VK_NULL_HANDLE;
    }

    qCDebug(logShaderManager) << "Shader loaded successfully:" << QString::fromStdString(filename);
    return shaderModule;
}

std::vector<char> ShaderManager::readFile(const std::string& filename)
{
    // Open file
    std::ifstream file(filename, std::ios::ate | std::ios::binary);

    if (!file.is_open()) {
        qCCritical(logShaderManager) << "Failed to open file:" << QString::fromStdString(filename);
        throw std::runtime_error("Failed to open file: " + filename);
    }

    // Get file size
    size_t fileSize = static_cast<size_t>(file.tellg());
    std::vector<char> buffer(fileSize);

    // Read file
    file.seekg(0);
    file.read(buffer.data(), fileSize);
    file.close();

    return buffer;
}

} // namespace OmniCpp
