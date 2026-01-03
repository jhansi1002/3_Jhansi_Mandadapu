document.getElementById('ask').addEventListener('click', async () => {
  const q = document.getElementById('question').value;
  const res = await fetch('/api/chat', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
  const j = await res.json();
  document.getElementById('answer').textContent = j.answer;
});

async function loadReminders(){
  const res = await fetch('/api/reminders');
  const j = await res.json();
  document.getElementById('reminders').textContent = JSON.stringify(j, null, 2);
}

document.getElementById('create_rem').addEventListener('click', async ()=>{
  const payload = {
    drug_name: document.getElementById('drug_name').value,
    dosage_mg: Number(document.getElementById('dosage_mg').value),
    frequency_per_day: Number(document.getElementById('freq').value),
    start_date: new Date().toISOString()
  }
  const res = await fetch('/api/reminders', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const j = await res.json();
  await loadReminders();
  alert('Created reminder id: ' + j.id);
});

document.getElementById('gen_plan').addEventListener('click', async ()=>{
  const drug = document.getElementById('drug_name').value || 'aspirin';
  const res = await fetch(`/api/generate_plan?drug_name=${encodeURIComponent(drug)}&dosage_mg=100&frequency_per_day=2`);
  const j = await res.json();
  document.getElementById('plan').textContent = JSON.stringify(j, null, 2);
});

loadReminders();
