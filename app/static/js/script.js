let token = '';
let headers = { 'Content-Type': 'application/json' };

const state = {
  countries: [],
  manufacturers: [],
  cars: []
};

async function getToken() {
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;
  const res = await fetch(`${apiBase}/token/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ username, password })
  });
  const data = await res.json();
  if (res.ok) {
    token = data.token;
    headers['Authorization'] = 'Token ' + token;
    document.getElementById('tokenStatus').innerText = 'Авторизация успешна';
    loadAll();
  } else {
    document.getElementById('tokenStatus').innerText = 'Ошибка авторизации';
  }
}

async function deleteItem(type, id) {
  if (!token) return alert("Нужен токен");
  await fetch(`${apiBase}/${type}/${id}/`, {
    method: 'DELETE',
    headers
  });
  loadAll();
}

async function loadAll() {
  await loadCountries();
  await loadManufacturers();
  await loadCars();
  await loadComments();
}

async function loadCountries() {
  const res = await fetch(`${apiBase}/countries/`);
  const data = await res.json();
  state.countries = data.results || data;

  const table = document.getElementById('countryTable');
  table.innerHTML = `<tr><th>ID</th><th>Страна</th><th>Производители и автомобили</th><th>Удалить</th></tr>` +
    state.countries.map(c => {
      const manufacturers = c.manufacturers.map(m => {
        const cars = m.cars.map(car =>
          `${car.name} (${car.start_year}–${car.end_year}) [${car.comment_count} комм.]`
        ).join("<br>");
        return `<b>${m.name}</b> (${m.comment_count} комм.)<br>Авто:<br>${cars}`;
      }).join("<hr>");
      return `<tr>
        <td>${c.id}</td>
        <td>${c.name}</td>
        <td>${manufacturers}</td>
        <td><button onclick="deleteItem('countries', ${c.id})">X</button></td>
      </tr>`;
    }).join('');
}

document.getElementById('countryForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!token) return alert("Нужен токен");
  const name = document.getElementById('countryName').value.trim();
  await fetch(`${apiBase}/countries/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ name })
  });
  document.getElementById('countryName').value = '';
  loadCountries();
});

async function loadManufacturers() {
  const res = await fetch(`${apiBase}/manufacturers/`);
  const data = await res.json();
  state.manufacturers = data.results || data;

  const table = document.getElementById('manufacturerTable');
  table.innerHTML = '<tr><th>ID</th><th>Название</th><th>Страна</th><th>Удалить</th></tr>' +
    state.manufacturers.map(m =>
      `<tr><td>${m.id}</td><td>${m.name}</td><td>${m.country}</td>
        <td><button onclick="deleteItem('manufacturers', ${m.id})">X</button></td></tr>`
    ).join('');
}

