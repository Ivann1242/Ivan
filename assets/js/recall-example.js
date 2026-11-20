const figure = document.getElementById("attention-example");
const example = JSON.parse(figure.querySelector(".recall-example-data").textContent);
const controls = figure.querySelector(".recall-controls");
const positions = Array.from(figure.querySelectorAll(".recall-tape li"));
const verdict = figure.querySelector("output");
const number = new Intl.NumberFormat("en", { maximumFractionDigits: 1 });

function formatWeight(weight) {
  const percent = weight * 100;
  if (percent > 0 && percent < 0.1) return "<0.1%";
  if (percent > 99.9 && percent < 100) return ">99.9%";
  return number.format(percent) + "%";
}

function updateExample() {
  const query = controls.querySelector('input[name="recall-query"]:checked').value;
  const mask = controls.querySelector('input[name="recall-block"]:checked').value;
  const reading = example.queries[query];
  const result = reading.conditions[mask];
  const tokens = [...example.prefix, query];

  positions.forEach((position, index) => {
    let role = "";
    if (index === reading.key_pos) role = "key";
    if (index === reading.value_pos) role = "value";
    if (index === tokens.length - 1) role = "query";
    const blocked = role === mask;
    position.dataset.role = role;
    position.toggleAttribute("data-blocked", blocked);
    position.querySelector(".recall-symbol").textContent = tokens[index];
    position.querySelector(".recall-role").textContent = role;
    position.querySelector(".recall-share").textContent = blocked ? "Blocked" : formatWeight(result.weights[index]);
    position.querySelector(".recall-bar").style.height = (100 * result.weights[index]) + "%";
  });

  const prediction = document.createElement("strong");
  prediction.textContent = result.prediction;
  const target = document.createElement("strong");
  target.textContent = reading.target;
  verdict.replaceChildren("The model predicts ", prediction, ". The target is ", target, ".");
}

controls.addEventListener("change", updateExample);
updateExample();
controls.hidden = false;
