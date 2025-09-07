const api = path => `/api${path}`;

async function apiFetch(path, opts){
  const res = await fetch(api(path), opts);
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  return res.status === 204 ? null : res.json();
}

// DOM
const newTodo = document.getElementById('newTodo');
const list = document.getElementById('todoList');
const stats = document.getElementById('stats');
const clearDoneBtn = document.getElementById('clearDone');

async function load(){
  try {
    const todos = await apiFetch('/todos');
    render(todos);
  } catch (e) {
    list.innerHTML = '<div style="color:tomato">Failed to load todos.</div>';
  }
}

function render(todos){
  list.innerHTML = '';
  todos.forEach(t => {
    const el = document.createElement('div');
    el.className = 'todo' + (t.done ? ' done' : '');
    el.innerHTML = `
      <input type="checkbox" ${t.done ? 'checked' : ''} data-id="${t.id}" />
      <div class="title">${escapeHtml(t.title)}</div>
      <div class="actions">
        <button class="btn edit" data-id="${t.id}">Edit</button>
        <button class="btn delete" data-id="${t.id}">Delete</button>
      </div>
    `;
    list.appendChild(el);
  });
  const remaining = todos.filter(t => !t.done).length;
  stats.textContent = remaining + ' items left';
}

function escapeHtml(s){ return s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;'); }

newTodo.addEventListener('keydown', async (e) => {
  if (e.key === 'Enter') {
    const title = newTodo.value.trim();
    if (!title) return;
    try {
      await apiFetch('/todos', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({title})
      });
      newTodo.value = '';
      load();
    } catch (err) {
      alert('Could not add todo');
    }
  }
});

list.addEventListener('click', async (e) => {
  const id = e.target.getAttribute('data-id');
  if (!id) return;
  if (e.target.classList.contains('delete')) {
    if (!confirm('Delete this task?')) return;
    await apiFetch('/todos/' + id, {method:'DELETE'});
    load();
  } else if (e.target.classList.contains('edit')) {
    const node = e.target.closest('.todo');
    const titleNode = node.querySelector('.title');
    const current = titleNode.textContent;
    const newTitle = prompt('Edit task', current);
    if (newTitle !== null) {
      await apiFetch('/todos/' + id, {
        method:'PUT',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({title: newTitle})
      });
      load();
    }
  } else if (e.target.tagName === 'INPUT') {
    const checked = e.target.checked;
    await apiFetch('/todos/' + id, {
      method:'PUT',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({done: checked})
    });
    load();
  }
});

clearDoneBtn.addEventListener('click', async () => {
  // fetch all, delete done items
  const todos = await apiFetch('/todos');
  const done = todos.filter(t => t.done);
  if (done.length === 0) return alert('No completed tasks');
  if (!confirm('Clear completed tasks?')) return;
  await Promise.all(done.map(t => fetch(`/api/todos/${t.id}`, {method:'DELETE'})));
  load();
});

// Initial load
load();