document.getElementById('manufacturerForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!token) return alert("Нужен токен");

  const name = document.getElementById('manufacturerName').value.trim();
  const countryName = document.getElementById('manufacturerCountryInput').value.trim();
  if (!name || !countryName) return alert("Введите и производителя, и страну");

  // Находим страну по имени или создаем
  let country = state.countries.find(c => c.name.toLowerCase() === countryName.toLowerCase());
  if (!country) {
    const res = await fetch(`${apiBase}/countries/`, {
      method: 'POST',
      headers,
      body: JSON.stringify({ name: countryName })
    });
    if (!res.ok) return alert("Ошибка при создании страны");
    country = await res.json();
    await loadCountries();
  }

  const res = await fetch(`${apiBase}/manufacturers/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ name, country_id: Number(country.id) })
  });

  if (!res.ok) {
    const err = await res.json();
    return alert("Ошибка создания производителя: " + JSON.stringify(err));
  }

  document.getElementById('manufacturerName').value = '';
  document.getElementById('manufacturerCountryInput').value = '';
  loadManufacturers();
});

async function loadCars() {
  const res = await fetch(`${apiBase}/cars/`);
  const data = await res.json();
  state.cars = data.results || data;

  const table = document.getElementById('carTable');
  table.innerHTML = '<tr><th>ID</th><th>Название</th><th>Годы</th><th>Производитель</th><th>Удалить</th></tr>' +
    state.cars.map(c =>
      `<tr><td>${c.id}</td><td>${c.name}</td><td>${c.start_year}–${c.end_year}</td><td>${c.manufacturer}</td>
        <td><button onclick="deleteItem('cars', ${c.id})">X</button></td></tr>`
    ).join('');
}

document.getElementById('carForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  if (!token) return alert("Нужен токен");

  const name = document.getElementById('carName').value.trim();
  const start_year = parseInt(document.getElementById('carStart').value);
  const end_year = parseInt(document.getElementById('carEnd').value);
  const manufacturerName = document.getElementById('carManufacturerInput').value.trim();

  const currentYear = new Date().getFullYear();

  if (!name) return alert("Введите название автомобиля");
  if (isNaN(start_year) || start_year < 1886 || start_year > currentYear) {
    // 1886 — год изобретения первого автомобиля, минимальный разумный порог
    return alert(`Введите корректный год начала выпуска (1886–${currentYear})`);
  }
  if (isNaN(end_year) || end_year < start_year || end_year > currentYear + 5) {
    // можно немного позволить в будущем, например до +5 лет
    return alert(`Введите корректный год окончания выпуска (не раньше года начала и не слишком далеко в будущем)`);
  }

  const manufacturer = state.manufacturers.find(m => m.name.toLowerCase() === manufacturerName.toLowerCase());
  if (!manufacturer) return alert("Производитель не найден");

  const res = await fetch(`${apiBase}/cars/`, {
    method: 'POST',
    headers,
    body: JSON.stringify({ name, start_year, end_year, manufacturer_id: manufacturer.id })
  });

  if (!res.ok) {
    const err = await res.json();
    return alert("Ошибка создания автомобиля: " + JSON.stringify(err));
  }

  document.getElementById('carName').value = '';
  document.getElementById('carStart').value = '';
  document.getElementById('carEnd').value = '';
  document.getElementById('carManufacturerInput').value = '';
  loadCars();
});

async function loadComments() {
  const res = await fetch(`${apiBase}/comments/`);
  const data = await res.json();
  const comments = data.results || data;

  const table = document.getElementById('commentTable');
  table.innerHTML = '<tr><th>ID</th><th>Email</th><th>Текст</th><th>Автомобиль</th><th>Дата</th><th>Удалить</th></tr>' +
    comments.map(c =>
      `<tr><td>${c.id}</td><td>${c.email}</td><td>${c.content}</td><td>${c.car}</td>
        <td>${new Date(c.created_at).toLocaleString()}</td>
        <td><button onclick="deleteItem('comments', ${c.id})">X</button></td></tr>`
    ).join('');
}

document.getElementById('commentForm').addEventListener('submit', async (e) => {
  e.preventDefault();

  const email = document.getElementById('commentEmail').value.trim();
  const content = document.getElementById('commentContent').value.trim();
  const carName = document.getElementById('commentCarInput').value.trim();

  const car = state.cars.find(c => c.name.toLowerCase() === carName.toLowerCase());
  if (!car) return alert("Автомобиль не найден");

  await fetch(`${apiBase}/comments/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, content, car: car.id })
  });

  document.getElementById('commentEmail').value = '';
  document.getElementById('commentContent').value = '';
  document.getElementById('commentCarInput').value = '';
  loadComments();
});

function setupAutocomplete(inputId, suggestionBoxId, sourceListFn) {
  const input = document.getElementById(inputId);
  const box = document.getElementById(suggestionBoxId);

  input.addEventListener('input', () => {
    const value = input.value.toLowerCase();
    const matches = sourceListFn().filter(item =>
      item.toLowerCase().includes(value)
    ).slice(0, 5);

    if (!value || matches.length === 0) {
      box.innerHTML = '';
      return;
    }

    box.innerHTML = matches.map(m => `<div>${m}</div>`).join('');
    box.querySelectorAll('div').forEach(div => {
      div.addEventListener('click', () => {
        input.value = div.innerText;
        box.innerHTML = '';
      });
    });
  });

  document.addEventListener('click', e => {
    if (!box.contains(e.target) && e.target !== input) box.innerHTML = '';
  });
}

setupAutocomplete('manufacturerCountryInput', 'manufacturerCountrySuggestions', () =>
  state.countries.map(c => c.name));

setupAutocomplete('carManufacturerInput', 'carManufacturerSuggestions', () =>
  state.manufacturers.map(m => m.name));

setupAutocomplete('commentCarInput', 'commentCarSuggestions', () =>
  state.cars.map(c => c.name));

setInterval(() => {
  if (!document.hidden) loadAll();
}, 10000);

loadAll();
