const API_URL = "http://127.0.0.1:8000/api/v1";

// 1. Fetch and Display Vehicles on Load
document.addEventListener("DOMContentLoaded", async () => {
  const listContainer = document.getElementById("car-list");

  try {
    const response = await fetch(`${API_URL}/vehicles`);
    if (!response.ok) throw new Error("Error connecting to server");

    const vehicles = await response.json();
    listContainer.innerHTML = ""; // Clear loading text

    vehicles.forEach((car) => {
      const card = document.createElement("div");
      card.className = "car-card";
      card.innerHTML = `
                <h3>${car.brand} ${car.model}</h3>
                <p>Año: ${car.year} | Color: ${car.color}</p>
                <p>KM: ${car.mileage}</p>
                <div class="price">$${car.price.toLocaleString()}</div>
                <button onclick="openBooking(${car.id}, '${car.brand} ${
        car.model
      }')">
                    Agendar Visita
                </button>
            `;
      listContainer.appendChild(card);
    });
  } catch (error) {
    listContainer.innerHTML = `<p style="color:red">Error: ${error.message}. Is Backend running?</p>`;
  }
});

// 2. Modal Logic
const modal = document.getElementById("booking-modal");
const closeBtn = document.querySelector(".close-btn");

function openBooking(id, name) {
  document.getElementById("vehicle_id").value = id;
  document.getElementById("selected-car-text").innerText = "Auto: " + name;
  modal.style.display = "block";
}

closeBtn.onclick = () => (modal.style.display = "none");
window.onclick = (e) => {
  if (e.target == modal) modal.style.display = "none";
};

// 3. Handle Form Submit (Create Appointment)
document
  .getElementById("booking-form")
  .addEventListener("submit", async (e) => {
    e.preventDefault();

    const data = {
      vehicle_id: parseInt(document.getElementById("vehicle_id").value),
      customer_name: document.getElementById("name").value,
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
        alert(
          "✅ Cita Creada! Revisa la consola del backend para ver la notificación."
        );
        modal.style.display = "none";
      } else {
        const err = await response.json();
        alert("❌ Error: " + JSON.stringify(err));
      }
    } catch (error) {
      alert("Error de red: " + error.message);
    }
  });
