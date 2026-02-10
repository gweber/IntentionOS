import { useState } from 'react';
import { useConfigStore } from '../lib/configApi';

// Define type for profile
interface Profile {
    readonly id: string;
    readonly label: string;
    readonly provider: 'openai_compatible' | 'anthropic' | 'google';
    readonly base_url: string;
    readonly model: string;
    readonly api_key_env: string;
}

export function ConfigModal() {
  const [isOpen, setIsOpen] = useState(false);
  const { profiles, activeProfile, updateProfile, setActiveProfile } = useConfigStore();

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    const formData = new FormData(e.target as HTMLFormElement);
    const id = formData.get('id') as string;
    const label = formData.get('label') as string;
    const provider = formData.get('provider') as string;
    const baseUrl = formData.get('baseUrl') as string;
    const model = formData.get('model') as string;
    const apiKeyEnv = formData.get('apiKeyEnv') as string;

    // Validate provider
    const validProviders: string[] = ['openai_compatible', 'anthropic', 'google'];
    if (!validProviders.includes(provider)) {
      alert('Invalid provider selected. Must be one of: openai_compatible, anthropic, google.');
      return;
    }

    // Cast provider to correct type
    const providerType = provider as 'openai_compatible' | 'anthropic' | 'google';

    // Create profile object
    const profile: Profile = {
      id,
      label,
      provider: providerType,
      base_url: baseUrl,
      model,
      api_key_env: apiKeyEnv
    };

    // Update profile
    await updateProfile(id, profile);
    setIsOpen(false);
  };

  return (
    <>
      <button
        onClick={() => setIsOpen(true)}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition"
      >
        Manage LLM Profiles
      </button>

      {isOpen && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg w-96 max-w-90vw shadow-xl">
            <h2 className="text-xl font-bold mb-4">Manage LLM Profiles</h2>
            <form onSubmit={handleSave} className="space-y-4">
              <div>
                <label className="block text-sm font-medium mb-1">ID</label>
                <input
                  type="text"
                  name="id"
                  defaultValue={activeProfile?.id || ''}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Label</label>
                <input
                  type="text"
                  name="label"
                  defaultValue={activeProfile?.label || ''}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Provider</label>
                <select
                  name="provider"
                  defaultValue={activeProfile?.provider || ''}
                  className="w-full p-2 border rounded"
                  required
                >
                  <option value="openai_compatible">OpenAI Compatible</option>
                  <option value="anthropic">Anthropic</option>
                  <option value="google">Google</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Base URL</label>
                <input
                  type="text"
                  name="baseUrl"
                  defaultValue={activeProfile?.base_url || ''}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">Model</label>
                <input
                  type="text"
                  name="model"
                  defaultValue={activeProfile?.model || ''}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium mb-1">API Key Env Var</label>
                <input
                  type="text"
                  name="apiKeyEnv"
                  defaultValue={activeProfile?.api_key_env || ''}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              <div className="flex gap-2 justify-end mt-6">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default ConfigModal;
