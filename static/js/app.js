// Mobile menu
(function () {
  var btn = document.getElementById('menuBtn'), bar = document.getElementById('sidebar');
  if (btn && bar) btn.addEventListener('click', function () { bar.classList.toggle('open'); });
})();

// Cancel-appointment: ask for confirmation + optional reason
document.querySelectorAll('.cancel-form').forEach(function (f) {
  f.addEventListener('submit', function (e) {
    var reason = window.prompt('Cancel this appointment?\nOptional reason (included in the email to the patient):', '');
    if (reason === null) { e.preventDefault(); return; }
    f.querySelector('input[name=cancel_reason]').value = reason;
  });
});

// Auto-dismiss info/success alerts
setTimeout(function () {
  document.querySelectorAll('.alert-info, .alert-success').forEach(function (a) { a.style.transition = 'opacity .5s'; a.style.opacity = '0'; setTimeout(function () { a.remove(); }, 600); });
}, 9000);
