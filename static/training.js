document.querySelectorAll("[data-mlp-config]").forEach((form) => {
  const layerCount = form.querySelector("[data-hidden-layer-count]");
  const layerList = form.querySelector("[data-hidden-layers]");
  const layerLabel = layerList.dataset.layerLabel;
  const neuronsLabel = layerList.dataset.neuronsLabel;
  const activationLabel = layerList.dataset.activationLabel;
  const activationTemplate = form.querySelector("[data-activation-template]");

  function renderLayers() {
    const previousValues = Array.from(layerList.querySelectorAll(".layer-row"), (row) => ({
      neurons: row.querySelector("input").value,
      activation: row.querySelector("select").value,
    }));
    layerList.replaceChildren();

    for (let index = 0; index < Number(layerCount.value); index += 1) {
      const number = index + 1;
      const row = document.createElement("div");
      const neuronField = document.createElement("label");
      const neuronCaption = document.createElement("span");
      const neuronInput = document.createElement("input");
      const activationField = document.createElement("label");
      const activationCaption = document.createElement("span");
      const activationSelect = activationTemplate.content.firstElementChild.cloneNode(true);

      row.className = "layer-row";
      neuronField.className = "field";
      neuronField.htmlFor = `hidden-layer-${number}`;
      neuronCaption.className = "field-label";
      neuronCaption.textContent = `${layerLabel.replace("{number}", String(number))} — ${neuronsLabel}`;
      neuronInput.id = neuronField.htmlFor;
      neuronInput.name = "neurons[]";
      neuronInput.type = "number";
      neuronInput.min = "1";
      neuronInput.max = "512";
      neuronInput.required = true;
      neuronInput.value = previousValues[index]?.neurons || "16";
      neuronField.append(neuronCaption, neuronInput);

      activationField.className = "field";
      activationField.htmlFor = `hidden-layer-activation-${number}`;
      activationCaption.className = "field-label";
      activationCaption.textContent = activationLabel;
      activationSelect.id = activationField.htmlFor;
      activationSelect.value = previousValues[index]?.activation || "relu";
      activationField.append(activationCaption, activationSelect);

      row.append(neuronField, activationField);
      layerList.append(row);
    }
  }

  layerCount.addEventListener("input", renderLayers);
  renderLayers();

  form.querySelector("[data-preview-trigger]").addEventListener("click", async () => {
    if (!form.reportValidity()) {
      return;
    }

    const hiddenLayers = Array.from(layerList.querySelectorAll(".layer-row"), (row) => {
      return {
        neurons: Number(row.querySelector("input").value),
        activation: row.querySelector("select").value,
      };
    });
    const settings = Array.from(layerList.querySelectorAll(".layer-row"), (row, index) => {
      const activation = row.querySelector("select").selectedOptions[0].textContent;
      return form.dataset.layerSummaryTemplate
        .replace("{number}", String(index + 1))
        .replace("{neurons}", row.querySelector("input").value)
        .replace("{activation}", activation);
    }).join("; ");
    const summary = form.dataset.summaryTemplate
      .replace("{layers}", String(settings.length))
      .replace("{settings}", settings);
    const preview = form.parentElement.querySelector("[data-preview]");
    preview.querySelector("[data-preview-result]").textContent = summary;
    preview.hidden = false;
    await saveConfiguration(form, { hidden_layers: hiddenLayers }, preview);
  });
});

document.querySelectorAll("[data-rbf-config]").forEach((form) => {
  form.querySelector("[data-preview-trigger]").addEventListener("click", async () => {
    if (!form.reportValidity()) {
      return;
    }

    const activationInput = form.querySelector("[data-activation]");
    const activation = activationInput.selectedOptions[0].textContent;
    const summary = form.dataset.summaryTemplate
      .replace("{units}", form.querySelector("[data-radial-units]").value)
      .replace("{spread}", form.querySelector("[data-spread]").value)
      .replace("{activation}", activation);
    const preview = form.parentElement.querySelector("[data-preview]");
    preview.querySelector("[data-preview-result]").textContent = summary;
    preview.hidden = false;
    await saveConfiguration(form, {
      radial_units: Number(form.querySelector("[data-radial-units]").value),
      spread: Number(form.querySelector("[data-spread]").value),
      activation: activationInput.value,
    }, preview);
  });
});

async function saveConfiguration(form, configuration, preview) {
  const result = preview.querySelector("[data-save-result]");
  result.textContent = "";

  try {
    const response = await fetch(form.dataset.saveUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(configuration),
    });
    if (!response.ok) {
      throw new Error("save failed");
    }

    const { filename } = await response.json();
    result.textContent = form.dataset.savedMessage.replace("{filename}", filename);
  } catch {
    result.textContent = form.dataset.saveError;
  }
}
