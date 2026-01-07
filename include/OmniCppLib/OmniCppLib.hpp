#pragma once

#include <OmniCppLib/version.h> // first configuration will create this file
#include <filesystem>
#include <string>

// Public API

namespace omnicpp {
  // Version information
  inline namespace v1 {

    class OmniCppLib {
    private:
      const std::string libName_ = "OmniCppLib v." OMNICPPLIB_VERSION;
      std::filesystem::path assetsPath_;
      bool isInitialized_ = false;

    public:
      OmniCppLib ();
      explicit OmniCppLib (const std::filesystem::path& assetsPath);
      ~OmniCppLib ();

      // Rule of 5 for better resource management
      OmniCppLib (const OmniCppLib& other) = delete;
      OmniCppLib& operator= (const OmniCppLib& other) = delete;
      OmniCppLib (OmniCppLib&& other) noexcept;
      OmniCppLib& operator= (OmniCppLib&& other) noexcept;

      // Public interface
      [[nodiscard]] bool isInitialized () const noexcept {
        return isInitialized_;
      }
      [[nodiscard]] const std::filesystem::path& getAssetsPath () const noexcept {
        return assetsPath_;
      }
    };

  } // namespace v1
} // namespace omnicpp

// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
