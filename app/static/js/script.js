document.getElementById('design-form').onsubmit = async function (e) {
  e.preventDefault(); // Prevent the default form submission

  // Collect form data and convert it to JSON
  const formData = new FormData(this);
  const formJSON = Object.fromEntries(formData.entries());

  // Send the JSON data to the server
  const response = await fetch("/", {
      method: "POST",
      headers: {
          "Content-Type": "application/json",
      },
      body: JSON.stringify(formJSON),
  });

  const resultContainer = document.getElementById('result-container');
  const data = await response.json();

  if (response.ok) {
      // Display the result data in a formatted way
      resultContainer.innerHTML = `
          <h3>Design Summary</h3>
          <pre>${JSON.stringify(data, null, 2)}</pre>
      `;

      // Repopulate form fields with submitted values to retain data
      Object.keys(formJSON).forEach(key => {
          const inputElement = document.querySelector(`[name="${key}"]`);
          if (inputElement) {
              inputElement.value = formJSON[key];
          }
      });
  } else {
      // Display an error message if the request failed
      resultContainer.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
  }
};
