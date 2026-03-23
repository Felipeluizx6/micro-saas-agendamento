const API = "http://127.0.0.1:8000";

const lista = document.getElementById("lista-agenda");

const selectClientes = document.getElementById("cliente_id");
const selectProfissionais = document.getElementById("profissional_id");
const selectServicos = document.getElementById("servico_select");


// ================= FETCH BASE =================
async function fetchData(url) {
  const res = await fetch(API + url);
  return await res.json();
}


// ================= RESUMO =================
async function carregarResumo() {
  const clientes = await fetchData("/clientes");
  const profissionais = await fetchData("/profissionais");
  const servicos = await fetchData("/servicos");
  const agendamentos = await fetchData("/agendamentos");

  document.getElementById("total-clientes").textContent = clientes.length;
  document.getElementById("total-profissionais").textContent = profissionais.length;
  document.getElementById("total-servicos").textContent = servicos.length;
  document.getElementById("total-agendamentos").textContent = agendamentos.length;
}


// ================= SELECTS =================
async function carregarSelects() {
  const clientes = await fetchData("/clientes");
  const profissionais = await fetchData("/profissionais");
  const servicos = await fetchData("/servicos");

  selectClientes.innerHTML = clientes.map(c => `<option value="${c.id}">${c.nome}</option>`).join("");
  selectProfissionais.innerHTML = profissionais.map(p => `<option value="${p.id}">${p.nome}</option>`).join("");
  selectServicos.innerHTML = servicos.map(s => `<option value="${s.nome}">${s.nome}</option>`).join("");
}


// ================= CLIENTE =================
document.getElementById("form-cliente").onsubmit = async (e) => {
  e.preventDefault();

  await fetch(API + "/clientes", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      nome: cliente_nome.value,
      telefone: cliente_telefone.value
    })
  });

  e.target.reset();
  carregarResumo();
  carregarSelects();
};


// ================= PROFISSIONAL =================
document.getElementById("form-profissional").onsubmit = async (e) => {
  e.preventDefault();

  await fetch(API + "/profissionais", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      nome: prof_nome.value,
      telefone: prof_telefone.value,
      servico: prof_servico.value
    })
  });

  e.target.reset();
  carregarResumo();
  carregarSelects();
};


// ================= SERVIÇO =================
document.getElementById("form-servico").onsubmit = async (e) => {
  e.preventDefault();

  await fetch(API + "/servicos", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      nome: servico_nome.value,
      preco: Number(servico_preco.value),
      duracao_minutos: Number(servico_duracao.value)
    })
  });

  e.target.reset();
  carregarResumo();
  carregarSelects();
};


// ================= AGENDAMENTO =================
document.getElementById("form-agendamento").onsubmit = async (e) => {
  e.preventDefault();

  await fetch(API + "/agendamentos", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      cliente_id: Number(selectClientes.value),
      profissional_id: Number(selectProfissionais.value),
      servico: selectServicos.value,
      data: data.value,
      hora: hora.value
    })
  });

  e.target.reset();
  carregarAgenda();
};


// ================= AGENDA =================
async function carregarAgenda() {
  lista.innerHTML = "";

  const agendamentos = await fetchData("/agendamentos");
  const clientes = await fetchData("/clientes");
  const profissionais = await fetchData("/profissionais");

  agendamentos.forEach(a => {
    const c = clientes.find(x => x.id === a.cliente_id);
    const p = profissionais.find(x => x.id === a.profissional_id);

    lista.innerHTML += `
      <li>
        <b>${a.servico}</b><br>
        ${c?.nome} | ${p?.nome}<br>
        ${a.data} ${a.hora}
      </li>
    `;
  });
}


// ================= INIT =================
document.getElementById("btn-carregar-agenda").onclick = carregarAgenda;

carregarResumo();
carregarSelects();