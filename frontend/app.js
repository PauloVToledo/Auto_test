const API_URL = "http://127.0.0.1:8000/api/v1";
let bookingModal;
let allVehicles = []; // 1. Variable Global para guardar los autos

import { carImages } from "./dictionary.js";

// Cache para almacenar imágenes ya validadas y no repetir peticiones
const validatedBrands = {};

// Función de validación de imágenes
function validateImages(urls, fallback) {
  return Promise.all(
    urls.map(
      (url) =>
        new Promise((resolve) => {
          const img = new Image();
          img.onload = () => resolve(url);
          img.onerror = () => resolve(null);
          img.src = url;
        }),
    ),
  ).then((results) => {
    const valid = results.filter(Boolean);
    return valid.length ? valid : [fallback];
  });
}

// Función auxiliar para obtener imagen según marca
async function getCarImage(brand, model, carId) {
  // Normalizamos a minúsculas para evitar errores
  const key = brand.toLowerCase();

  if (!validatedBrands[key]) {
    const images = carImages[key] || carImages["default"];
    const fallback = carImages["default"][0];
    validatedBrands[key] = await validateImages(images, fallback);
  }

  const validImages = validatedBrands[key];
  const index = carId % validImages.length;

  return validImages[index];
}

document.addEventListener("DOMContentLoaded", async () => {
  // Configurar Modal
  const modalEl = document.getElementById("bookingModal");
  if (modalEl) bookingModal = new bootstrap.Modal(modalEl);

  // Cargar Autos
  const listContainer = document.getElementById("car-list");
  if (listContainer) {
    await fetchAndSetupVehicles(listContainer);
  }

  // Configurar Eventos de Filtros
  setupFilterEvents();
});

// --- LÓGICA DE CARGA Y RENDERIZADO ---

async function fetchAndSetupVehicles(container) {
  try {
    const response = await fetch(`${API_URL}/vehicles`);
    allVehicles = await response.json(); // Guardamos en memoria

    // Llenar los Selects (Marca y Año) dinámicamente según lo que haya en BD
    populateDropdowns();

    // Renderizar todos inicialmente
    await renderVehicles(allVehicles);
  } catch (error) {
    container.innerHTML = `<div class="alert alert-danger">Error cargando autos: ${error.message}</div>`;
  }
}

async function renderVehicles(vehiclesToRender) {
  const container = document.getElementById("car-list");
  container.innerHTML = "";

  if (vehiclesToRender.length === 0) {
    container.innerHTML = `<div class="col-12 text-center py-5 text-muted"><h4>😕 No se encontraron vehículos.</h4></div>`;
    return;
  }

  // Pre-cargamos las imágenes validadas
  const carsWithImages = await Promise.all(
    vehiclesToRender.map(async (car) => {
      const imageUrl = await getCarImage(car.brand, car.model, car.id);
      return { car, imageUrl };
    }),
  );

  carsWithImages.forEach(({ car, imageUrl }) => {
    const col = document.createElement("div");
    col.className = "col";
    col.innerHTML = `
            <div class="card h-100 shadow-sm border-0">
                <!-- IMAGEN REAL AQUÍ -->
                <div class="card-img-wrapper" style="position: relative; overflow: hidden; border-radius: 12px 12px 0 0;">
                    <img src="${imageUrl}" class="card-img-top" alt="${
                      car.brand
                    }" style="height: 220px; object-fit: cover; width: 100%;">
                    
                    <!-- Etiqueta de precio flotante -->
                    <span class="badge bg-dark position-absolute bottom-0 end-0 m-3 py-2 px-3 shadow" style="font-size: 1rem;">
                        $${car.price.toLocaleString()}
                    </span>
                </div>

                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <div>
                            <h5 class="card-title fw-bold mb-0">${car.brand} ${
                              car.model
                            }</h5>
                            <small class="text-muted text-uppercase" style="letter-spacing: 1px;">${
                              car.brand
                            }</small>
                        </div>
                        <span class="badge bg-light text-dark border">${
                          car.year
                        }</span>
                    </div>
                    
                    <div class="d-flex align-items-center text-muted small mb-3">
                        <span class="me-3">🎨 ${car.color}</span>
                        <span>🛣️ ${car.mileage} km</span>
                    </div>

                    <div class="d-grid">
                        <button class="btn btn-primary fw-bold" 
                            style="border-radius: 50px;"
                            onclick="openBooking(${car.id}, '${car.brand} ${
                              car.model
                            }')">
                            Agendar Visita
                        </button>
                    </div>
                </div>
            </div>
        `;
    container.appendChild(col);
  });
}

