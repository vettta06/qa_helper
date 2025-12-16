async function loadRequirements() {
    const res = await fetch('/requirements/');
    const reqs = await res.json();
    const container = document.getElementById('listContainer');
    container.innerHTML = reqs.map(r => `
        <div class="list-item">
            <strong>ID ${r.id}</strong>: ${r.text} (${r.req_type})<br>
            <a href="/requirement/${r.id}">Подробнее</a>
            <button onclick="deleteReq(${r.id})">Удалить</button>
        </div>
    `).join('');
}

async function deleteReq(id) {
    if (!confirm('Вы уверены, что хотите удалить требование ID ' + id + '?')) return;
    const res = await fetch(`/requirements/${id}`, { method: 'DELETE' });
    if (res.ok) {
        loadRequirements();
    } else {
        alert('Ошибка удаления: ' + (await res.json()).detail);
    }
}
document.getElementById('reqForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;

    const req = {
        id: parseInt(form.id.value),
        text: form.text.value,
        req_type: form.req_type.value,
        device_type: form.device_type.value
    };

    const res = await fetch('/requirements/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(req)
    });

    const msgEl = document.getElementById('message');
    if (res.ok) {
        msgEl.innerHTML = '<p style="color:green">✅ Требование создано!</p>';
        form.reset();
        loadRequirements();
    } else {
        const err = await res.json();
        const msg = err.detail?.[0]?.msg || 'Ошибка';
        msgEl.innerHTML = `<p style="color:red">❌ ${msg}</p>`;
    }
});
document.addEventListener('DOMContentLoaded', loadRequirements);
