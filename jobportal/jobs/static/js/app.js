// Tab toggle on auth page
document.querySelectorAll(".tab-btn").forEach(btn=>{
  btn.addEventListener("click", ()=>{
    document.querySelectorAll(".tab-btn").forEach(b=>b.classList.remove("active"));
    document.querySelectorAll(".tab-panel").forEach(p=>p.classList.remove("active"));
    btn.classList.add("active");
    const tgt = document.querySelector(btn.dataset.target);
    if (tgt) tgt.classList.add("active");
  });
});

// Save job buttons
const isAuthenticated = document.body.classList.contains("auth-yes"); // optional if you set it
document.querySelectorAll(".save-btn").forEach(btn=>{
  btn.addEventListener("click", async ()=>{
    const id = btn.dataset.id;
    if (document.querySelector(".brand")) { /* noop to avoid errors */ }
    // Logged-in -> use server toggle
    const loggedIn = document.querySelector('a[href$="Logout"]') || document.querySelector('a[href*="?logout=1"]');
    if (loggedIn) {
      const res = await fetch(`/save/${id}/`, {headers: {"x-requested-with":"XMLHttpRequest"}});
      const data = await res.json();
      if (data.status === "saved") { btn.classList.add("is-saved"); btn.textContent = "Saved"; }
      else { btn.classList.remove("is-saved"); btn.textContent = "Save"; }
    } else {
      // Guest -> localStorage
      const key = "savedJobs";
      const saved = new Set(JSON.parse(localStorage.getItem(key) || "[]"));
      if (saved.has(id)) { saved.delete(id); btn.classList.remove("is-saved"); btn.textContent = "Save"; }
      else { saved.add(id); btn.classList.add("is-saved"); btn.textContent = "Saved"; }
      localStorage.setItem(key, JSON.stringify([...saved]));
    }
  });
});

// Simple login/register client validation (optional – server still validates)
document.getElementById("registerForm")?.addEventListener("submit", function(e){
  const u = this.querySelector('input[name="username"]');
  const em = this.querySelector('input[name="email"]');
  if(!u.value.trim()){ e.preventDefault(); alert("Username is required"); }
  else if(!/^\S+@\S+\.\S+$/.test(em.value)){ e.preventDefault(); alert("Valid email required"); }
});
