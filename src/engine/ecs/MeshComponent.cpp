#include "engine/ecs/MeshComponent.hpp"
#include "engine/logging/Log.hpp"

namespace omnicpp {
namespace ecs {

MeshComponent::MeshComponent(uint64_t entity_id)
    : Component(entity_id) {
    omnicpp::log::debug("MeshComponent: Created mesh component for entity {}", entity_id);
}

MeshComponent::MeshComponent(uint64_t entity_id,
                               Mesh* mesh,
                               Material* material)
    : Component(entity_id)
    , m_mesh(mesh)
    , m_material(material) {
    omnicpp::log::debug("MeshComponent: Created mesh component for entity {} with mesh and material", entity_id);
}

} // namespace ecs
} // namespace omnicpp