// --- LÓGICA DE FILTROS ---

function populateDropdowns() {
  const brandSelect = document.getElementById("filter-brand");
  const yearSelect = document.getElementById("filter-year");

  // Obtener valores únicos usando Set
  const brands = [...new Set(allVehicles.map((car) => car.brand))].sort();
  const years = [...new Set(allVehicles.map((car) => car.year))].sort(
    (a, b) => b - a,
  ); // Orden descendente

  // Llenar Marcas
  brands.forEach((brand) => {
    const option = document.createElement("option");
    option.value = brand;
    option.textContent = brand; // Convertir primera letra a mayuscula si se desea
    brandSelect.appendChild(option);
  });

  // Llenar Años
  years.forEach((year) => {
    const option = document.createElement("option");
    option.value = year;
    option.textContent = year;
    yearSelect.appendChild(option);
  });
}

function setupFilterEvents() {
  const brandSelect = document.getElementById("filter-brand");
  const yearSelect = document.getElementById("filter-year");
  const priceInput = document.getElementById("filter-price");
  const priceDisplay = document.getElementById("price-value");
  const resetBtn = document.getElementById("btn-reset");

  if (!brandSelect) return; // Si estamos en about.html, salir

  // Evento Slider de Precio (Visual)
  priceInput.addEventListener("input", (e) => {
    priceDisplay.innerText = "$" + parseInt(e.target.value).toLocaleString();
    applyFilters(); // Filtrar en tiempo real mientras deslizas
  });

  // Eventos Selects
  brandSelect.addEventListener("change", applyFilters);
  yearSelect.addEventListener("change", applyFilters);

  // Evento Reset
  resetBtn.addEventListener("click", () => {
    brandSelect.value = "all";
    yearSelect.value = "all";
    priceInput.value = 90000;
    priceDisplay.innerText = "$90,000";
    renderVehicles(allVehicles); // Volver a mostrar todos
  });
}

function applyFilters() {
  const selectedBrand = document.getElementById("filter-brand").value;
  const selectedYear = document.getElementById("filter-year").value;
  const maxPrice = parseInt(document.getElementById("filter-price").value);

  // La lógica de filtrado pura
  const filtered = allVehicles.filter((car) => {
    const matchBrand = selectedBrand === "all" || car.brand === selectedBrand;
    const matchYear =
      selectedYear === "all" || car.year.toString() === selectedYear;
    const matchPrice = car.price <= maxPrice;

    return matchBrand && matchYear && matchPrice;
  });

  renderVehicles(filtered);
}

// --- MODAL Y FORMULARIO (Igual que antes) ---

window.openBooking = function (id, name) {
  document.getElementById("vehicle_id").value = id;
  document.getElementById("selected-car-text").innerText = "Vehículo: " + name;
  bookingModal.show();
};

const form = document.getElementById("booking-form");
if (form) {
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // --- NUEVA VALIDACIÓN DE HORA ---
    const dateInput = document.getElementById("date").value;
    const selectedDate = new Date(dateInput);
    const hour = selectedDate.getHours();

    // Validar rango (9 a 17:59)
    if (hour < 9 || hour >= 18) {
      alert(
        "⛔ Horario no válido.\n\nNuestras sucursales atienden de 09:00 AM a 18:00 PM.\nPor favor selecciona otro horario.",
      );
      return; // Detiene el envío, no llama al backend
    }

    const btn = form.querySelector("button[type='submit']");
    const originalText = btn.innerText;
    btn.disabled = true;
    btn.innerText = "Enviando...";

    const data = {
      vehicle_id: parseInt(document.getElementById("vehicle_id").value),
      customer_name: document.getElementById("name").value,
      customer_email: document.getElementById("email").value,
      customer_phone: document.getElementById("phone").value,
      date: document.getElementById("date").value,
    };

    try {
      const response = await fetch(`${API_URL}/appointments/`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        alert("✅ ¡Cita Confirmada!");
        bookingModal.hide();
        form.reset();
      } else {
        const err = await response.json();
        alert("❌ Error: " + (err.detail || "Error desconocido"));
      }
    } catch (error) {
      alert("Error de red: " + error.message);
    } finally {
      btn.disabled = false;
      btn.innerText = originalText;
    }
  });
}

