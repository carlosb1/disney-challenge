document.addEventListener('DOMContentLoaded', function () {
  const apiUrlImages = 'http://' + window.location.host + '/api/v1/images/';

  // Function to fetch data from the API
  function fetchData() {
    fetch(apiUrlImages)
      .then(response => response.json())
      .then(data => {
        populateImage(data.results);
      })
      .catch(error => console.log(error));
  }

  // Function to populate images
  function populateImage(data) {
    const tableBody = document.getElementById('list-images');
    tableBody.innerHTML = '';

    console.log(data);

    data.forEach(item => {
      const row = document.createElement("div");
      row.className = 'row mt-4';

      const originalCol = document.createElement("div");
      originalCol.className = 'col-md-6';

      const generateCol = document.createElement("div");
      generateCol.className = 'col-md-6';


      const originalImg = document.createElement('img');
      originalImg.src = item.original_image;
      originalImg.alt = 'Original Image';
      originalImg.className = 'img-fluid';

      const generatedImg = document.createElement('img');
      generatedImg.src = item.generated_image;
      generatedImg.alt = 'Generated Image';
      generatedImg.className = 'img-fluid mt-2';

      originalCol.appendChild(originalImg);
      generateCol.appendChild(generatedImg);
      row.appendChild(originalCol);
      row.appendChild(generateCol);
      tableBody.appendChild(row);
    });
  }

  const pollingInterval = 30000;
  setInterval(fetchData, pollingInterval);
  // Fetch initial data
  fetchData();
});


