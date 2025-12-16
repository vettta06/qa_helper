async function loadTestCases() {
    const res = await fetch('/testcases/');
    const tcs = await res.json();
    const container = document.getElementById('listContainer');
    container.innerHTML = tcs.map(tc => `
        <div class="list-item">
            <strong>ID ${tc.id}</strong>: ${tc.description}<br>
            <a href="/testcase/${tc.id}">Подробнее</a>
            <button onclick="deleteTestCase(${tc.id})">Удалить</button>
        </div>
    `).join('');
}

async function deleteTestCase(id) {
    if (!confirm('Вы уверены, что хотите удалить тест-кейс ID ' + id + '?')) return;
    const res = await fetch(`/testcases/${id}`, { method: 'DELETE' });
    if (res.ok) {
        loadTestCases();
    } else {
        alert('Ошибка удаления: ' + (await res.json()).detail);
    }
}
document.getElementById('tcForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const form = e.target;

    const steps = form.steps.value
        .split('\n')
        .map(s => s.trim())
        .filter(s => s);

    const tc = {
        id: parseInt(form.id.value),
        requirement_id: parseInt(form.requirement_id.value),
        description: form.description.value,
        steps: steps,
        expected_result: form.expected_result.value
    };

    const res = await fetch('/testcases/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tc)
    });

    const msgEl = document.getElementById('message');
    if (res.ok) {
        msgEl.innerHTML = '<p style="color:green">✅ Тест-кейс создан!</p>';
        form.reset();
        loadTestCases();
    } else {
        const err = await res.json();
        const msg = err.detail?.[0]?.msg || 'Ошибка';
        msgEl.innerHTML = `<p style="color:red">❌ ${msg}</p>`;
    }
});
document.addEventListener('DOMContentLoaded', loadTestCases);