// --- LÓGICA DEL CHATBOT (GLOBAL) ---

// 1. Asignamos a window para que el HTML pueda verlas sí o sí
window.toggleChat = function () {
  const chatWindow = document.getElementById("chat-window");
  if (!chatWindow) {
    console.error("No se encontró el elemento chat-window");
    return;
  }

  if (chatWindow.style.display === "none" || chatWindow.style.display === "") {
    chatWindow.style.display = "block";
    // Poner foco en el input al abrir
    setTimeout(() => document.getElementById("chat-input").focus(), 100);
  } else {
    chatWindow.style.display = "none";
  }
};

window.handleEnter = function (e) {
  if (e.key === "Enter") window.sendMessage();
};

window.sendMessage = async function () {
  const input = document.getElementById("chat-input");
  const message = input.value.trim();
  if (!message) return;

  // 1. Mostrar mensaje del usuario
  addMessageToChat(message, "user");
  input.value = "";
  input.disabled = true;

  // 2. Mostrar "Escribiendo..."
  const loadingId = addMessageToChat("Pensando... 🤔", "bot", true);

  try {
    const response = await fetch(`${API_URL}/chat/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: message }),
    });

    const data = await response.json();

    removeMessage(loadingId);
    addMessageToChat(data.response, "bot");
  } catch (error) {
    console.error(error);
    removeMessage(loadingId);
    addMessageToChat(
      "Error de conexión ❌. ¿Está corriendo el backend?",
      "bot",
    );
  } finally {
    input.disabled = false;
    input.focus();
  }
};

// Funciones auxiliares (no necesitan window, pero las usamos dentro de las otras)
function addMessageToChat(text, sender, isLoading = false) {
  const container = document.getElementById("chat-messages");
  const div = document.createElement("div");
  const msgId = "msg-" + Date.now();
  div.id = msgId;

  const isUser = sender === "user";
  div.className = `d-flex ${isUser ? "justify-content-end" : "align-items-start"} mb-2`;

  const bubbleColor = isUser
    ? "bg-primary text-white"
    : "bg-white text-dark border";

  // Convertir saltos de línea a <br> para que se vea bien el formato de la IA
  const formattedText = text.replace(/\n/g, "<br>");

  div.innerHTML = `
        <div class="${bubbleColor} p-2 rounded shadow-sm" style="max-width: 80%;">
            ${formattedText}
        </div>
    `;

  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return msgId;
}

function removeMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

// --- DARK MODE LOGIC ---

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  const body = document.body;

  // 1. Verificar preferencia guardada en LocalStorage
  const savedTheme = localStorage.getItem("theme");

  // Si hay tema guardado 'dark', o si no hay nada pero el sistema operativo prefiere oscuro
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;

  if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
    enableDarkMode();
  } else {
    disableDarkMode(); // Asegurar estado inicial
  }

  // 2. Evento Click
  if (toggleBtn) {
    toggleBtn.addEventListener("click", () => {
      if (body.classList.contains("dark-mode")) {
        disableDarkMode();
      } else {
        enableDarkMode();
      }
    });
  }

  // Funciones auxiliares
  function enableDarkMode() {
    body.classList.add("dark-mode");
    localStorage.setItem("theme", "dark");
    if (toggleBtn) toggleBtn.innerHTML = "☀️"; // Icono de Sol para volver a luz
    if (toggleBtn) toggleBtn.style.borderColor = "rgba(255,255,255,0.5)";
  }

  function disableDarkMode() {
    body.classList.remove("dark-mode");
    localStorage.setItem("theme", "light");
    if (toggleBtn) toggleBtn.innerHTML = "🌙"; // Icono de Luna para ir a oscuro
    if (toggleBtn) toggleBtn.style.borderColor = "rgba(0,0,0,0.1)";
  }
});
