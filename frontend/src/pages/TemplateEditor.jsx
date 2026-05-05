import { useState, useEffect } from 'react';

const API = import.meta.env.VITE_API_URL || 'https://dmcashield-agency.vercel.app';

export default function TemplateEditor() {
  const [templates, setTemplates] = useState([]);
  const [selected, setSelected] = useState(null);
  const [editMode, setEditMode] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/templates`)
      .then(r => r.json())
      .then(d => { setTemplates(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const saveTemplate = async () => {
    await fetch(`${API}/api/templates/${selected.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(selected)
    });
    setEditMode(false);
  };

  const createNew = async () => {
    const res = await fetch(`${API}/api/templates`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'New Template', steps: [{ step: 1, delay_days: 0, angle: 'cold_intro', emotion_trigger: 'fear' }] })
    });
    const data = await res.json();
    setTemplates([...templates, { id: data.id, name: data.name, steps: [] }]);
  };

  if (loading) return <div className="p-6">Loading...</div>;

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold">📝 Email Template Editor</h1>
        <button onClick={createNew} className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
          + New Template
        </button>
      </div>

      <div className="grid grid-cols-3 gap-6">
        <div className="bg-gray-800 p-4 rounded-lg">
          <h2 className="text-lg font-bold mb-3">Templates</h2>
          <div className="space-y-2">
            {templates.map(t => (
              <div key={t.id} onClick={() => { setSelected(t); setEditMode(false); }}
                className={`p-3 rounded cursor-pointer ${selected?.id === t.id ? 'bg-blue-600' : 'bg-gray-700 hover:bg-gray-600'}`}>
                <p className="font-bold">{t.name}</p>
                <p className="text-sm text-gray-400">{t.steps?.length || 0} steps</p>
              </div>
            ))}
          </div>
        </div>

        <div className="col-span-2 bg-gray-800 p-4 rounded-lg">
          {selected ? (
            <>
              <div className="flex justify-between items-center mb-4">
                <input value={selected.name} onChange={e => setSelected({...selected, name: e.target.value})}
                  className="bg-gray-700 text-white p-2 rounded text-lg font-bold" disabled={!editMode} />
                <button onClick={() => editMode ? saveTemplate() : setEditMode(true)}
                  className="bg-green-600 text-white px-4 py-2 rounded">
                  {editMode ? 'Save' : 'Edit'}
                </button>
              </div>

              <div className="space-y-4">
                {selected.steps?.map((step, i) => (
                  <div key={i} className="bg-gray-700 p-4 rounded">
                    <div className="grid grid-cols-3 gap-4 mb-2">
                      <div>
                        <label className="text-gray-400 text-sm">Step</label>
                        <p className="font-bold">{step.step}</p>
                      </div>
                      <div>
                        <label className="text-gray-400 text-sm">Delay (days)</label>
                        <p>{step.delay_days}</p>
                      </div>
                      <div>
                        <label className="text-gray-400 text-sm">Emotion</label>
                        <p className="text-orange-400">{step.emotion_trigger}</p>
                      </div>
                    </div>
                    <div>
                      <label className="text-gray-400 text-sm">Angle</label>
                      <p className="text-blue-400">{step.angle}</p>
                    </div>
                  </div>
                ))}
              </div>

              {selected.steps?.length === 0 && (
                <p className="text-gray-400 text-center py-8">No steps yet - edit to add</p>
              )}
            </>
          ) : (
            <p className="text-gray-400 text-center py-8">Select a template to edit</p>
          )}
        </div>
      </div>
    </div>
  );
}