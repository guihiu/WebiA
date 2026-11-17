const upload = document.querySelector("[data-csv-upload]");

if (upload) {
  const fileInput = upload.querySelector("[data-csv-file]");
  const dropZone = upload.querySelector("[data-drop-zone]");
  const status = upload.querySelector("[data-csv-status]");
  const preview = upload.querySelector("[data-csv-preview]");
  const fileSummary = upload.querySelector("[data-file-summary]");
  const pageSizeInput = upload.querySelector("[data-page-size]");
  const tableCaption = upload.querySelector("[data-csv-caption]");
  const tableHead = upload.querySelector("[data-csv-head]");
  const tableBody = upload.querySelector("[data-csv-body]");
  const emptyData = upload.querySelector("[data-empty-data]");
  const pageSummary = upload.querySelector("[data-page-summary]");
  const previousButton = upload.querySelector("[data-previous]");
  const nextButton = upload.querySelector("[data-next]");
  let csvData = null;
  let currentPage = 1;

  function parseCsv(contents) {
    const text = contents.replace(/^\uFEFF/, "");
    if (text.includes("\0")) {
      throw new Error("invalid-content");
    }

    const rows = [];
    let row = [];
    let field = "";
    let inQuotes = false;

    for (let index = 0; index < text.length; index += 1) {
      const character = text[index];

      if (inQuotes) {
        if (character === '"') {
          if (text[index + 1] === '"') {
            field += '"';
            index += 1;
          } else {
            inQuotes = false;
          }
        } else {
          field += character;
        }
      } else if (character === '"' && field.length === 0) {
        inQuotes = true;
      } else if (character === ",") {
        row.push(field);
        field = "";
      } else if (character === "\n" || character === "\r") {
        if (character === "\r" && text[index + 1] === "\n") {
          index += 1;
        }
        row.push(field);
        rows.push(row);
        row = [];
        field = "";
      } else {
        field += character;
      }
    }

    if (inQuotes) {
      throw new Error("invalid-content");
    }
    if (field.length > 0 || row.length > 0) {
      row.push(field);
      rows.push(row);
    }

    return rows;
  }

  function showError(message) {
    csvData = null;
    preview.hidden = true;
    status.textContent = message;
  }

  function renderTable() {
    const pageSize = Number(pageSizeInput.value);
    const pageCount = Math.max(1, Math.ceil(csvData.rows.length / pageSize));
    currentPage = Math.min(currentPage, pageCount);
    const firstRow = (currentPage - 1) * pageSize;
    const visibleRows = csvData.rows.slice(firstRow, firstRow + pageSize);

    tableBody.replaceChildren();
    visibleRows.forEach((row) => {
      const tableRow = document.createElement("tr");
      csvData.headers.forEach((_, columnIndex) => {
        const cell = document.createElement("td");
        cell.textContent = row[columnIndex] || "";
        tableRow.append(cell);
      });
      tableBody.append(tableRow);
    });

    emptyData.hidden = csvData.rows.length > 0;
    pageSummary.textContent = upload.dataset.pageSummaryTemplate
      .replace("{page}", String(currentPage))
      .replace("{pages}", String(pageCount));
    previousButton.disabled = currentPage <= 1;
    nextButton.disabled = currentPage >= pageCount;
  }

  function renderFile(file, rows) {
    const headerRow = rows[0];
    const dataRows = rows.slice(1);
    const columnCount = rows.reduce((maximum, row) => Math.max(maximum, row.length), 0);
    const headers = Array.from({ length: columnCount }, (_, index) => {
      const heading = headerRow[index] || "";
      return heading || upload.dataset.columnTemplate.replace("{number}", String(index + 1));
    });

    csvData = { headers, rows: dataRows };
    currentPage = 1;
    tableHead.replaceChildren();
    const headerRowElement = document.createElement("tr");
    headers.forEach((heading) => {
      const cell = document.createElement("th");
      cell.scope = "col";
      cell.textContent = heading;
      headerRowElement.append(cell);
    });
    tableHead.append(headerRowElement);
    tableCaption.textContent = upload.dataset.captionTemplate
      .replace("{filename}", () => file.name);
    fileSummary.textContent = upload.dataset.fileSummaryTemplate
      .replace("{filename}", () => file.name)
      .replace("{rows}", String(dataRows.length));
    emptyData.textContent = upload.dataset.emptyData;
    status.textContent = "";
    preview.hidden = false;
    renderTable();
  }

  async function loadFile(file) {
    if (!file.name.toLowerCase().endsWith(".csv")) {
      showError(upload.dataset.invalidExtension);
      fileInput.value = "";
      return;
    }

    status.textContent = upload.dataset.loading;
    preview.hidden = true;

    try {
      const rows = parseCsv(await file.text());
      if (rows.length === 0) {
        showError(upload.dataset.emptyFile);
        fileInput.value = "";
        return;
      }
      renderFile(file, rows);
    } catch (error) {
      showError(error.message === "invalid-content"
        ? upload.dataset.invalidContent
        : upload.dataset.readError);
      fileInput.value = "";
    }
  }

  fileInput.addEventListener("change", () => {
    if (fileInput.files.length > 0) {
      loadFile(fileInput.files[0]);
    }
  });

  ["dragenter", "dragover"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropZone.classList.add("is-drag-over");
    });
  });

  ["dragleave", "drop"].forEach((eventName) => {
    dropZone.addEventListener(eventName, (event) => {
      event.preventDefault();
      dropZone.classList.remove("is-drag-over");
    });
  });

  dropZone.addEventListener("drop", (event) => {
    if (event.dataTransfer.files.length > 1) {
      showError(upload.dataset.multipleFiles);
      return;
    }
    if (event.dataTransfer.files.length === 1) {
      loadFile(event.dataTransfer.files[0]);
    }
  });

  pageSizeInput.addEventListener("change", () => {
    currentPage = 1;
    renderTable();
  });

  previousButton.addEventListener("click", () => {
    currentPage -= 1;
    renderTable();
  });

  nextButton.addEventListener("click", () => {
    currentPage += 1;
    renderTable();
  });
}
