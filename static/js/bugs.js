async function loadBugs() {
    const res = await fetch('/bugs/');
    const bugs = await res.json();
    const container = document.getElementById('listContainer');
    container.innerHTML = bugs.map(b => `
        <div class="list-item ${b.severity}">
            <strong>${b.title}</strong> (ID: ${b.id})<br>
            <a href="/bug/${b.id}">Подробнее</a>
        </div>
    `).join('');
}
document.getElementById('bugForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const form = e.target;
    const steps = form.steps_to_reproduce.value
        .split('\n')
        .map(s => s.trim())
        .filter(s => s.length > 0);

    const bug = {
        id: parseInt(form.id.value),
        title: form.title.value,
        severity: form.severity.value,
        steps_to_reproduce: steps,
        actual_result: form.actual_result.value,
        expected_result: form.expected_result.value,
        environment: form.environment.value,
        test_case_id: form.test_case_id.value ? parseInt(form.test_case_id.value) : null
    };

    const response = await fetch('/bugs/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bug)
    });

    const messageEl = document.getElementById('message');
    if (response.ok) {
        messageEl.innerHTML = '<p style="color:green">✅ Баг-репорт успешно добавлен!</p>';
        form.reset();
        loadBugs();
    } else {
        const error = await response.json();
        const msg = error.detail?.[0]?.msg || 'Неизвестная ошибка';
        messageEl.innerHTML = `<p style="color:red">❌ ${msg}</p>`;
    }
});
document.addEventListener('DOMContentLoaded', loadBugs);
