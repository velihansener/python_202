// app.js
async function fetchBooks() {
  const ul = document.getElementById('books');
  ul.innerHTML = '<li class="item">Yükleniyor...</li>';
  try {
    const res = await fetch(`${API}/books`);
    const data = await res.json();
    ul.innerHTML = '';
    if (data.length === 0) {
      ul.innerHTML = '<li class="item">(Henüz kitap yok)</li>';
      return;
    }
    for (const b of data) {
      const li = document.createElement('li');
      li.className = 'item';
      li.innerHTML = `
        <div>
          <div><strong>${b.title}</strong></div>
          <div class="badge">${b.author}</div>
        </div>
        <div>
          <span class="badge">ISBN: ${b.isbn}</span>
          <button data-isbn="${b.isbn}">Sil</button>
        </div>
      `;
      li.querySelector('button').addEventListener('click', () => deleteBook(b.isbn));
      ul.appendChild(li);
    }
  } catch (e) {
    ul.innerHTML = '<li class="item">Hata oluştu.</li>';
  }
}

async function addBook() {
  const msg = document.getElementById('msg');
  msg.textContent = '';
  const isbn = document.getElementById('isbn').value.trim();
  if (!isbn) { msg.textContent = 'ISBN girin'; return; }
  try {
    const res = await fetch(`${API}/books`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({ isbn })
    });
    if (res.status === 201) {
      msg.textContent = 'Eklendi!';
      document.getElementById('isbn').value = '';
      fetchBooks();
    } else {
      const body = await res.json();
      msg.textContent = body.detail || 'Hata.';
    }
  } catch (e) {
    msg.textContent = 'Ağ hatası.';
  }
}

async function deleteBook(isbn) {
  await fetch(`${API}/books/${encodeURIComponent(isbn)}`, { method: 'DELETE' });
  fetchBooks();
}

document.getElementById('addBtn').addEventListener('click', addBook);
fetchBooks();
