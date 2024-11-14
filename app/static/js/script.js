async function calculateBeam() {
    const data = {
      concreteClass: document.getElementById("concreteClass").value,
      fykMain: document.getElementById("fykMain").value,
      sectionWidth: document.getElementById("sectionWidth").value,
      sectionDepth: document.getElementById("sectionDepth").value,
      ultimateMoment: document.getElementById("ultimateMoment").value
    };
  
    try {
      const response = await fetch("/calculate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
      });
      const result = await response.json();
      document.getElementById("result").innerHTML = formatResult(result);
    } catch (error) {
      document.getElementById("result").innerText = "Error: " + error;
    }
  }
  
  function formatResult(result) {
    let html = "<h3>Design Summary</h3><ul>";
    for (const [key, value] of Object.entries(result)) {
      html += `<li><b>${key}:</b> ${value}</li>`;
    }
    html += "</ul>";
    return html;
  }
  
  async function savePDF() {
    const result = document.getElementById("result").innerText;
    const data = JSON.parse(result.replace(/'/g, '"'));
    
    try {
      const response = await fetch("/save_pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });
  
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "RC_Beam_Design.pdf";
        document.body.appendChild(a);
        a.click();
        a.remove();
      }
    } catch (error) {
      alert("Error saving PDF: " + error);
    }
  }
  